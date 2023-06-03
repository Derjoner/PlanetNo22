import pygame
from pygame.sprite import Sprite
import random

class Alien(Sprite):
    """Класс инопланетянина"""

    def __init__(self, ai_game):
        """Инициализация врага"""

        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()
        self.zeta_img = [pygame.image.load('images/aliens/zeta/zetaL.png'), pygame.image.load('images/aliens/zeta/zetaR.png')]
        self.zeta_anim = [pygame.image.load(f'images/aliens/zeta/zetaBoom{i}.png') for i in range(0, 7)]
        self.image = self.zeta_img[1]
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.bott = True

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        """Возвращение значения, при конце экрана"""
        sea = 200
        screen_rect = self.screen.get_rect()
        if self.rect.right >= (screen_rect.right - sea) or self.rect.left <= sea:
            return True

    def update(self):
        """Движение врага"""
        if self.settings.fleet_direction > 0:
            self.image = self.zeta_img[1]
        elif self.settings.fleet_direction < 0:
            self.image = self.zeta_img[0]
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x + 200
        if self.bott:
            self.rect.y += 35
            self.bott = False