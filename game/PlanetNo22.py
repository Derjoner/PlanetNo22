import sys
import pygame
from time import sleep
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from button_quit import Button_quit
from alien import Alien
from pygame import mixer

class AlienInvasion:

    """Общий класс по управлению игровыми активами и поведением."""

    def __init__(self):

        """Инициализация игры и создание игровых ресурсов."""

        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        self.settings.screen_width = self.screen.get_rect().width

        self.settings.screen_height = self.screen.get_rect().height

        self.stats = GameStats(self)

        self.sb = Scoreboard(self)

        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.clock = pygame.time.Clock()
        self.FPS = 100

        self.play_button = Button(self, "Играть")
        self.quit_button = Button_quit(self, "Выход", 530, 500)

        pygame.display.set_caption("Planet No.22")

    def _check_events(self):

        """Реакции на нажатия"""

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                sys.exit()

            elif event.type == pygame.KEYDOWN:

                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:

                self._check_keyup_events(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_quit_button(mouse_pos)

    def _check_keydown_events(self, event):

        """Реакция на клавиши"""

        if event.key == pygame.K_d:

            self.ship.moving_right = True

        elif event.key == pygame.K_a:

            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:

            sys.exit()
        
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):

        """Реакция на клавиши"""

        if event.key == pygame.K_d:

            self.ship.moving_right = False

        elif event.key == pygame.K_a:

            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Реакция на мышь"""

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active:
            self.settings.bg_sound
            mixer.music.play(-1)
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)

    def _check_quit_button(self, mouse_pos):
        button_click = self.quit_button.rect.collidepoint(mouse_pos)
        if button_click:
            sys.exit()

    def _fire_bullet(self):
        """Создание пуль"""
        if len(self.bullets) < self.settings.bullets_allowed and self.stats.game_active:
            self.settings.bullet_sound.play()
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_bullet_alien_collisions(self):
        """Реакция на столкновение с врагом"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    self.settings.alien_sound.play()
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _update_bullets(self):
        """Обновление пуль"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _ship_hit(self):
        """Реакция на удар по кораблю"""

        if self.stats.ships_left > 0:

            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mixer.music.pause()
            pygame.mouse.set_visible(True)

        sleep(0.5)

    def _check_aliens_bottom(self):
        """Проверка на столкновение с экраном врагов"""

        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """Изменение движения врагов"""

        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        """Реакция на врага"""

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _create_alien(self, alien_number, row_number):
        """Создание одного врага в ряду"""

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 3 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _create_fleet(self):
        """Cоздание армии врагов"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (10 * alien_width)
        number_aliens_x = available_space_x // (3 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (4 * alien_height) - ship_height)

        number_rows = available_space_y // (6 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _update_aliens(self):
        """Обновление врага"""

        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            self._check_aliens_bottom()

    def _update_screen(self):

        """Обновление экрана"""

        # self.screen.fill(self.settings.bg_color)

        pygame.transform.scale(self.settings.bg_img.convert(), (1200, 750), self.screen)

        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.stats.game_active:
            self.screen.fill((0, 0, 0))
            self.play_button.draw_button()
            self.screen.blit(pygame.font.Font('fonts/Undertale-Battle-Font.ttf', 65).render("Планета No.22", False, (255, 255, 255)), (350, 150))
            self.quit_button.draw_button()

        pygame.display.update()

    def run_game(self):

        """Запуск основного цикла игры."""

        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(self.FPS)



if __name__ == '__main__':

    # Создание экземпляра игры и её запуск

    ai = AlienInvasion()

    ai.run_game()