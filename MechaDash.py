"""
Mecha Dash — Projeto Final de Design de Software (Insper).
Versão 5: animações do personagem (correndo, voando, caindo).
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
PLAYER_SIZE = 100         # lado do sprite do player em pixels
GRAVITY = 0.6            # aceleração pra baixo (px/frame²)
THRUST = -1.0            # aceleração do jetpack (negativo = sobe)
MAX_FALL_SPEED = 12      # velocidade terminal de queda
MAX_RISE_SPEED = -10     # velocidade máxima de subida
GROUND_OFFSET = 70       # limitando o chão
CEILING_OFFSET = 110     # limitando o teto

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Mecha Dash')

# ----- Classes =====
class Player(pygame.sprite.Sprite):
    """Personagem controlado pelo jogador, com animação por estado.

    Estados:
        'run'  — apoiado no chão, 3 frames de corrida.
        'fly'  — jetpack ligado, 8 frames de chama animada.
        'fall' — no ar sem jetpack, 4 frames de queda.

    Args:
        x (int): posição horizontal inicial (centro do sprite).
        y (int): posição vertical inicial (centro do sprite).
    """

    # Tempo em ms entre frames de cada animação. Ajustado por estado:
    # corrida tem poucos frames (deve ser mais lenta), voo tem muitos
    # (deve ser mais rápida pra flame parecer flicker).
    ANIM_DELAYS = {
        'run':  120,
        'fly':  70,
        'fall': 100,
    }

    def __init__(self, x, y):
        super().__init__()

        # Carrega as listas de frames de cada estado
        self.frames_run = [
            self._load(f'assets/img/player/corrida{i}.png')
            for i in range(1, 4)         # corrida1, corrida2, corrida3
        ]
        self.frames_fly = [
            self._load(f'assets/img/player/voo{i}.png')
            for i in range(1, 9)         # voo1 até voo8
        ]
        self.frames_fall = [
            self._load(f'assets/img/player/queda{i}.png')
            for i in range(1, 5)         # queda1 até queda4
        ]

        # Estado e frame atual
        self.state = 'fall'
        self.frame_index = 0
        self.last_anim_update = pygame.time.get_ticks()

        # Sprite inicial e rect
        self.image = self.frames_fall[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Física
        self.speedy = 0
        self.thrusting = False

    def _load(self, path):
        """Carrega uma imagem PNG e redimensiona pro tamanho-padrão."""
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (PLAYER_SIZE, PLAYER_SIZE))

    def update(self):
        """Aplica física e atualiza o frame de animação."""
        # --- Física ---
        self.speedy += GRAVITY
        if self.thrusting:
            self.speedy += THRUST

        if self.speedy > MAX_FALL_SPEED:
            self.speedy = MAX_FALL_SPEED
        if self.speedy < MAX_RISE_SPEED:
            self.speedy = MAX_RISE_SPEED

        self.rect.y += self.speedy

        # Limites de tela
        if self.rect.top < CEILING_OFFSET:
            self.rect.top = CEILING_OFFSET
            self.speedy = 0
        if self.rect.bottom > HEIGHT - GROUND_OFFSET:
            self.rect.bottom = HEIGHT - GROUND_OFFSET
            self.speedy = 0

        # Detecta chão pela posição atual (não pelo evento de colisão).
        # Evita oscilação causada pela perda de fração ao somar float em rect.y int.
        on_ground = self.rect.bottom >= HEIGHT - GROUND_OFFSET

        # --- Determina o estado atual ---
        if self.thrusting:
            new_state = 'fly'
        elif on_ground:
            new_state = 'run'
        else:
            new_state = 'fall'

        # Se mudou de estado, reseta o ciclo da animação
        if new_state != self.state:
            self.state = new_state
            self.frame_index = 0
            self.last_anim_update = pygame.time.get_ticks()

        # --- Avança o frame conforme o tempo do estado atual ---
        now = pygame.time.get_ticks()
        if now - self.last_anim_update >= self.ANIM_DELAYS[self.state]:
            self.last_anim_update = now
            self.frame_index += 1

        # --- Aplica o sprite correto ---
        if self.state == 'run':
            frames = self.frames_run
        elif self.state == 'fly':
            frames = self.frames_fly
        else:  # 'fall'
            frames = self.frames_fall
        self.image = frames[self.frame_index % len(frames)]


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