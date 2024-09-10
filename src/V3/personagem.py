# personagem.py
import pygame
import math
from constantes import BLACK, RED, BLUE, VERDE, ROXO, TipoObstaculo
from tiro import Tiro
import random

class Personagem:
    def __init__(self, pos, arena, radius=20, speed=5, vidas=5):
        self.pos = pos # posição do personagem
        self.radius = radius
        self.angle = 0 # orientação do personagem
        self.speed = speed # velocidade do personagem
        self.correndo = False # se está correndo
        self.lento = False # você está andando devagar
        self.arena = arena
        self.movendo = False  # Novo atributo para verificar se o personagem está se movendo
        self.tiros = []  # Lista para armazenar os tiros
        self.tempo_ultimo_tiro = 0
        self.cooldown_tiro = 150  # Tempo de cooldown em milissegundos
        self.vida_maxima = vidas  # Vida máxima do personagem
        self.vida_atual = self.vida_maxima  # Vida atual começa como máxima
        # Configurações do cone de tiro
        self.cone_minimo = 5    # Ângulo do cone quando o personagem está parado
        self.cone_padrao = 25   # Ângulo padrão do cone
        self.cone_maximo = 45   # Ângulo máximo do cone quando o personagem está correndo
        self.tmo_brl_min = 2
        self.tmo_brl_piqueno = 3
        self.tmo_brl_medio = 6
        self.tmo_brl_grande = 12
        # self.direcoes_visao = self.calcular_direcoes_visao()
        # self.direcoes_som = self.calcular_direcoes_som()
        self.alcance_visao = 100  # Alcance máximo dos feixes de visão
        self.alcance_som = 150  # Alcance máximo dos feixes de som
        self.distancia_maxima_visao = 200
        self.colisoes = [{'ponto_colisao': None, 'distancia': float('inf')} for _ in range(8)] # valores de visão e da distância de outros objetos
        self.colisoes_som = [{'ponto_colisao': None, 'distancia': float('inf')} for _ in range(12)] # valores de som e da distância de outros personagens

    def desenhar_laser_360(self, surface):
        """Desenha 12 lasers em um formato de cone a partir do personagem e verifica colisão com obstáculos."""
        num_lasers = 12
        cone_angle = 360 # Ângulo total do cone (em graus)
        half_cone_angle = cone_angle / 2

        # Desenha os lasers
        for i in range(num_lasers):
            # Calcula o ângulo do laser
            angle_offset = half_cone_angle - (i * cone_angle / (num_lasers - 1))
            laser_angle = self.angle + angle_offset
            
            # Calcula a posição final do laser
            direction = (math.cos(math.radians(laser_angle)), math.sin(math.radians(laser_angle)))
            end_pos = (self.pos[0] + direction[0] * self.distancia_maxima_visao, 
                       self.pos[1] + direction[1] * self.distancia_maxima_visao)
            
            # Desenha o laser
            pygame.draw.line(surface, ROXO, self.pos, end_pos, 2)
            
            # Verifica a colisão do laser com os obstáculos
            ponto_colisao, distancia = self._verificar_colisao_laser_com_barulho(end_pos)
            
            if ponto_colisao:
                # Adiciona a colisão à lista
                self.colisoes_som[i] = {'ponto_colisao': ponto_colisao, 'distancia': distancia}
                # Desenha um círculo vermelho no ponto de colisão
                pygame.draw.circle(surface, ROXO, ponto_colisao, 5)

    def _verificar_colisao_laser_com_barulho(self, laser_end):
        """Verifica a colisão do laser com os círculos de barulho dos outros personagens."""
        ponto_colisao = None
        menor_distancia = self.distancia_maxima_visao

        # Verifica colisão com os círculos de barulho dos outros personagens
        for personagem in self.arena.personagens:
            if personagem == self:
                continue
            # Calcula o círculo de barulho do personagem
            tamanho_barulho = personagem._atualizar_tamanho_barulho()
            centro = personagem.pos
            raio = tamanho_barulho
            colisao, ponto_colisao_personagem, distancia_personagem = self._interseccao_laser_circulo(laser_end, centro, raio)
            if colisao and distancia_personagem < menor_distancia:
                menor_distancia = distancia_personagem
                ponto_colisao = ponto_colisao_personagem

        return ponto_colisao, menor_distancia
    
    def _interseccao_laser_circulo(self, laser_end, centro_circulo, raio_circulo):
        """Verifica a colisão entre o laser e um círculo (representando o círculo de barulho)."""
        # Calcula a interseção entre o laser e o círculo
        x0, y0 = self.pos
        x1, y1 = laser_end
        cx, cy = centro_circulo
        dx, dy = x1 - x0, y1 - y0
        A = dx**2 + dy**2
        B = 2 * (dx * (x0 - cx) + dy * (y0 - cy))
        C = (x0 - cx)**2 + (y0 - cy)**2 - raio_circulo**2
        discriminant = B**2 - 4 * A * C

        if discriminant < 0:
            return False, None, float('inf')  # Sem colisão

        discriminant = math.sqrt(discriminant)
        t1 = (-B - discriminant) / (2 * A)
        t2 = (-B + discriminant) / (2 * A)

        if t1 >= 0 and t1 <= 1:
            x_colisao = x0 + t1 * dx
            y_colisao = y0 + t1 * dy
            distancia = math.hypot(x_colisao - x0, y_colisao - y0)
            return True, (int(x_colisao), int(y_colisao)), distancia

        if t2 >= 0 and t2 <= 1:
            x_colisao = x0 + t2 * dx
            y_colisao = y0 + t2 * dy
            distancia = math.hypot(x_colisao - x0, y_colisao - y0)
            return True, (int(x_colisao), int(y_colisao)), distancia

        return False, None, float('inf')  # Sem colisão

    def desenhar_laser(self, surface):
        """Desenha 8 lasers em um formato de cone a partir do personagem e verifica colisão com obstáculos."""
        num_lasers = 8
        cone_angle = 30  # Ângulo total do cone (em graus)
        half_cone_angle = cone_angle / 2

        # Desenha os lasers
        for i in range(num_lasers):
            # Calcula o ângulo do laser
            angle_offset = half_cone_angle - (i * cone_angle / (num_lasers - 1))
            laser_angle = self.angle + angle_offset
            
            # Calcula a posição final do laser
            direction = (math.cos(math.radians(laser_angle)), math.sin(math.radians(laser_angle)))
            end_pos = (self.pos[0] + direction[0] * self.distancia_maxima_visao, 
                       self.pos[1] + direction[1] * self.distancia_maxima_visao)
            
            # Desenha o laser
            pygame.draw.line(surface, RED, self.pos, end_pos, 2)
            
            # Verifica a colisão do laser com os obstáculos
            ponto_colisao, distancia = self._verificar_colisao_laser(end_pos)
            
            if ponto_colisao:
                # Adiciona a colisão à lista
                self.colisoes[i] = {'ponto_colisao': ponto_colisao, 'distancia': distancia}

                # Desenha um círculo vermelho no ponto de colisão
                pygame.draw.circle(surface, RED, ponto_colisao, 5)

    def _interseccao_laser_personagem(self, laser_inicio, laser_fim, personagem):
        """Verifica a colisão entre o laser e o círculo de um personagem."""
        dist_x = laser_fim[0] - laser_inicio[0]
        dist_y = laser_fim[1] - laser_inicio[1]
        a = dist_x**2 + dist_y**2
        b = 2 * (dist_x * (laser_inicio[0] - personagem.pos[0]) + dist_y * (laser_inicio[1] - personagem.pos[1]))
        c = (laser_inicio[0] - personagem.pos[0])**2 + (laser_inicio[1] - personagem.pos[1])**2 - personagem.radius**2
        discriminante = b**2 - 4 * a * c

        if discriminante < 0:
            return False, None, None
        
        sqrt_disc = math.sqrt(discriminante)
        t1 = (-b - sqrt_disc) / (2 * a)
        t2 = (-b + sqrt_disc) / (2 * a)

        t = min(t1, t2) if t1 < t2 else max(t1, t2)
        if t < 0:
            return False, None, None

        ponto = (laser_inicio[0] + t * dist_x, laser_inicio[1] + t * dist_y)
        distancia = math.hypot(ponto[0] - laser_inicio[0], ponto[1] - laser_inicio[1])

        return True, ponto, distancia
    
    def _interseccao_laser_arena(self, laser_inicio, laser_fim):
        """Verifica a colisão entre o laser e as bordas da arena."""
        pontos_borda = [
            (0, 0, self.arena.largura, 0),
            (self.arena.largura, 0, self.arena.largura, self.arena.altura),
            (self.arena.largura, self.arena.altura, 0, self.arena.altura),
            (0, self.arena.altura, 0, 0)
        ]
        
        ponto_colisao = None
        menor_distancia = self.distancia_maxima_visao

        for x1, y1, x2, y2 in pontos_borda:
            colisao, ponto = self._interseccao_segmento(laser_inicio, laser_fim, (x1, y1), (x2, y2))
            if colisao:
                distancia = math.hypot(ponto[0] - laser_inicio[0], ponto[1] - laser_inicio[1])
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    ponto_colisao = ponto

        return ponto_colisao, menor_distancia
    
    def _verificar_colisao_laser(self, laser_end):
        """Verifica a colisão do laser com obstáculos, outros personagens e as bordas da arena."""
        ponto_colisao = None
        menor_distancia = self.distancia_maxima_visao

        # Verifica colisão com obstáculos
        for obstaculo in self.arena.obstaculos:
            colisao, ponto = self._interseccao_laser_obstaculo(self.pos, laser_end, obstaculo)
            if colisao:
                distancia = math.hypot(ponto[0] - self.pos[0], ponto[1] - self.pos[1])
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    ponto_colisao = ponto

        # Verifica colisão com outros personagens
        for personagem in self.arena.personagens:
            if personagem == self:
                continue
            colisao, ponto_colisao_personagem, distancia_personagem = self._interseccao_laser_personagem(self.pos, laser_end, personagem)
            if colisao and distancia_personagem < menor_distancia:
                menor_distancia = distancia_personagem
                ponto_colisao = ponto_colisao_personagem

        # Verifica colisão com as bordas da arena
        ponto_colisao_arena, distancia_arena = self._interseccao_laser_arena(self.pos, laser_end)
        if ponto_colisao_arena:
            if distancia_arena < menor_distancia:
                menor_distancia = distancia_arena
                ponto_colisao = ponto_colisao_arena

        return ponto_colisao, menor_distancia
    
    def _interseccao_laser_obstaculo(self, laser_inicio, laser_fim, obstaculo):
        """Verifica a interseção entre o laser e o obstáculo."""
        # Implementa a verificação de interseção entre o segmento do laser e os lados do retângulo do obstáculo
        rect = obstaculo.rect
        pontos = [
            (rect.left, rect.top),
            (rect.right, rect.top),
            (rect.right, rect.bottom),
            (rect.left, rect.bottom)
        ]
        
        for i in range(4):
            ponto1 = pontos[i]
            ponto2 = pontos[(i + 1) % 4]
            colisao, ponto = self._interseccao_segmento(laser_inicio, laser_fim, ponto1, ponto2)
            if colisao:
                return True, ponto
        
        return False, None
    
    def _interseccao_segmento(self, A, B, C, D):
        """Verifica a interseção entre dois segmentos de linha (A-B e C-D)."""
        def orientacao(p, q, r):
            return (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

        def ponto_interseccao(p1, p2, q1, q2):
            a1, b1 = p1, p2
            a2, b2 = q1, q2
            den = (b1[0] - a1[0]) * (b2[1] - a2[1]) - (b1[1] - a1[1]) * (b2[0] - a2[0])
            if den == 0:
                return None
            ua = ((a2[0] - a1[0]) * (b2[1] - a2[1]) - (a2[1] - a1[1]) * (b2[0] - a2[0])) / den
            return (a1[0] + ua * (b1[0] - a1[0]), a1[1] + ua * (b1[1] - a1[1]))

        if (min(A[0], B[0]) <= max(C[0], D[0]) and min(C[0], D[0]) <= max(A[0], B[0]) and
            min(A[1], B[1]) <= max(C[1], D[1]) and min(C[1], D[1]) <= max(A[1], B[1])):
            if orientacao(A, B, C) * orientacao(A, B, D) <= 0 and orientacao(C, D, A) * orientacao(C, D, B) <= 0:
                ponto = ponto_interseccao(A, B, C, D)
                return ponto is not None, ponto
        return False, None
    
    def calcular_direcoes_som(self):
        direcoes = []
        num_feixes = 8
        passo = 2 * math.pi / num_feixes

        for i in range(num_feixes):
            angulo = i * passo
            direcao = (math.cos(angulo), math.sin(angulo))
            direcoes.append(direcao)
        
        return direcoes
    
    def perder_vida(self):
        """Reduz a vida do personagem em 1."""
        self.vida_atual -= 1

    def _desenhar_barra_vida(self, surface):
        """Desenha a barra de vida acima do personagem."""
        barra_largura = 40  # Largura total da barra de vida
        barra_altura = 5  # Altura da barra de vida
        barra_pos = (self.pos[0] - barra_largura // 2, self.pos[1] - self.radius - 10)  # Posição da barra de vida

        # Calcula o tamanho da vida atual proporcional à vida máxima
        vida_proporcao = self.vida_atual / self.vida_maxima
        vida_largura = int(barra_largura * vida_proporcao)

        # Desenha a barra vermelha (vida perdida)
        pygame.draw.rect(surface, (255, 0, 0), (barra_pos[0], barra_pos[1], barra_largura, barra_altura))

        # Desenha a barra verde (vida restante)
        pygame.draw.rect(surface, (0, 255, 0), (barra_pos[0], barra_pos[1], vida_largura, barra_altura))

    def receber_dano(self, dano):
        """Reduz a vida do personagem ao receber dano."""
        self.vida_atual = max(0, self.vida_atual - dano)

    def _atualizar_tamanho_barulho(self):
        velocidade_atual = self._determinar_velocidade()
        if not self.movendo:  # Verifica se o personagem está se movendo
            return self.radius * self.tmo_brl_min  # Círculo pequeno
        elif velocidade_atual < self.speed:
            return self.radius * self.tmo_brl_piqueno  # Círculo médio pequeno
        elif velocidade_atual == self.speed:
            return self.radius * self.tmo_brl_medio  # Círculo médio
        elif velocidade_atual > self.speed:
            return self.radius * self.tmo_brl_grande  # Círculo grande

    def _calcular_angulo_cone(self):
        """Calcula o ângulo do cone baseado na velocidade do personagem."""
        velocidade_atual = self._determinar_velocidade()
        if velocidade_atual < self.speed or self.movendo == False:
            cone_angulo = self.cone_minimo
        elif velocidade_atual == self.speed:
            cone_angulo = self.cone_padrao
        else:
            cone_angulo = self.cone_maximo
        return max(self.cone_minimo, min(cone_angulo, self.cone_maximo))

    def _desenhar_cone(self, surface):
        """Desenha o cone do tiro para depuração."""
        # Calcula o ângulo do cone usando a função de cálculo
        angulo_cone = self._calcular_angulo_cone()
        angulo_variacao = angulo_cone / 2
        
        # Calcula os pontos do cone
        p1 = (self.pos[0] + 100 * math.cos(math.radians(self.angle - angulo_variacao)),
            self.pos[1] + 100 * math.sin(math.radians(self.angle - angulo_variacao)))
        p2 = (self.pos[0] + 100 * math.cos(math.radians(self.angle + angulo_variacao)),
            self.pos[1] + 100 * math.sin(math.radians(self.angle + angulo_variacao)))
        
        # Desenha as linhas que formam as bordas do cone
        pygame.draw.line(surface, BLACK, self.pos, p1, 1)
        pygame.draw.line(surface, BLACK, self.pos, p2, 1)
        
        # Desenha o polígono do cone
        pygame.draw.polygon(surface, (0, 0, 255, 50), [self.pos, p1, p2], 1)

    def desenhar(self, surface):
        """Desenha o personagem e o círculo de barulho no surface."""
        pygame.draw.circle(surface, VERDE, self.pos, self.radius)
        direction = (math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle)))
        line_end = (self.pos[0] + direction[0] * self.radius, self.pos[1] + direction[1] * self.radius)
        pygame.draw.line(surface, BLACK, self.pos, line_end, 2)

        # Desenha o círculo de barulho
        tamanho_barulho = self._atualizar_tamanho_barulho()
        pygame.draw.circle(surface, BLUE, self.pos, tamanho_barulho, 1)  # Círculo com transparência

        # Desenha o cone de tiro para depuração
        self._desenhar_cone(surface)

        # Desenha a barra de vida
        self._desenhar_barra_vida(surface)

        # Desenha os tiros
        for tiro in self.tiros:
            tiro.desenhar(surface)
            
        # Desenha o laser
        self.desenhar_laser(surface)
        self.desenhar_laser_360(surface)

    def _determinar_velocidade(self):
            if self.correndo and self.lento:
                return self.speed
            elif self.correndo:
                return self.speed * 2
            elif self.lento:
                return self.speed / 2
            else:
                return self.speed

    def _calcular_movimento(self, keys):
        move_x, move_y = 0, 0
        if keys[pygame.K_w]:
            move_x += math.cos(math.radians(self.angle))
            move_y += math.sin(math.radians(self.angle))
        if keys[pygame.K_s]:
            move_x -= math.cos(math.radians(self.angle))
            move_y -= math.sin(math.radians(self.angle))
        if keys[pygame.K_a]:
            move_x += math.cos(math.radians(self.angle + 90))
            move_y += math.sin(math.radians(self.angle + 90))
        if keys[pygame.K_d]:
            move_x += math.cos(math.radians(self.angle - 90))
            move_y += math.sin(math.radians(self.angle - 90))
        return move_x, move_y

    def mover(self, keys):
        """Move o personagem baseado nas teclas pressionadas."""
        move_x, move_y = 0, 0  # Inicializa os componentes do movimento
        velocidade_atual = self._determinar_velocidade()

        if keys[pygame.K_q]:  # Rotaciona para a esquerda
            self.rotacionar_esquerda()
        if keys[pygame.K_e]:  # Rotaciona para a direita
            self.rotacionar_direita()
        # Dispara um tiro se a tecla espaço for pressionada e o personagem não estiver correndo
        if keys[pygame.K_SPACE]:
            self.atirar()

        # Atualiza o atributo movendo baseado nas teclas pressionadas
        self.movendo = any([keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d]])
        
        # Verifica as teclas pressionadas e ajusta os componentes de movimento
        if self.movendo:
            move_x, move_y = self._calcular_movimento(keys)
            # Normaliza o movimento para evitar soma excessiva de velocidades
            magnitude = math.sqrt(move_x**2 + move_y**2)
            if magnitude > 0:
                move_x = (move_x / magnitude) * velocidade_atual
                move_y = (move_y / magnitude) * velocidade_atual

            # Calcula a nova posição do personagem
            nova_pos_x = self.pos[0] + move_x
            nova_pos_y = self.pos[1] + move_y

            # Verifica colisões com obstáculos na nova posição
            para_colisao = pygame.Rect(nova_pos_x - self.radius, nova_pos_y - self.radius, self.radius * 2, self.radius * 2)
            for obstaculo in self.arena.obstaculos:
                if obstaculo.rect.colliderect(para_colisao):
                    if obstaculo.tipo == TipoObstaculo.INTRANSPONIVEL:
                        # Se o obstáculo for intransponível, não move o personagem
                        return
                    elif obstaculo.tipo == TipoObstaculo.TRANSPONIVEL:
                        # Se o obstáculo for transponível, diminui a velocidade do personagem
                        lentidao = 0.50
                        # Recalcula a nova posição com a velocidade reduzida
                        if magnitude != 0:
                            if move_x != 0:
                                move_x = (move_x / magnitude) * lentidao
                            if move_y != 0:
                                move_y = (move_y / magnitude) * lentidao
                        nova_pos_x -=  move_x
                        nova_pos_y -=  move_y

            # Atualiza a posição do personagem
            self.pos[0] = nova_pos_x
            self.pos[1] = nova_pos_y
      
        # Mantém o personagem dentro da arena
        self.pos[0] = max(self.radius, min(self.pos[0], self.arena.largura - self.radius))
        self.pos[1] = max(self.radius, min(self.pos[1], self.arena.altura - self.radius))

    def rotacionar_esquerda(self):
        """Rotaciona o personagem para a esquerda."""
        self.angle += 5

    def rotacionar_direita(self):
        """Rotaciona o personagem para a direita."""
        self.angle -= 5

    def atirar(self):
        """Lança um tiro se o personagem estiver se movendo na velocidade padrão ou menor."""
        tempo_atual = pygame.time.get_ticks()
        if (tempo_atual - self.tempo_ultimo_tiro) >= self.cooldown_tiro:
            angulo_cone = self._calcular_angulo_cone()
            angulo_variacao = random.uniform(-angulo_cone / 2, angulo_cone / 2)
            direcao_aleatoria = self.angle + angulo_variacao
            novo_tiro = Tiro(self.pos, direcao_aleatoria)
            self.tiros.append(novo_tiro)
            self.tempo_ultimo_tiro = tempo_atual  # Atualiza o tempo do último tiro

    def detectar_obstaculos(self, obstaculos):
        distancias = []
        for direcao in self.direcoes_visao:
            for obstaculo in obstaculos:
                # Cálculo da distância e verificação de interseção com o obstáculo
                distancia = self.calcular_distancia_obstaculo(direcao, obstaculo)
                if distancia < self.raio_visao:
                    distancias.append((obstaculo, distancia))
        return distancias

    def _distancia_entre_pontos(self, ponto1, ponto2):
        return math.sqrt((ponto2[0] - ponto1[0])**2 + (ponto2[1] - ponto1[1])**2)
   
    def calcular_distancia_obstaculo(self, direcao, obstaculo):
        """Calcula a distância entre o personagem e um obstáculo na direção especificada e retorna os pontos da linha de verificação."""
        # Exemplo simples: calcula o ponto de interseção entre o personagem e o obstáculo
        # Substitua o seguinte código com o cálculo real
        start_point = self.pos
        end_point = (self.pos[0] + direcao[0] * 1000, self.pos[1] + direcao[1] * 1000)  # Extende a linha para o infinito

        # Aqui você deve adicionar a lógica para calcular a interseção real com o obstáculo
        # Neste exemplo, vamos apenas retornar os pontos de início e fim e uma distância fictícia
        distancia = math.hypot(end_point[0] - start_point[0], end_point[1] - start_point[1])
        
        return distancia, start_point, end_point

    def detectar_som(self, inimigos):
        distancias = []
        for direcao in self.direcoes_som:
            for inimigo in inimigos:
                # Cálculo da distância e verificação de presença do inimigo
                distancia = self.calcular_distancia_som(direcao, inimigo)
                if distancia < self.raio_som:
                    distancias.append((inimigo, distancia))
        return distancias

    def calcular_distancia_som(self, direcao, inimigo):
        """Calcula a distância entre o personagem e um inimigo na direção especificada e retorna os pontos da linha de verificação."""
        # Exemplo simples: calcula o ponto de interseção entre o personagem e o inimigo
        # Substitua o seguinte código com o cálculo real
        start_point = self.pos
        end_point = (self.pos[0] + direcao[0] * 1000, self.pos[1] + direcao[1] * 1000)  # Extende a linha para o infinito

        # Aqui você deve adicionar a lógica para calcular a interseção real com o inimigo
        # Neste exemplo, vamos apenas retornar os pontos de início e fim e uma distância fictícia
        distancia = math.hypot(end_point[0] - start_point[0], end_point[1] - start_point[1])
        
        return distancia, start_point, end_point