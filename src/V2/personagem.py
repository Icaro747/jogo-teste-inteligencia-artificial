# personagem.py
import pygame
import math
from constantes import BLACK, RED,BLUE, TipoObstaculo

class Personagem:
    def __init__(self, pos, arena, radius=20, speed=5):
        self.pos = pos
        self.radius = radius
        self.angle = 0
        self.speed = speed
        self.correndo = False
        self.lento = False
        self.arena = arena
        self.movendo = False  # Novo atributo para verificar se o personagem está se movendo

    def _atualizar_tamanho_barulho(self):
        velocidade_atual = self._determinar_velocidade()
        if not self.movendo:  # Verifica se o personagem está se movendo
            return self.radius * 1.2  # Círculo pequeno
        elif velocidade_atual < self.speed:
            return self.radius * 1.5  # Círculo médio pequeno
        elif velocidade_atual == self.speed:
            return self.radius * 2.5  # Círculo médio
        elif velocidade_atual > self.speed:
            return self.radius * 3.5  # Círculo grande

    def desenhar(self, surface):
        """Desenha o personagem e o círculo de barulho no surface."""
        pygame.draw.circle(surface, RED, self.pos, self.radius)
        direction = (math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle)))
        line_end = (self.pos[0] + direction[0] * self.radius, self.pos[1] + direction[1] * self.radius)
        pygame.draw.line(surface, BLACK, self.pos, line_end, 2)

        # Desenha o círculo de barulho
        tamanho_barulho = self._atualizar_tamanho_barulho()
        pygame.draw.circle(surface, BLUE, self.pos, tamanho_barulho, 1)  # Círculo com transparência

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
        if keys[pygame.K_q]:  # Rotaciona para a esquerda
            self.rotacionar_esquerda()
        if keys[pygame.K_e]:  # Rotaciona para a direita
            self.rotacionar_direita()

        # Mantém o personagem dentro da arena
        self.pos[0] = max(self.radius, min(self.pos[0], self.arena.largura - self.radius))
        self.pos[1] = max(self.radius, min(self.pos[1], self.arena.altura - self.radius))

    def rotacionar_esquerda(self):
        """Rotaciona o personagem para a esquerda."""
        self.angle += 5

    def rotacionar_direita(self):
        """Rotaciona o personagem para a direita."""
        self.angle -= 5
