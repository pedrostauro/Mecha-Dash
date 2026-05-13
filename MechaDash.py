"""
Mecha Dash — Projeto Final de Design de Software (Insper).
Versão 3: adiciona o personagem (classe Player) sobre o background.
"""

# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame

pygame.init()

# ----- Constantes do jogo
WIDTH = 1280
HEIGHT = 680
FPS = 60
BG_SPEED = -5            # velocidade do scroll do fundo (px/frame)
PLAYER_SIZE = 50         # lado do sprite do player em pixels
GRAVITY = 0.6            # aceleração pra baixo (px/frame²)
THRUST = -1.0            # aceleração do jetpack (negativo = sobe)
MAX_FALL_SPEED = 12      # velocidade terminal de queda
MAX_RISE_SPEED = -10     # velocidade máxima de subida
GROUND_OFFSET = 210      # limitando o chão
CEILING_OFFSET = 110     # limitando o teto

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Mecha Dash')

# ----- Classes =====
class Player(pygame.sprite.Sprite):
    """Personagem controlado pelo jogador.

    Posição x fixa (WIDTH/4). Posição y controlada por gravidade
    constante e empuxo do jetpack enquanto ESPAÇO estiver pressionado.

    Args:
        x (int): posição horizontal inicial (centro do sprite).
        y (int): posição vertical inicial (centro do sprite).
    """

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/img/player.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (PLAYER_SIZE, PLAYER_SIZE)
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Velocidade vertical em px/frame. Positiva = descendo.
        self.speedy = 0
        # True enquanto o jogador segura ESPAÇO.
        self.thrusting = False

    def update(self):
        """Aplica gravidade, empuxo e limites de tela a cada frame."""
        # 1. Gravidade puxa pra baixo sempre
        self.speedy += GRAVITY

        # 2. Se o jetpack está ligado, aplica empuxo pra cima
        if self.thrusting:
            self.speedy += THRUST

        # 3. Limita velocidades (terminal velocity em ambas direções)
        if self.speedy > MAX_FALL_SPEED:
            self.speedy = MAX_FALL_SPEED
        if self.speedy < MAX_RISE_SPEED:
            self.speedy = MAX_RISE_SPEED

        # 4. Aplica o movimento
        self.rect.y += self.speedy

        # 5. Prende o player entre teto e chão da tela
        if self.rect.top < CEILING_OFFSET:
            self.rect.top = CEILING_OFFSET
            self.speedy = 0           # bate no teto e para
        if self.rect.bottom > HEIGHT - GROUND_OFFSET:
            self.rect.bottom = HEIGHT - GROUND_OFFSET
            self.speedy = 0           # bate no chão e para


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
        # KEYDOWN dispara uma vez no instante que a tecla é pressionada
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.thrusting = True
        # KEYUP dispara uma vez no instante que a tecla é solta
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player.thrusting = False

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