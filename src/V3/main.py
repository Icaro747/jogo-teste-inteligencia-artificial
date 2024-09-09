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
    personagem1 = Personagem([arena.largura // 2, 30], arena, 20, 3)
    personagem2  = Personagem([arena.largura // 2, arena.altura - 30], arena, 20, 3)

    # Adicionando obstáculos à arena
    arena.adicionar_obstaculo(Obstaculo([arena.largura // 2 - 150, arena.altura // 2 - 37.5], 300, 75, Con.BLACK, Con.TipoObstaculo.INTRANSPONIVEL))
    arena.adicionar_obstaculo(Obstaculo([arena.largura - 150, arena.altura // 5], 150, 70, Con.CINZA, Con.TipoObstaculo.TRANSPONIVEL))
    arena.adicionar_obstaculo(Obstaculo([0, arena.altura // 5], 150, 70, Con.CINZA, Con.TipoObstaculo.TRANSPONIVEL))
    arena.adicionar_obstaculo(Obstaculo([arena.largura - 150, arena.altura // 2 + arena.altura // 5], 150, 70, Con.CINZA, Con.TipoObstaculo.TRANSPONIVEL))
    arena.adicionar_obstaculo(Obstaculo([0, arena.altura // 2 + arena.altura // 5], 150, 70, Con.CINZA, Con.TipoObstaculo.TRANSPONIVEL))

    # No loop principal
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
        personagem1.correndo = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        personagem1.lento = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]

        # Atualizando a posição do personagem
        personagem1.mover(keys)

        # Atualiza os tiros do personagem 1
        for tiro in personagem1.tiros[:]:
            tiro.atualizar()

            # Verifica se o tiro atingiu o personagem 2
            if tiro.verifica_colisao_personagem(personagem2):
                personagem2.perder_vida()
                personagem1.tiros.remove(tiro)

            # Verifica colisão com obstáculos ou se saiu da arena
            if tiro.verifica_colisao_obstaculos(arena.obstaculos, arena.largura, arena.altura):
                personagem1.tiros.remove(tiro)

        # Atualiza os tiros do personagem 2
        for tiro in personagem2.tiros[:]:
            tiro.atualizar()

            # Verifica se o tiro atingiu o personagem 1
            if tiro.verifica_colisao_personagem(personagem1):
                personagem1.perder_vida()
                personagem2.tiros.remove(tiro)

            # Verifica colisão com obstáculos ou se saiu da arena
            if tiro.verifica_colisao_obstaculos(arena.obstaculos, arena.largura, arena.altura):
                personagem2.tiros.remove(tiro)

        # Desenhando a arena e os personagens
        arena.desenhar(screen)
        personagem1.desenhar(screen)
        personagem2.desenhar(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
