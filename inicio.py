import pygame
import subprocess
import sys

pygame.init()
pygame.mixer.init()  # Inicializar o mixer do Pygame

# Carregar e redimensionar imagens
img_fundo = pygame.image.load("img/Background/bkg.png")
img_fundo = pygame.transform.scale(img_fundo, (1024, 768))

img_iniciar_jogo = pygame.image.load("img/Icons/jogar.PNG")
img_iniciar_jogo = pygame.transform.scale(img_iniciar_jogo, (160, 80))

img_sair = pygame.image.load("img/Icons/sair.PNG")
img_sair = pygame.transform.scale(img_sair, (130, 70))

img_seta = pygame.image.load("img/Icons/heart.png")
img_seta = pygame.transform.scale(img_seta, (img_seta.get_width() * 0.15, img_seta.get_height() * 0.15))
rect_seta = img_seta.get_rect()
rect_seta.x = 350

# Ajuste as posições da seta para o novo layout
posicoes_seta = [390, 450]
pos_atual_seta = 0

# Configurações da tela
largura = 1024
altura = 768
tela = pygame.display.set_mode((largura, altura))

fps = 60
clock = pygame.time.Clock()
main_menu = True
fonte = pygame.font.Font('freesansbold.ttf', 40)
menu_controle = -1

# Carregar e tocar música de fundo geral
pygame.mixer.music.load("soundtrack/ost.wav")
pygame.mixer.music.play(-1)  # Reproduzir música em loop

def play_opening_animation():
    pygame.mixer.music.load("soundtrack/moonlight.wav")  # Música da animação de abertura
    pygame.mixer.music.play(-1)  # Reproduzir música da animação de abertura em loop
    for i in range(45):
        frame_path = f"img/opening/frame_{i+1}.jpg"
        frame = pygame.image.load(frame_path)
        frame = pygame.transform.scale(frame, (1024, 768))
        tela.blit(frame, (0, 0))
        pygame.display.update()
        pygame.time.delay(90)  # Ajuste a velocidade da animação conforme necessário
    # Não parar a música aqui; ela continuará tocando em loop

def play_transition_animation():
    pygame.mixer.music.load("soundtrack/ost.wav")  # Música da animação de transição
    pygame.mixer.music.play(-1)  # Reproduzir música da animação de transição em loop
    for i in range(117):
        frame_path = f"img/transition/frame_{i+1}.jpg"
        frame = pygame.image.load(frame_path)
        frame = pygame.transform.scale(frame, (1024, 768))
        tela.blit(frame, (0, 0))
        pygame.display.update()
        pygame.time.delay(70)  # Ajuste a velocidade da animação conforme necessário
    pygame.mixer.music.stop()  # Parar a música da animação de transição

# Classe para os botões
class Buttons:
    def __init__(self, image, pos):
        self.image = image
        self.pos = pos
        self.rect = self.image.get_rect(topleft=self.pos)

    def draw(self, tela):
        tela.blit(self.image, self.rect)

    def checa_clique(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False

# Função para desenhar o menu principal
def desenha_menu_principal():
    iniciar_jogo = Buttons(img_iniciar_jogo, (432, 390))
    sair = Buttons(img_sair, (448, 450))
    iniciar_jogo.draw(tela)
    sair.draw(tela)

# Exibir animação de abertura
# play_opening_animation()

run = True
while run:
    tela.blit(img_fundo, (0, 0))
    clock.tick(fps)

    if main_menu:
        desenha_menu_principal()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    pos_atual_seta += 1
                    if pos_atual_seta > 1:
                        pos_atual_seta = 1
                elif event.key == pygame.K_UP:
                    pos_atual_seta -= 1
                    if pos_atual_seta < 0:
                        pos_atual_seta = 0
                elif event.key == pygame.K_RETURN:
                    if pos_atual_seta == 0:
                        pygame.mixer.music.stop()  # Parar a música ao selecionar "Jogar"
                        play_transition_animation()  # Exibir animação ao selecionar "Jogar"
                        pygame.quit()
                        subprocess.Popen([sys.executable, 'menu.py'])
                        run = False
                    elif pos_atual_seta == 1:
                        pygame.mixer.music.stop()  # Parar a música ao selecionar "Sair"
                        run = False
        rect_seta.y = posicoes_seta[pos_atual_seta]
        menu_controle = pos_atual_seta
        tela.blit(img_seta, rect_seta)
    else:
        if menu_controle == 0:
            text = fonte.render('Iniciar jogo', True, (0, 0, 0))
            tela.blit(text, (350, 400))
        if menu_controle == 1:
            text = fonte.render('Sair', True, (0, 0, 0))
            tela.blit(text, (350, 400))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
