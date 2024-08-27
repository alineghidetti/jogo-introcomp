import pygame
import subprocess
import sys

pygame.init()

img_fundo = pygame.image.load("imagens/fundo.png")
img_fundo = pygame.transform.scale(img_fundo, (1024, 768))

img_botao = pygame.image.load("imagens/botao.png")
img_botao = pygame.transform.scale(img_botao, (350, 75))  # Ajuste proporcional para o tamanho da tela
rect_botao = img_botao.get_rect()

img_seta = pygame.image.load("imagens/seta.png")
img_seta = pygame.transform.scale(img_seta, (img_seta.get_width() * 0.15, img_seta.get_height() * 0.15))  # Ajuste proporcional para o tamanho da tela
img_seta = pygame.transform.rotate(img_seta, -90)
rect_seta = img_seta.get_rect()
rect_seta.x = 400  # Ajuste a posição da seta

# Ajuste as posições da seta para o novo layout
posicoes_seta = [150, 250]  # Ajuste para o novo layout
pos_atual_seta = 0

largura = 1024
altura = 768
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Menu do Introcomp')

fps = 60
clock = pygame.time.Clock()
main_menu = True
fonte = pygame.font.Font('freesansbold.ttf', 40)  # Ajuste do tamanho da fonte
menu_controle = -1

class Buttons:
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.button = pygame.rect.Rect(self.pos[0], self.pos[1], 350, 75)  # Ajuste do tamanho do botão

    def draw(self, tela):
        tela.blit(img_botao, self.button)
        text = fonte.render(self.text, True,(0, 0, 0))  # Anti-aliasing
        tela.blit(text, (self.pos[0] + 30, self.pos[1] + 20))  # Ajuste da posição do texto

    def checa_clique(self):
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False

def desenha_jogo():
    button = Buttons('Menu Principal', (500, 600))  # Ajuste a posição para o novo layout
    button.draw(tela)
    return button.checa_clique()

def desenha_menu_principal():
    iniciar_jogo = Buttons('Iniciar Jogo', (500, 150))
    sair = Buttons('Sair', (500, 250))

    iniciar_jogo.draw(tela)
    sair.draw(tela)

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
                        # Start the game
                        pygame.quit()
                        subprocess.Popen([sys.executable, 'menu.py'])
                        run = False
                    elif pos_atual_seta == 1:
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
