import pygame

class Bullet(pygame.sprite.Sprite):

	"""Класс пули"""

	def __init__(self, screen, gun):

		"""Создание пули в позиции космобума"""

		super(Bullet, self).__init__()
		self.screen = screen

		# Параметры пушки
		self.rect = pygame.Rect(0, 0, 2, 12)
		self.color = (246, 214, 189)
		self.speed = 1.5
		self.rect.centerx = gun.rect.centerx
		self.rect.top = gun.rect.top
		self.y = float(self.rect.y)
	
	def update(self):

		"""Перемещение пули вверх"""

		self.y -= self.speed
		self.rect.y = self.y

	def draw_bullet(self):

		"""Отрисовка пули"""

		pygame.draw.rect(self.screen, self.color, self.rect)