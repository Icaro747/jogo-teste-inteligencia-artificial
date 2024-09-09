# personagem.py
import pygame
import math
from constantes import BLACK, RED, BLUE, VERDE, TipoObstaculo
from tiro import Tiro
import random

class Personagem:
    def __init__(self, pos, arena, radius=20, speed=5, vidas=5):
        self.pos = pos
        self.radius = radius
        self.angle = 0 # orientação do personagem
        self.speed = speed
        self.correndo = False
        self.lento = False
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
        self.direcoes_visao = self.calcular_direcoes_visao()
        self.direcoes_som = self.calcular_direcoes_som()
        self.alcance_visao = 100  # Alcance máximo dos feixes de visão
        self.alcance_som = 150  # Alcance máximo dos feixes de som

    def atualizar_angulo(self):
        self.direcoes_visao = self.calcular_direcoes_visao()  # Recalcular direções após mudança de ângulo

    def calcular_direcoes_visao(self):
        direcoes = []
        num_feixes = 8
        angulo_cone = 75
        angulo_cone_radianos = math.radians(angulo_cone)
        angulo_central = math.radians(self.angle)  # Convertendo o ângulo de orientação para radianos
        angulo_inicial = angulo_central - angulo_cone_radianos / 2
        passo_radianos = angulo_cone_radianos / (num_feixes - 1)

        for i in range(num_feixes):
            angulo = angulo_inicial + i * passo_radianos
            direcao = (math.cos(angulo), math.sin(angulo))
            direcoes.append(direcao)
            print(f'Direção {i+1}: ângulo = {math.degrees(angulo)}°, direção = {direcao}')
        
        return direcoes

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

        # Desenha os feixes de visão
        for direcao in self.direcoes_visao:
            linha_fim = (self.pos[0] + direcao[0] * self.alcance_visao, self.pos[1] + direcao[1] * self.alcance_visao)
            pygame.draw.line(surface, RED, self.pos, linha_fim, 2)
        
        # Desenha os feixes de som
        # for direcao in self.direcoes_som:
        #     pygame.draw.line(surface, (0, 255, 0), self.pos, (self.pos[0] + direcao[0] * self.radius, self.pos[1] + direcao[1] * self.radius), 2)
      
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
        self.atualizar_angulo()

    def rotacionar_direita(self):
        """Rotaciona o personagem para a direita."""
        self.angle -= 5
        self.atualizar_angulo()

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