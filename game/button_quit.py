import pygame.font

class Button_quit:

    def __init__(self, ai_game, msg, x, y):
        """Инициализация кнопки"""

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.x = x
        self.y = y
        self.width, self.height = 200, 50
        self.button_color = (36, 61, 92)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font("fonts/Undertale-Battle-Font.ttf", 48)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self._prep_msg(msg)
        
    def _prep_msg(self, msg):
        """Визуализация кнопки"""

        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        """Отображение кнопки"""
        #self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, (self.x, self.y))