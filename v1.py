"""
Ashfall - Jetpack Apocalíptico
Projeto Final de Design de Software - Insper
Versão 1: estrutura básica do game loop.
"""

# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame

pygame.init()

# ----- Constantes do jogo
WIDTH = 1024
HEIGHT = 576
FPS = 60

# Paleta provisória (até termos imagem de fundo)
COR_FUNDO = (15, 10, 25)  # roxo-quase-preto, vibe apocalíptica
TITULO = 'Ashfall - Jetpack Apocaliptico'

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITULO)

# ----- Inicia estruturas de dados
game = True
clock = pygame.time.Clock()

# ===== Loop principal =====
while game:
    # Limita a 60 frames por segundo (jogo fluido em qualquer máquina)
    clock.tick(FPS)

    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False

    # ----- Atualiza estado do jogo
    # (vazio por enquanto - virá nas próximas versões)

    # ----- Gera saídas
    window.fill(COR_FUNDO)
    pygame.display.update()

# ===== Finalização =====
pygame.quit()