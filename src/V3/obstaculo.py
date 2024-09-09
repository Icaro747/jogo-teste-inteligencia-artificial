# obstaculo.py
import pygame
from constantes import BLACK, RED, TipoObstaculo

class Obstaculo:
    def __init__(self, pos, largura, altura, cor=BLACK, tipo=TipoObstaculo.INTRANSPONIVEL):
        self.pos = pos
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.tipo = tipo
        self.rect = pygame.Rect(pos[0], pos[1], largura, altura)

    def desenhar(self, surface):
        """Desenha o obstáculo no surface."""
        pygame.draw.rect(surface, self.cor, self.rect)
        if self.tipo == TipoObstaculo.INTRANSPONIVEL:
            pygame.draw.line(surface, RED, self.rect.topleft, self.rect.bottomright, 2)
            pygame.draw.line(surface, RED, self.rect.bottomleft, self.rect.topright, 2)
