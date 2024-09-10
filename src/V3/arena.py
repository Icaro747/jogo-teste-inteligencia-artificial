# arena.py
import pygame
from constantes import BLACK

class Arena:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.rect = pygame.Rect(0, 0, largura, altura)
        self.obstaculos = []
        self.personagens = []

    def adicionar_obstaculo(self, obstaculo):
        """Adiciona um obstáculo à lista de obstáculos."""
        self.obstaculos.append(obstaculo)

    def remover_obstaculo(self, obstaculo):
        """Remove um obstáculo da lista de obstáculos."""
        if obstaculo in self.obstaculos:
            self.obstaculos.remove(obstaculo)

    def desenhar(self, surface):
        """Desenha as bordas da arena e os obstáculos."""
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        for obstaculo in self.obstaculos:
            obstaculo.desenhar(surface)
    def adicionar_personagem(self, personagem):
        """Adiciona um personagem à lista de personagens."""
        self.personagens.append(personagem)
