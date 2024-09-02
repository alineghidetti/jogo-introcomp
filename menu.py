import pygame
import sys
import subprocess
from utils import load_character_images, load_selection_images, draw_menu

pygame.init()

# Configurações da tela
screen_width = 1024
screen_height = 768
bottom_panel = 230
character_width = 200
character_height = 200

# Posições específicas para a imagem de cada personagem
character_positions = {
    'SailorMoon': (46, 20),
    'SailorVenus': (46, 20),
    'SailorJupiter': (46, 20),
    'SailorMars': (46, 20),
    'SailorMercury': (46, 20),
    'SailorChibiMoon': (46, 20)
}

# Carregar a imagem de fundo
background_image = pygame.image.load("img/Background/menu-select.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Carregar os sons
pygame.mixer.music.load("soundtrack/selection.wav")  # Música de fundo
select_sound = pygame.mixer.Sound("soundtrack/select.wav")  # Efeito de seleção

# Pré-redimensionar as imagens dos personagens para evitar redimensionamento contínuo
def pre_scale_images(all_characters):
    for character in all_characters:
        character['scaled_image'] = pygame.transform.scale(character['image'], (300, 300))
        # Não redimensionar a imagem de seleção
        character['selection_image'] = selection_images[character['name']]

def select_characters(screen, all_characters):
    num_characters = len(all_characters)
    selected_selections = [False] * num_characters
    selected_index = 0

    # Criar um surface para a tela temporária
    temp_surface = pygame.Surface((screen_width, screen_height))

    # Carregar imagens de seleção
    selection_images = load_selection_images()

    # Reproduzir a música de fundo em loop
    pygame.mixer.music.set_volume(0.5)  # Ajustar o volume conforme necessário
    pygame.mixer.music.play(-1)  # -1 significa loop infinito

    while True:
        # Preencher a tela temporária com a cor de fundo
        temp_surface.fill((0, 0, 0))
        temp_surface.blit(background_image, (0, 0))

        # Desenhar o menu
        draw_menu(temp_surface, all_characters, selected_index, selected_selections, screen_width, screen_height, character_width, character_height)

        # Desenhar a imagem específica do personagem selecionado
        selected_character = all_characters[selected_index]
        position = character_positions.get(selected_character['name'], (50, 175))  # Usar a posição padrão se não encontrada
        
        # Obter a imagem de seleção
        selection_image = selection_images.get(selected_character['name'])

        if selection_image:
            temp_surface.blit(selection_image, position)  # Usar a imagem redimensionada
        else:
            print(f"Imagem de seleção para {selected_character['name']} não encontrada.")

        # Blitar a superfície temporária para a tela
        screen.blit(temp_surface, (0, 0))
        pygame.display.flip()  # Atualiza a tela depois de desenhar tudo

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()  # Parar a música quando o menu for fechado
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % num_characters
                elif event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % num_characters
                elif event.key == pygame.K_z:
                    if selected_selections[selected_index]:
                        selected_selections[selected_index] = False
                    elif sum(selected_selections) < 3:
                        selected_selections[selected_index] = True
                        select_sound.play()  # Tocar o efeito de seleção
                    else:
                        print("Você só pode selecionar até 3 personagens.")
                elif event.key == pygame.K_RETURN:
                    if sum(selected_selections) == 3:
                        selected_names = [all_characters[i]['name'] for i in range(num_characters) if selected_selections[i]]
                        pygame.mixer.music.stop()  # Parar a música quando a seleção for feita
                        subprocess.run([sys.executable, 'jogo.py'] + selected_names)
                        return
                    else:
                        print("Selecione exatamente 3 personagens para continuar.")

def main():
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Character Selection')

    character_images = load_character_images()
    global selection_images
    selection_images = load_selection_images()
    all_characters = [{'name': name, 'image': image} for name, image in character_images.items()]

    # Pré-redimensionar as imagens antes de iniciar o loop
    pre_scale_images(all_characters)

    select_characters(screen, all_characters)

if __name__ == "__main__":
    main()
