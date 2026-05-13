"""
Mecha Dash — Projeto Final de Design de Software (Insper).
Versão 3: adiciona o personagem (classe Player) sobre o background.
"""

# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame

pygame.init()

# ----- Constantes do jogo
WIDTH = 800
HEIGHT = 480
FPS = 60
BG_SPEED = -3            # velocidade do scroll do fundo (px/frame)
PLAYER_SIZE = 64         # lado do sprite do player em pixels

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Mecha Dash')

# ----- Classes =====
class Player(pygame.sprite.Sprite):
    """Personagem controlado pelo jogador.

    Na v3, fica parado em uma posição fixa (x = WIDTH/4, y = HEIGHT/2).
    A movimentação com gravidade e empuxo será adicionada na v4.

    Args:
        x (int): posição horizontal inicial (centro do sprite).
        y (int): posição vertical inicial (centro do sprite).
    """

    def __init__(self, x, y):
        super().__init__()
        # Carrega a imagem com canal alfa (transparência funciona)
        self.image = pygame.image.load('assets/img/player.png').convert_alpha()
        # Redimensiona pro tamanho-padrão definido nas constantes
        self.image = pygame.transform.scale(
            self.image, (PLAYER_SIZE, PLAYER_SIZE)
        )
        # Rect controla posição e colisão futura
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        """Atualiza o estado do player a cada frame.

        Vazio na v3 — o player ainda não se mexe.
        """
        pass


# ----- Inicia assets
background = pygame.image.load('assets/img/background.jpg').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
BG_WIDTH = background.get_width()

# ----- Inicia estruturas de dados
game = True
clock = pygame.time.Clock()

# Posições x das duas cópias do background
bg_x1 = 0
bg_x2 = BG_WIDTH

# Cria o player e adiciona ao grupo de sprites
player = Player(WIDTH // 4, HEIGHT // 2)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# ===== Loop principal =====
while game:
    clock.tick(FPS)

    # ----- Trata eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    # ----- Atualiza estado do jogo
    bg_x1 += BG_SPEED
    bg_x2 += BG_SPEED

    if bg_x1 + BG_WIDTH <= 0:
        bg_x1 = bg_x2 + BG_WIDTH
    if bg_x2 + BG_WIDTH <= 0:
        bg_x2 = bg_x1 + BG_WIDTH

    all_sprites.update()

    # ----- Gera saídas
    window.fill((0, 0, 0))
    window.blit(background, (bg_x1, 0))
    window.blit(background, (bg_x2, 0))
    all_sprites.draw(window)

    pygame.display.update()

# ===== Finalização =====
pygame.quit()