import pygame

class Settings:

    """Класс настроек"""

    def __init__(self):

        """Инициализация настроек"""

        self.screen_width = 1200

        self.screen_height = 750

        self.bg_color = (230, 230, 230)

        self.bg_img = pygame.image.load("images/bgs/bgOne.png")

        self.bg_sound = pygame.mixer.music.load("sound/bg_music/bg_sound.mp3")

        self.ship_speed = 1.5

        self.ship_limit = 3

        self.alien_speed = 1.0

        self.alien_sound = pygame.mixer.Sound("sound/aliens/dead_alien.wav")

        self.anim = False

        self.fleet_drop_speed = 10

        self.fleet_direction = 1

        self.bullet_speed = 1.5

        self.bullet_width = 3

        self.bullet_height = 15

        self.bullet_color = (60, 60, 60)

        self.bullets_allowed = 3

        self.bullet_sound = pygame.mixer.Sound("sound/ship/laser_shoot.wav")

        self.speedup_scale = 1.1

        self.score_scale = 1.5

        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """Инициализация динамичной настройки игры"""

        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        self.alien_points = 50
        self.fleet_direction = 1
    
    def increase_speed(self):
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)

    def increase_speed(self):
        """Инициализация ускорения"""

        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)