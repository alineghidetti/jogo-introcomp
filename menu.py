import pygame
import sys
import subprocess
from utils import load_character_images, draw_menu

pygame.init()

# Configurações da tela
screen_width = 1024
screen_height = 768
bottom_panel = 230
character_width = 200
character_height = 200

# Carregar a imagem de fundo
background_image = pygame.image.load("img/Background/menu.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Carregar o som
pygame.mixer.music.load("soundtrack/select.wav")

def play_sound_segment(sound, start_time, duration):
    """Toca um segmento específico do som."""
    sound.play(start=start_time)  # Começar a tocar a partir do tempo especificado (em segundos)
    pygame.time.delay(int(duration * 1000))  # Aguardar o tempo de duração do segmento (convertido para milissegundos)
    sound.stop()  # Parar o som após a duração

def select_characters(screen, all_characters):
    num_characters = len(all_characters)
    selected_selections = [False] * num_characters
    selected_index = 0

    while True:
        # Desenhar o plano de fundo
        screen.blit(background_image, (0, 0))

        # Desenhar o menu
        draw_menu(screen, all_characters, selected_index, selected_selections, screen_width, screen_height, character_width, character_height)

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
                        selected_selections[selected_index] = False
                    elif sum(selected_selections) < 3:
                        selected_selections[selected_index] = True
                        pygame.mixer.music.play()
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

    character_images = load_character_images()
    all_characters = [{'name': name, 'image': image} for name, image in character_images.items()]

    selected_character_names = select_characters(screen, all_characters)
    print("Personagens selecionados:", selected_character_names)

    subprocess.run([sys.executable, 'jogo.py'] + selected_character_names)

if __name__ == "__main__":
    main()
