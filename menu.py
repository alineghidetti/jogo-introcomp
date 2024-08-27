import pygame
import sys
import subprocess
from utils import load_character_images

pygame.init()

# Configurações da tela
screen_width = 1024
screen_height = 768
bottom_panel = 230
character_width = 200
character_height = 150

def draw_menu(screen, all_characters, selected_index, selected_selections):
    # Preencher fundo com a imagem
    background_img = pygame.image.load('img/Background/background.png')
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
    screen.blit(background_img, (0, 0))

    num_columns = 3  # Número de colunas
    spacing = 20  # Espaçamento entre personagens

    num_characters = len(all_characters)
    num_rows = (num_characters + num_columns - 1) // num_columns
    
    total_width = num_columns * (character_width + spacing) - spacing
    total_height = num_rows * (character_height + spacing) - spacing

    start_x = (screen_width - total_width) // 2
    start_y = (screen_height - total_height) // 2

    for i, character in enumerate(all_characters):
        x = start_x + (i % num_columns) * (character_width + spacing)
        y = start_y + (i // num_columns) * (character_height + spacing)
        
        image = pygame.transform.scale(character['image'], (character_width, character_height))
        screen.blit(image, (x, y))

        if i == selected_index:
            pygame.draw.rect(screen, (0, 0, 255), (x - 5, y - 5, character_width + 10, character_height + 10), 2)
        if selected_selections[i]:
            pygame.draw.rect(screen, (0, 255, 0), (x - 5, y - 5, character_width + 10, character_height + 10), 2)

    # Desenhar contorno em torno dos personagens selecionados
    for i, selected in enumerate(selected_selections):
        if selected:
            x = start_x + (i % num_columns) * (character_width + spacing)
            y = start_y + (i // num_columns) * (character_height + spacing)
            pygame.draw.rect(screen, (0, 255, 0), (x - 5, y - 5, character_width + 10, character_height + 10), 2)

    font = pygame.font.Font(None, 36)
    instructions = font.render('Use as setas para navegar, Z para selecionar, Enter para continuar', True, (0, 0, 0))
    screen.blit(instructions, (20, screen_height - 40))

    pygame.display.flip()

def select_characters(screen, all_characters):
    num_characters = len(all_characters)
    selected_selections = [False] * num_characters
    selected_index = 0

    while True:
        draw_menu(screen, all_characters, selected_index, selected_selections)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % num_characters
                elif event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % num_characters
                elif event.key == pygame.K_z:
                    if selected_selections[selected_index]:
                        # Se o personagem já estiver selecionado, desmarque-o
                        selected_selections[selected_index] = False
                    elif sum(selected_selections) < 3:
                        # Se menos de 3 personagens estiverem selecionados, selecione o personagem
                        selected_selections[selected_index] = True
                    else:
                        print("Você só pode selecionar até 3 personagens.")
                elif event.key == pygame.K_RETURN:
                    if sum(selected_selections) == 3:
                        selected_names = [all_characters[i]['name'] for i in range(num_characters) if selected_selections[i]]
                        return selected_names
                    else:
                        print("Selecione exatamente 3 personagens para continuar.")

def main():
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Character Selection')

    # Carregar imagens dos personagens
    character_images = load_character_images()

    # Criar uma lista de dicionários com nomes e imagens
    all_characters = [{'name': name, 'image': image} for name, image in character_images.items()]

    selected_character_names = select_characters(screen, all_characters)
    print("Personagens selecionados:", selected_character_names)

    # Passa os nomes dos personagens selecionados para o jogo
    subprocess.run([sys.executable, 'jogo.py'] + selected_character_names)


if __name__ == "__main__":
    main()