import pygame
import math
from constantes import TipoObstaculo

class Tiro:
    def __init__(self, pos, direcao):
        self.pos = pos[:]
        self.direcao = direcao
        self.velocidade = 15
        self.raio = 5

    def atualizar(self):
        """Atualiza a posição do tiro."""
        self.pos[0] += self.velocidade * math.cos(math.radians(self.direcao))
        self.pos[1] += self.velocidade * math.sin(math.radians(self.direcao))

    def desenhar(self, surface):
        """Desenha o tiro no surface."""
        pygame.draw.circle(surface, (0, 255, 0), (int(self.pos[0]), int(self.pos[1])), 5)

    def verifica_colisao_personagem(self, personagem):
        """Verifica se o tiro colidiu com o personagem."""
        distancia = math.hypot(self.pos[0] - personagem.pos[0], self.pos[1] - personagem.pos[1])
        return distancia < (self.raio + personagem.radius)

    def verifica_colisao_obstaculos(self, obstaculos, arena_largura, arena_altura):
        # Verifica colisão com os limites da arena
        if self.pos[0] < 0 or self.pos[0] > arena_largura or self.pos[1] < 0 or self.pos[1] > arena_altura:
            return True  # O tiro ultrapassou os limites da arena
        
        # Verifica colisão com cada obstáculo
        for obstaculo in obstaculos:
            if obstaculo.tipo == TipoObstaculo.INTRANSPONIVEL and obstaculo.rect.collidepoint(self.pos):
                return True
        
        return False  # Nenhuma colisão foi detectada