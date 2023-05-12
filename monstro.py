import pygame

class Monstro(pygame.sprite.Sprite):
	"""Класс пришельца"""

	def __init__(self, screen):

		"""Инициализация класса"""

		super(Monstro, self).__init__()
		self.screen = screen
		self.image = pygame.image.load('images/monstro1.png')
		self.rect = self.image.get_rect()
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)

	def draw(self):

		"""Отрисовка пришельца"""

		self.screen.blit(self.image, self.rect)

	def update(self):
		
		"""Перемещение пришельца"""

		self.y += 0.1
		self.rect.y = self.y
