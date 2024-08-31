import pygame
import sys
import random
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

# Definir variáveis do jogo
current_fighter = 1
total_fighters = 5
action_cooldown = 0
action_wait_time = 90

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Battle')

    font = pygame.font.Font(font_path, 20)
    seta_img = pygame.image.load('img/Icons/seta.png').convert_alpha()
    seta_img = pygame.transform.scale(seta_img, (30, 30))

    background_img = pygame.image.load('img/Background/background.png').convert_alpha()
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
    panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()

    character_images = load_character_images()

    selected_character_names = sys.argv[1:]

    player_positions = [(200, 230), (150, 330), (200, 430)]
    player_list = []

    # Defina os valores individuais de ataque e habilidade para cada personagem
    character_attributes = {
        'Knight': {'strength': 10, 'skill_strength': 20},
        'Mage': {'strength': 5, 'skill_strength': 30},
        'Warrior': {'strength': 15, 'skill_strength': 25}
    }

    for i, name in enumerate(selected_character_names):
        x, y = player_positions[i]
        attributes = character_attributes.get(name, {'strength': 10, 'skill_strength': 10})
        player_list.append(Player(x, y, name, 30, attributes['strength'], 3, attributes['skill_strength'], character_images))

    enemy1 = Player(800, 380, 'Kunzite', 20, 6, 1, 5, character_images, flip=True)
    enemy2 = Player(850, 300, 'QueenBeryl', 20, 6, 1, 5, character_images, flip=True)
    enemy_list = [enemy1, enemy2]

    all_characters = player_list + enemy_list
    turn_index = 0
    is_player_turn = True

    options = ['Ataque', 'Skill', 'Poção']
    selected_option = 0
    cont = -1

    clock = pygame.time.Clock()
    fps = 60

    run = True
    while run:
        clock.tick(fps)

        draw_bg(screen, background_img, screen_width, screen_height)
        draw_panel(screen, panel_img, screen_width, screen_height, bottom_panel, player_list, font)

        if is_player_turn:
            if len(player_list) > 0:
                turn_index = min(turn_index, len(player_list) - 1)  # Garantir que turn_index está dentro do intervalo
                current_player = player_list[turn_index]
                turn_message = f"{current_player.name}'s Turn!"
                draw_turn_message(screen, turn_message, 60, screen_height - bottom_panel + 25, font_path, 20)
                draw_options_panel(screen, options, selected_option, 60, screen_height - bottom_panel + 75, font, seta_img)
            else:
                # Se não houver jogadores, terminar o jogo
                game_over_message = 'Game Over! You have been defeated.'
                cont = 100
                is_player_turn = False
        else:
            turn_message = "Enemy's Turn!"
            draw_turn_message(screen, turn_message, 60, screen_height - bottom_panel + 25, font_path, 20)

        for player in all_characters:
            player.update()
            player.draw(screen)

        game_over_message = check_game_over(player_list, enemy_list)
        if game_over_message and cont == -1:
            cont = 100
        if cont > 0:
            cont -= 1
        if cont == 0:
            screen.fill(black)
            game_over_font = pygame.font.Font(font_path, 20)
            text_surf = game_over_font.render(game_over_message, True, white)
            text_rect = text_surf.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(text_surf, text_rect)
            pygame.display.update()
            pygame.time.wait(3000)  # Espera 3 segundos antes de fechar
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if is_player_turn:
                    if event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_UP:
                        selected_option = (selected_option - 1 + len(options)) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if len(player_list) > 0:
                            jogador_atual = player_list[turn_index]
                            if options[selected_option] == 'Ataque':
                                alvo = enemy_list[0]
                                jogador_atual.atacar(alvo)
                                if not alvo.alive:
                                    enemy_list.remove(alvo)
                            elif options[selected_option] == 'Skill':
                                alvo = enemy_list[0]
                                jogador_atual.usar_skill(alvo)
                                if not alvo.alive:
                                    enemy_list.remove(alvo)
                            elif options[selected_option] == 'Poção':
                                jogador_atual.usar_pocao()
                            
                            turn_index = (turn_index + 1) % len(player_list)
                            selected_option = 0
                            is_player_turn = False
                            # Garantir que turn_index está dentro do intervalo após a remoção
                            turn_index = min(turn_index, len(player_list) - 1)
                else:
                    if player_list:
                        alvo = random.choice(player_list)
                        for enemy in enemy_list:
                            if enemy.alive:
                                enemy.atacar(alvo)
                                if not alvo.alive:
                                    player_list.remove(alvo)
                                break
                        # Garantir que turn_index está dentro do intervalo após a remoção
                        turn_index = min(turn_index, len(player_list) - 1)

                    is_player_turn = True

        pygame.display.update()

if __name__ == "__main__":
    main()
