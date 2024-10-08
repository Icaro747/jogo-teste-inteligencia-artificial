# constantes.py
import pygame
from enum import Enum

# Configurações da tela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800

# Definindo cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE =  (0, 0, 255, 50)

# Enumerador para tipos de obstáculos
class TipoObstaculo(Enum):
    INTRANSPONIVEL = 1
    TRANSPONIVEL = 2
