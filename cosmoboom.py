import pygame
from pygame.sprite import Sprite

class Gun(Sprite):

	"Класс космобума"

	def __init__(self, screen):

		""" инициализация космобума """

		super(Gun, self).__init__()
		
		#Определение экрана и космобума
		self.screen = screen
		self.image = pygame.image.load('images/cosmoboom.png')

		#Получение графических космобума и экрана в качестве прямоугольников
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		#Центр космобума
		self.rect.centerx = self.screen_rect.centerx

		#Изменение значений движения космобума в формат дробных чисел
		self.center = float(self.rect.centerx)

		#Низ космобума
		self.rect.bottom = self.screen_rect.bottom - 10

		#Движение космобума
		self.mright = False
		self.mleft = False

	def output(self):

		"""Отображение космобума"""

		self.screen.blit(self.image, self.rect)
	
	def update_gun(self):

		"""Обновление позиции космобума"""

		if self.mright and self.rect.right < self.screen_rect.right:
			self.center += 0.5
		elif self.mleft and self.rect.left > 0:
			self.center -= 0.5
		
		self.rect.centerx = self.center

	def create_gun(self):
		"""Размещение космобума"""
		self.center = self.screen_rect.centerx