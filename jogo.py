import pygame
import sys
import random
import subprocess
from utils import load_character_images, draw_bg, draw_panel, draw_options_panel, draw_turn_message, Player

# Configurações da tela
screen_width = 1024
screen_height = 768
bottom_panel = 230
character_width = 120
character_height = 150

# Definir cores
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)  # Cor da sombra

# Caminho para a fonte
font_path = 'Press_Start_2P/PressStart2P-Regular.ttf'

# Carregar a música de fundo
def play_background_music():
    try:
        pygame.mixer.music.load('soundtrack/game.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # -1 significa loop infinito
    except pygame.error as e:
        print(f"Erro ao carregar a música: {e}")

# Carregar os frames da animação de Game Over
def load_game_over_animation():
    frames = []
    for i in range(145):  # Total de 145 frames
        frame = pygame.image.load(f'img/Game-over/{i+1}.png').convert_alpha()
        frame = pygame.transform.scale(frame, (screen_width, screen_height))  # Ajustar o tamanho da tela
        frames.append(frame)
    return frames

# Reproduzir a animação de Game Over
def play_game_over_animation(screen, frames, speed=100):
    pygame.mixer.music.load('soundtrack/game-over.wav')
    pygame.mixer.music.play()
    for frame in frames:
        screen.blit(frame, (0, 0))
        pygame.display.update()
        pygame.time.delay(speed)  # Ajuste a velocidade da animação conforme necessário
    pygame.mixer.music.stop()

# Carregar a animação de Vitória
def load_winner_animation():
    frames = []
    for i in range(300):  # Total de 300 frames
        frame = pygame.image.load(f'img/Win/{i+1}.png').convert_alpha()
        frame = pygame.transform.scale(frame, (screen_width, screen_height))  # Ajustar o tamanho da tela
        frames.append(frame)
    return frames

# Reproduzir a animação de Vitória
def play_winner_animation(screen, frames, fps=60):  # Use o parâmetro 'fps'
    pygame.mixer.music.load('soundtrack/win.wav')
    pygame.mixer.music.play()

    clock = pygame.time.Clock()  # Criar um objeto Clock para controlar o FPS
    frame_time = 1000 // fps  # Tempo por frame em milissegundos

    for frame in frames:
        screen.blit(frame, (0, 0))
        pygame.display.update()
        clock.tick(fps)  # Controla a taxa de frames por segundo

    pygame.mixer.music.stop()

# Carregar a animação após seleção dos personagens
def load_start_animation():
    frames = []
    zoom_x = 1.5  # Fator de zoom no eixo X
    zoom_y = 1  # Fator de zoom no eixo Y
    for i in range(351):  # Total de 351 frames
        frame = pygame.image.load(f'img/Start/{i+1}.png').convert_alpha()
        # Aplicar zoom e redimensionamento
        new_width = int(screen_width * zoom_x)
        new_height = int(screen_height * zoom_y)
        frame = pygame.transform.scale(frame, (new_width, new_height))
        frames.append(frame)
    return frames

# Reproduzir a animação após a seleção dos personagens
def play_start_animation(screen, frames, speed=50):
    pygame.mixer.music.load('soundtrack/start.wav')
    pygame.mixer.music.play()

    screen_rect = pygame.Rect(0, 0, screen_width, screen_height)
    for frame in frames:
        frame_rect = frame.get_rect()
        # Calcular a posição para centralizar a imagem
        x = (frame_rect.width - screen_width) // 2
        y = (frame_rect.height - screen_height) // 2
        cropped_frame = frame.subsurface(pygame.Rect(x, y, screen_width, screen_height))
        
        screen.blit(cropped_frame, (0, 0))
        pygame.display.update()
        pygame.time.delay(speed)  # Ajuste a velocidade da animação conforme necessário

    pygame.mixer.music.stop()

def draw_text(screen, text, font, text_col, x, y):
    shadow_offset = 2
    shadow = font.render(text, True, black)
    screen.blit(shadow, (x + shadow_offset, y + shadow_offset))
  
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def check_game_over(player_list, enemy_list):
    if not player_list:
        return 'Game Over! You have been defeated.'
    elif not enemy_list:
        return 'Victory! All enemies have been defeated.'
    return None

def show_end_screen(screen, font, background_img):
    options = ['Jogar Novamente', 'Sair']
    selected_option = 0

    while True:
        screen.blit(background_img, (0, 0))
        draw_text(screen, 'Escolha uma opção:', font, white, 500, 200)
        for i, option in enumerate(options):
            color = red if i == selected_option else white
            draw_text(screen, option, font, color, 500, 230 + i * 30)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1 + len(options)) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected_option] == 'Jogar Novamente':
                        return 'restart'
                    elif options[selected_option] == 'Sair':
                        pygame.quit()
                        sys.exit()

def main():
    pygame.init()
    pygame.mixer.init()  # Inicializar o mixer
    play_background_music()  # Começar a tocar a música de fundo

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Battle')

    font = pygame.font.Font(font_path, 20)
    panel_font = pygame.font.Font(font_path, 15)  # Fonte para o painel
    seta_img = pygame.image.load('img/Icons/seta.png').convert_alpha()
    seta_img = pygame.transform.scale(seta_img, (30, 30))

    background_img = pygame.image.load('img/Background/background.png').convert_alpha()
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
    panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()
    menu_background_img = pygame.image.load('img/Background/final.png').convert_alpha()
    menu_background_img = pygame.transform.scale(menu_background_img, (screen_width, screen_height))

    character_images = load_character_images()
    selected_character_names = sys.argv[1:]

    game_over_frames = load_game_over_animation()
    start_frames = load_start_animation()

    player_positions = [(300, 300), (150, 330), (250, 400)]
    player_list = []

    character_attributes = {
        'SailorMoon': {'max_hp': 100, 'strength': 50, 'skill_strength': 80},
        'SailorChibiMoon': {'max_hp': 100, 'strength': 15, 'skill_strength': 25},
        'SailorMars': {'max_hp': 100, 'strength': 45, 'skill_strength': 50},
        'SailorJupiter': {'max_hp': 100, 'strength': 35, 'skill_strength': 45},
        'SailorMercury': {'max_hp': 100, 'strength': 35, 'skill_strength': 40},
        'SailorVenus': {'max_hp': 100, 'strength': 40, 'skill_strength': 50}
    }

    for i, name in enumerate(selected_character_names):
        x, y = player_positions[i]
        attributes = character_attributes.get(name, {'max_hp': 100, 'strength': 20, 'skill_strength': 30})
        player_list.append(Player(x, y, name, attributes['max_hp'], attributes['strength'], 3, attributes['skill_strength'], character_images))

    enemy1 = Player(750, 380, 'Kunzite', 1, 6, 1, 5, character_images, flip=True)
    enemy2 = Player(850, 300, 'QueenBeryl', 1, 6, 1, 5, character_images, flip=True)
    enemy_list = [enemy1, enemy2]

    all_characters = player_list + enemy_list
    turn_index = 0
    is_player_turn = True
    is_selecting_enemy = False
    selected_enemy_index = 0
    options = ['Ataque', 'Skill', 'Poção']
    selected_option = 0
    game_over = False  # Adicionado para controlar o estado de finalização do jogo
    cont = -1  # Variável para controlar o tempo de exibição da mensagem de Game Over

    clock = pygame.time.Clock()
    fps = 60

    play_start_animation(screen, start_frames, speed=30)  # Reproduzir a animação de início

    while True:
        clock.tick(fps)

        draw_bg(screen, background_img, screen_width, screen_height)
        draw_panel(screen, panel_img, screen_width, screen_height, bottom_panel, player_list, panel_font)

        if not game_over:
            if is_player_turn:
                if len(player_list) > 0:
                    turn_index = min(turn_index, len(player_list) - 1)
                    current_player = player_list[turn_index]
                    turn_message = f"{current_player.name}'s Turn!"
                    draw_turn_message(screen, turn_message, 60, screen_height - bottom_panel + 25, font_path, 20)

                    if is_selecting_enemy:
                        enemy_message = f"Select enemy: {enemy_list[selected_enemy_index].name}"
                        draw_text(screen, enemy_message, font, white, 60, screen_height - bottom_panel + 50)
                    else:
                        draw_options_panel(screen, options, selected_option, 60, screen_height - bottom_panel + 75, font, seta_img)
                else:
                    game_over = True
                    game_over_message = 'Game Over! You have been defeated.'
                    cont = 100  # Inicia o temporizador de exibição da mensagem de Game Over
            else:
                turn_message = "Enemy's Turn!"
                draw_turn_message(screen, turn_message, 60, screen_height - bottom_panel + 25, font_path, 20)

            for player in all_characters:
                player.update()
                player.draw(screen)

            if not game_over:
                game_over_message = check_game_over(player_list, enemy_list)
                if game_over_message:
                    if 'Game Over' in game_over_message:
                        game_over = True
                        cont = 100  # Inicia o temporizador de exibição da mensagem de Game Over
                    elif 'Victory' in game_over_message:
                        play_winner_animation(screen, load_winner_animation(), fps=50)  # Defina o FPS desejado
                        pygame.time.wait(2000)
                        result = show_end_screen(screen, font, menu_background_img)
                        if result == 'restart':
                            break  # Voltar para o início do loop principal
                        else:
                            pygame.quit()
                            sys.exit()

        if game_over:
            if cont > 0:
                cont -= 1
                if cont > 0:
                    screen.fill(black)
                    game_over_font = pygame.font.Font(font_path, 20)
                    text_surf = game_over_font.render(game_over_message, True, white)
                    text_rect = text_surf.get_rect(center=(screen_width // 2, screen_height // 2))
                    screen.blit(text_surf, text_rect)
                    pygame.display.update()
                else:
                    play_game_over_animation(screen, game_over_frames, speed=100)
                    pygame.time.wait(3000)
                    result = show_end_screen(screen, font, menu_background_img)
                    if result == 'restart':
                        break  # Voltar para o início do loop principal
                    else:
                        pygame.quit()
                        sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if is_player_turn:
                    if is_selecting_enemy:
                        if event.key == pygame.K_LEFT:
                            selected_enemy_index = (selected_enemy_index - 1 + len(enemy_list)) % len(enemy_list)
                        elif event.key == pygame.K_RIGHT:
                            selected_enemy_index = (selected_enemy_index + 1) % len(enemy_list)
                        elif event.key == pygame.K_z:
                            if len(enemy_list) > 0:
                                selected_enemy = enemy_list[selected_enemy_index]
                                if options[selected_option] == 'Ataque':
                                    current_player.atacar(selected_enemy)
                                    if not selected_enemy.alive:
                                        enemy_list.remove(selected_enemy)
                                elif options[selected_option] == 'Skill':
                                    current_player.usar_skill(selected_enemy)
                                    if not selected_enemy.alive:
                                        enemy_list.remove(selected_enemy)
                                elif options[selected_option] == 'Poção':
                                    current_player.usar_pocao()
                                
                                turn_index = (turn_index + 1) % len(player_list)
                                selected_option = 0
                                is_selecting_enemy = False
                                is_player_turn = False
                                turn_index = min(turn_index, len(player_list) - 1)
                    else:
                        if event.key == pygame.K_DOWN:
                            selected_option = (selected_option + 1) % len(options)
                        elif event.key == pygame.K_UP:
                            selected_option = (selected_option - 1 + len(options)) % len(options)
                        elif event.key == pygame.K_RETURN:
                            if len(enemy_list) > 0:
                                is_selecting_enemy = True
                else:
                    if player_list:
                        alvo = random.choice(player_list)
                        for enemy in enemy_list:
                            if enemy.alive:
                                enemy.atacar(alvo)
                                if not alvo.alive:
                                    player_list.remove(alvo)
                                break
                        turn_index = min(turn_index, len(player_list) - 1)
                        is_player_turn = True

        pygame.display.update()

if __name__ == "__main__":
    main()
