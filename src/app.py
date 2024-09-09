import pygame
import math

# Inicializando o pygame
pygame.init()

# Configurações da tela (tamanho da tela pode ser diferente do tamanho da arena)
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Teste de Jogo Simples - Arena')

# Definindo cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Arena:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.rect = pygame.Rect(0, 0, largura, altura)
        self.obstaculos = []  # Lista de obstáculos

    def adicionar_obstaculo(self, obstaculo):
        """Adiciona um obstáculo à lista de obstáculos."""
        self.obstaculos.append(obstaculo)

    def remover_obstaculo(self, obstaculo):
        """Remove um obstáculo da lista de obstáculos."""
        if obstaculo in self.obstaculos:
            self.obstaculos.remove(obstaculo)

    def desenhar(self, surface):
        """Desenha as bordas da arena e os obstáculos."""
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Desenha o retângulo da arena
        for obstaculo in self.obstaculos:
            obstaculo.desenhar(surface)

# Classe Obstaculo
class Obstaculo:
    INTRANSPONIVEL = 1
    TRANSPONIVEL = 2

    def __init__(self, pos, largura, altura, cor=BLACK, tipo=INTRANSPONIVEL):
        self.pos = pos  # Posição [x, y] do canto superior esquerdo do obstáculo
        self.largura = largura  # Largura do obstáculo
        self.altura = altura  # Altura do obstáculo
        self.cor = cor  # Cor do obstáculo
        self.tipo = tipo  # Tipo do obstáculo (INTRANSPONIVEL ou TRANSPONIVEL)
        self.rect = pygame.Rect(pos[0], pos[1], largura, altura)  # Retângulo para colisão

    def desenhar(self, surface):
        """Desenha o obstáculo no surface."""
        pygame.draw.rect(surface, self.cor, self.rect)
        # Opcional: Indicar visualmente o tipo de obstáculo
        if self.tipo == self.INTRANSPONIVEL:
            pygame.draw.line(surface, RED, self.rect.topleft, self.rect.bottomright, 2)
            pygame.draw.line(surface, RED, self.rect.bottomleft, self.rect.topright, 2)

# Classe Personagem
class Personagem:
    def __init__(self, pos, arena, radius=20, speed=5):
        self.pos = pos  # Posição [x, y] da bolinha
        self.radius = radius  # Raio da bolinha
        self.angle = 0  # Ângulo de rotação
        self.speed = speed  # Velocidade de movimento
        self.correndo = False  # Estado de corrida
        self.lento = False  # Estado de movimento lento
        self.arena = arena  # Arena onde o personagem está localizado

    def desenhar(self, surface):
        """Desenha a bolinha no surface."""
        pygame.draw.circle(surface, RED, self.pos, self.radius)
        # Desenha a linha indicando a direção da bolinha
        direction = (math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle)))
        line_end = (self.pos[0] + direction[0] * self.radius, self.pos[1] + direction[1] * self.radius)
        pygame.draw.line(surface, BLACK, self.pos, line_end, 2)

    def mover(self, keys):
        """Move o personagem baseado nas teclas pressionadas."""
        move_x, move_y = 0, 0  # Inicializa os componentes do movimento

        # Ajusta a velocidade de acordo com o estado do personagem
        if self.correndo and self.lento:  # Shift + Control = "velocidade anormal"
            velocidade_atual = velocidade_atual  # Defina aqui a velocidade "anormal"
        elif self.correndo:  # Apenas Shift
            velocidade_atual = self.speed * 2
        elif self.lento:  # Apenas Control
            velocidade_atual = self.speed / 2
        else:
            velocidade_atual = self.speed

        # Verifica as teclas pressionadas e ajusta os componentes de movimento
        if keys[pygame.K_w]:  # Move para frente
            move_x += math.cos(math.radians(self.angle))
            move_y += math.sin(math.radians(self.angle))
        if keys[pygame.K_s]:  # Move para trás
            move_x -= math.cos(math.radians(self.angle))
            move_y -= math.sin(math.radians(self.angle))
        if keys[pygame.K_a]:  # Move para a esquerda
            move_x += math.cos(math.radians(self.angle + 90))
            move_y += math.sin(math.radians(self.angle + 90))
        if keys[pygame.K_d]:  # Move para a direita
            move_x += math.cos(math.radians(self.angle - 90))
            move_y += math.sin(math.radians(self.angle - 90))

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
                if obstaculo.tipo == Obstaculo.INTRANSPONIVEL:
                    # Se o obstáculo for intransponível, não move o personagem
                    return
                elif obstaculo.tipo == Obstaculo.TRANSPONIVEL:
                    # Se o obstáculo for transponível, diminui a velocidade do personagem
                    lentidao = 0.50
                    # Recalcula a nova posição com a velocidade reduzida
                    move_x = (move_x / magnitude) * lentidao
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


# Loop principal do jogo
running = True
clock = pygame.time.Clock()

# Criando uma instância da arena e do personagem
arena = Arena(400, 300)  # Definindo a arena com largura 400 e altura 300
personagem = Personagem([arena.largura // 2, arena.altura // 2], arena)

# Adicionando obstáculos à arena
obstaculo1 = Obstaculo([100, 100], 50, 50, BLACK, Obstaculo.INTRANSPONIVEL)
obstaculo2 = Obstaculo([300, 200], 70, 70, BLACK, Obstaculo.TRANSPONIVEL)
arena.adicionar_obstaculo(obstaculo1)
arena.adicionar_obstaculo(obstaculo2)

while running:
    clock.tick(60)  # Limita o FPS a 60 frames por segundo
    screen.fill(WHITE)

    # Capturando eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Capturando teclas pressionadas
    keys = pygame.key.get_pressed()

    # Verifica o estado de corrida (Shift) e movimento lento (Control)
    personagem.correndo = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]  # Shift pressionado
    personagem.lento = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]  # Control pressionado

    # Controlando o personagem
    personagem.mover(keys)
    if keys[pygame.K_q]:  # Rotaciona para a esquerda
        personagem.rotacionar_esquerda()
    if keys[pygame.K_e]:  # Rotaciona para a direita
        personagem.rotacionar_direita()

    # Desenhando a arena e o personagem
    arena.desenhar(screen)
    personagem.desenhar(screen)

    # Atualizando a tela
    pygame.display.flip()

pygame.quit()
