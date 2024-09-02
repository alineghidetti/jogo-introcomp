import pygame


def load_character_images():
   return {
       'SailorMoon': pygame.image.load('img/Character/SailorMoon.png'),
       'SailorVenus': pygame.image.load('img/Character/SailorVenus.png'),
       'SailorJupiter': pygame.image.load('img/Character/SailorJupiter.png'),
       'SailorMars': pygame.image.load('img/Character/SailorMars.png'),
       'SailorMercury': pygame.image.load('img/Character/SailorMercury.png'),
       'SailorChibiMoon': pygame.image.load('img/Character/SailorChibiMoon.png'),
   }

def load_selection_images():
    # Suponha que as imagens estão na pasta 'img/Character/selection'
    character_names = ['SailorMoon', 'SailorVenus', 'SailorJupiter', 'SailorMars', 'SailorMercury', 'SailorChibiMoon']
    images = {}
    
    for name in character_names:
        # Carregar a imagem e redimensionar
        image_path = f"img/Character/selection/{name}.png"
        try:
            original_image = pygame.image.load(image_path)
            new_size = (805, 740)  # Tamanho desejado
            scaled_image = pygame.transform.scale(original_image, new_size)
            images[name] = scaled_image
        except pygame.error as e:
            print(f"Erro ao carregar imagem {image_path}: {e}")

    return images

def draw_text(screen, text, font, text_col, x, y):
   shadow_offset = 2
   shadow = font.render(text, True, (0, 0, 0))  # Cor da sombra
   screen.blit(shadow, (x + shadow_offset, y + shadow_offset))
  
   img = font.render(text, True, text_col)
   screen.blit(img, (x, y))


def draw_bg(screen, background_img, screen_width, screen_height):
   screen.fill((0, 0, 0))
   bg_rect = background_img.get_rect(center=(screen_width // 2, screen_height // 2))
   screen.blit(background_img, bg_rect.topleft)


def draw_panel(screen, panel_img, screen_width, screen_height, bottom_panel, player_list, font):
    screen.blit(panel_img, (15, screen_height - bottom_panel))
  
    x_start = 620
    y_start = screen_height - bottom_panel + 40
    for i, player in enumerate(player_list):
        draw_text(screen, f'{player.name}', font, (255, 255, 255), x_start, y_start + i * 60)
        draw_text(screen, f'{player.hp} / {player.max_hp}', font, (255, 255, 255), x_start + 210, y_start + i * 60)

def draw_menu(screen, all_characters, selected_index, selected_selections, screen_width, screen_height, character_width, character_height):
    # Carregar e desenhar o fundo do menu
    background_img = pygame.image.load('img/Background/menu-select.png')
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
    screen.blit(background_img, (0, 0))

    # Definir o espaçamento entre as personagens (ajuste o valor aqui)
    spacing = 1  # Definir o espaçamento para 1 pixel ou 0 para quase nulo

    num_characters = len(all_characters)
    
    # Calcular a altura total necessária para as personagens enfileiradas
    total_height = num_characters * (character_height + spacing) - spacing

    # Calcular a posição inicial no eixo X e Y
    start_x = 872
    start_y = 20
    value = 0.54

    for i, character in enumerate(all_characters):
        # Posicionar cada personagem uma abaixo da outra
        x = start_x
        y = start_y + i * (character_height*value + 15)  # Ajustar a posição Y com o novo espaçamento
        
        # Redimensionar e desenhar a imagem do personagem
        image = pygame.transform.scale(character['image'], (int(character_width * value), int(character_height * value)))
        screen.blit(image, (x, y))

        # Desenhar a borda azul em torno do personagem selecionado
        if i == selected_index:
            pygame.draw.rect(screen, (0, 0, 255), (x - 5, y - 5, int(character_width * value) + 10, int(character_height * value) + 10), 2)
        # Desenhar a borda verde em torno dos personagens já selecionados
        if selected_selections[i]:
            pygame.draw.rect(screen, (0, 255, 0), (x - 5, y - 5, int(character_width * value) + 10, int(character_height * value) + 10), 2)

    # Atualizar a tela
    pygame.display.flip()



def draw_options_panel(screen, options, selected_index, x, y, font, seta_img):
   for i, option in enumerate(options):
       color = (255, 255, 0) if i == selected_index else (255, 255, 255)
       draw_text(screen, option, font, color, x, y + i * 50)
  
   # Desenhar a seta
   seta_x = x - 40
   seta_y = y + selected_index * 50 - 5
   screen.blit(seta_img, (seta_x, seta_y))


def draw_turn_message(screen, message, x, y, font, font_size):
   turn_message_font = pygame.font.Font(font, font_size)
   draw_text(screen, message, turn_message_font, (255, 255, 0), x, y)


class Player():
    def __init__(self, x, y, name, max_hp, strength, potions, skill_strength, images, flip=False):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.skill_strength = skill_strength
        self.alive = True
        self.animation_list = []
        self.flip = flip
        self.frame_index = 0
        self.action = 0  # 0: idle, 1: attack, 2: hurt, 3: dead, 4: skill
        self.update_time = pygame.time.get_ticks()

        # Carregar as animações Idle
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'img/{self.name}/Idle/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Carregar as animações Attack
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'img/{self.name}/Attack/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Carregar as animações Hurt
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'img/{self.name}/Hurt/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Carregar as animações Death
        temp_list = []
        for i in range(7):
            img = pygame.image.load(f'img/{self.name}/Death/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Carregar as animações Skill
        temp_list = []
        for i in range(9):
            img = pygame.image.load(f'img/{self.name}/Special/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100
        current_time = pygame.time.get_ticks()

        if current_time - self.update_time > animation_cooldown:
            self.update_time = current_time
            if self.action == 3:  # Dead animation
                self.frame_index += 1
                if self.frame_index >= len(self.animation_list[self.action]):
                    self.frame_index = len(self.animation_list[self.action]) - 1  # Manter no último frame
            elif self.action == 4:  # Skill animation
                self.frame_index += 1
                if self.frame_index >= len(self.animation_list[self.action]):
                    self.frame_index = 0
                    self.action = 0  # Voltar para o idle
            else:
                self.frame_index += 1
                if self.frame_index >= len(self.animation_list[self.action]):
                    self.frame_index = 0
                    if self.action in [1, 2]:  # Attack or Hurt
                        self.action = 0  # Voltar para o idle
            self.image = self.animation_list[self.action][self.frame_index]

    def draw(self, screen):
        if self.flip:
            image = pygame.transform.flip(self.image, True, False)  # Flip horizontal
        else:
            image = self.image
        
        # Se o personagem estiver morto, desenhe o último frame da animação de morte
        if not self.alive and self.action == 3:
            image = self.animation_list[self.action][-1]  # Último frame da animação de morte

        screen.blit(image, (self.rect.x, self.rect.y))

    def atacar(self, alvo):
        if self.alive:
            self.action = 1
            self.frame_index = 0
            self.update()  # Atualizar a animação de ataque
            dano = self.strength
            alvo.receber_dano(dano)
            if not alvo.alive:
                alvo.action = 3  # Mudar para a animação de morte
                alvo.frame_index = 0  # Reiniciar a animação de morte

    def receber_dano(self, dano):
        if self.alive:
            self.hp -= dano
            if self.hp <= 0:
                self.hp = 0
                self.alive = False
                self.action = 3  # Mudar para a animação de morte
                self.frame_index = 0  # Reiniciar a animação de morte
            else:
                self.action = 2  # Mudar para a animação de dano
                self.frame_index = 0
        self.update()

    def usar_pocao(self):
        if self.potions > 0:
            self.potions -= 1
            aumento = self.max_hp * 0.2
            self.hp += aumento
            if self.hp > self.max_hp:
                self.hp = self.max_hp

    def usar_skill(self, alvo):
        if self.alive:
            self.action = 4
            self.frame_index = 0
            self.update()  # Atualizar a animação de skill
            dano = self.skill_strength
            alvo.receber_dano(dano)
            if not alvo.alive:
                alvo.action = 3  # Mudar para a animação de morte
                alvo.frame_index = 0  # Reiniciar a animação de morte
