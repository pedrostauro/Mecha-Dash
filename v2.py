# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame

pygame.init()

# ----- Gera tela principal
WIDTH = 800
HEIGHT = 480
FPS = 60
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Mecha Dash')

# ----- Inicia assets
# Carrega o background e redimensiona para a altura da janela,
# mantendo proporção visual. A largura final será BG_WIDTH.
background = pygame.image.load('assets/img/background.jpg').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
BG_WIDTH = background.get_width()

# ----- Inicia estruturas de dados
game = True
clock = pygame.time.Clock()

# Posições x das duas cópias do background.
# A segunda começa logo após a primeira, formando uma faixa contínua.
bg_x1 = 0
bg_x2 = BG_WIDTH

# Velocidade do scroll (pixels por frame). Valor negativo = move pra esquerda.
BG_SPEED = -4

# ===== Loop principal =====
while game:
    clock.tick(FPS)

    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False

    # ----- Atualiza estado do jogo
    # Desloca as duas cópias para a esquerda
    bg_x1 += BG_SPEED
    bg_x2 += BG_SPEED

    # Se a primeira cópia saiu completamente da tela pela esquerda,
    # reposiciona ela à direita da segunda.
    if bg_x1 + BG_WIDTH <= 0:
        bg_x1 = bg_x2 + BG_WIDTH

    # Mesma coisa para a segunda cópia.
    if bg_x2 + BG_WIDTH <= 0:
        bg_x2 = bg_x1 + BG_WIDTH

    # ----- Gera saídas
    window.fill((0, 0, 0))
    window.blit(background, (bg_x1, 0))
    window.blit(background, (bg_x2, 0))

    pygame.display.update()

# ===== Finalização =====
pygame.quit()