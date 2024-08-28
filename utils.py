import pygame


def load_character_images():
   return {
       'Knight': pygame.image.load('img/Knight/Idle/0.png'),
       'Bandit': pygame.image.load('img/Knight/Idle/0.png'),
       'Warrior': pygame.image.load('img/Knight/Idle/0.png'),
       'Mage': pygame.image.load('img/Knight/Idle/0.png'),
       # Adicione outros personagens conforme necessário
   }


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
  
   x_start = 650
   y_start = screen_height - bottom_panel + 40
   for i, player in enumerate(player_list):
       draw_text(screen, f'{player.name}', font, (255, 255, 255), x_start, y_start + i * 60)
       draw_text(screen, f'{player.hp} / {player.max_hp}', font, (255, 255, 255), x_start + 150, y_start + i * 60)


def draw_menu(screen, all_characters, selected_index, selected_selections, screen_width, screen_height, character_width, character_height):
   background_img = pygame.image.load('img/Background/background.png')
   background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
   screen.blit(background_img, (0, 0))


   num_columns = 3
   spacing = 20


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


   for i, selected in enumerate(selected_selections):
       if selected:
           x = start_x + (i % num_columns) * (character_width + spacing)
           y = start_y + (i // num_columns) * (character_height + spacing)
           pygame.draw.rect(screen, (0, 255, 0), (x - 5, y - 5, character_width + 10, character_height + 10), 2)


   font = pygame.font.Font(None, 36)
   instructions = font.render('Use as setas para navegar, Z para selecionar, Enter para continuar', True, (0, 0, 0))
   screen.blit(instructions, (20, screen_height - 40))


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


import pygame


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
       self.action = 0  # 0: idle, 1: attack, 2: hurt, 3: dead
       self.update_time = pygame.time.get_ticks()


       # Carregar as animações Idle
       temp_list = []
       for i in range(8):
           img = pygame.image.load(f'img/{self.name}/Idle/{i}.png').convert_alpha()
           img = pygame.transform.scale(img, (img.get_width()*3, img.get_height()*3))
           temp_list.append(img)
       self.animation_list.append(temp_list)


       # Carregar as animações Attack
       temp_list = []
       for i in range(8):
           img = pygame.image.load(f'img/{self.name}/Attack/{i}.png').convert_alpha()
           img = pygame.transform.scale(img, (img.get_width()*3, img.get_height()*3))
           temp_list.append(img)
       self.animation_list.append(temp_list)


       # Carregar as animações Hurt
       temp_list = []
       for i in range(3):
           img = pygame.image.load(f'img/{self.name}/Hurt/{i}.png').convert_alpha()
           img = pygame.transform.scale(img, (img.get_width()*3, img.get_height()*3))
           temp_list.append(img)
       self.animation_list.append(temp_list)


       # Carregar as animações Death
       temp_list = []
       for i in range(10):
           img = pygame.image.load(f'img/{self.name}/Death/{i}.png').convert_alpha()
           img = pygame.transform.scale(img, (img.get_width()*3, img.get_height()*3))
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
           else:
               self.frame_index += 1
               if self.frame_index >= len(self.animation_list[self.action]):
                   self.frame_index = 0
                   if self.action in [1, 2]:  # Attack or Hurt
                       self.action = 0  # Voltar para o idle
           self.image = self.animation_list[self.action][self.frame_index]


   def draw(self, screen):
       screen.blit(self.image, self.rect)


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






