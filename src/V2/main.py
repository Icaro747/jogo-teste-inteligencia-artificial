# main.py
import pygame
import constantes as Con
from arena import Arena
from personagem import Personagem
from obstaculo import Obstaculo

def main():
    pygame.init()
    screen = pygame.display.set_mode((Con.SCREEN_WIDTH, Con.SCREEN_HEIGHT))
    pygame.display.set_caption('Teste de Jogo Simples - Arena')
    clock = pygame.time.Clock()

    # Criando uma instância da arena e do personagem
    arena = Arena(600, 600)
    personagem = Personagem([arena.largura // 2, arena.altura // 2], arena)

    # Adicionando obstáculos à arena
    arena.adicionar_obstaculo(Obstaculo([150, 150], 200, 50, Con.BLACK, Con.TipoObstaculo.INTRANSPONIVEL))
    arena.adicionar_obstaculo(Obstaculo([300, 200], 70, 70, Con.BLACK, Con.TipoObstaculo.TRANSPONIVEL))

    running = True
    while running:
        clock.tick(60)
        screen.fill(Con.WHITE)

        # Capturando eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Capturando teclas pressionadas
        keys = pygame.key.get_pressed()
        personagem.correndo = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        personagem.lento = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]

        # Atualizando a posição do personagem
        personagem.mover(keys)

        # Desenhando a arena e o personagem
        arena.desenhar(screen)
        personagem.desenhar(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
