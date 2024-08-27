import pygame
import sys
from utils import load_character_images

# Configurações da tela
screen_width = 1024
screen_height = 768
bottom_panel = 230
character_width = 120
character_height = 150

# Definir cores
red = (255, 0, 0)
white = (255, 255, 255) 

# Caminho para a fonte
font_path = 'Press_Start_2P/PressStart2P-Regular.ttf'

# Função para desenhar texto
def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg(screen, background_img, screen_width, screen_height):
    screen.fill((0, 0, 0))
    bg_rect = background_img.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(background_img, bg_rect.topleft)

def draw_panel(screen, panel_img, screen_width, bottom_panel, player_list, font):
    # Desenhar o painel
    screen.blit(panel_img, (15, screen_height - bottom_panel))
    
    # Mostrar informações dos personagens
    x_start = 660
    y_start = screen_height - bottom_panel + 40
    for i, player in enumerate(player_list):
        draw_text(screen, f'{player.name}', font, white, x_start, y_start + i * 60)
        draw_text(screen, f'{player.hp} / {player.max_hp}', font, white, x_start + 150, y_start + i * 60)
        # draw_text(screen, f'Strength: {player.strength}', font, white, x_start + 300, y_start + i * 40)

class Player():
    def __init__(self, x, y, name, max_hp, strength, potions, images):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 # 0: idle, 1: attack, 2: hurt, 3: dead
        self.update_time = pygame.time.get_ticks()

        # Carregar as animações Idle
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Idle/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width()*3, img.get_height()*3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Carregar as animações Attack (exemplo, ajuste conforme necessário)
        temp_list = []
        for i in range(8):  # Supondo que tenha 8 quadros de ataque
            img = pygame.image.load(f'img/{self.name}/Attack/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width()*3, img.get_height()*3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Outras animações como 'Hurt' e 'Dead' podem ser adicionadas aqui

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100
        current_time = pygame.time.get_ticks()

        if current_time - self.update_time > animation_cooldown:
            self.update_time = current_time
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
            self.image = self.animation_list[self.action][self.frame_index]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Battle')

    # Definir fontes após inicializar Pygame
    font = pygame.font.Font(font_path, 20)

    # Carregar imagens de fundo e painel
    background_img = pygame.image.load('img/Background/background.png').convert_alpha()
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
    panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()

    # Carregar imagens dos personagens
    character_images = load_character_images()

    # Obter personagens selecionados da linha de comando
    selected_character_names = sys.argv[1:]  # Recebe argumentos de linha de comando

    # Criar instâncias dos jogadores
    player_positions = [(200, 230), (150, 330), (200, 430)]  # Posições dos personagens
    player_list = []
    for i, name in enumerate(selected_character_names):
        x, y = player_positions[i]
        player_list.append(Player(x, y, name, 30, 10, 3, character_images))

    # Definir inimigos de exemplo
    bandit1 = Player(800, 380, 'Bandit', 20, 6, 1, character_images)
    bandit2 = Player(850, 300, 'Bandit', 20, 6, 1, character_images)
    bandit_list = [bandit1, bandit2]

    clock = pygame.time.Clock()
    fps = 60

    run = True
    while run:
        clock.tick(fps)

        # Desenhar fundo
        draw_bg(screen, background_img, screen_width, screen_height)

        # Desenhar painel com informações dos personagens
        draw_panel(screen, panel_img, screen_width, bottom_panel, player_list, font)

        # Desenhar jogadores
        for player in player_list:
            player.update()
            player.draw(screen)

        # Desenhar inimigos
        for bandit in bandit_list:
            bandit.update()
            bandit.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main()