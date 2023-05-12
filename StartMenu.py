import pygame

class StartMenu():
	def __init__(self):
		self._options_surfaces = []
		self._callback = []
		self._current_option_index = 0
		self.font = pygame.font.SysFont("Open Sans", 50)
	
	def append_option(self, option, callback):
		self._options_surfaces.append(self.font.render(option, True, (246, 214, 189)))
		self._callback.append(callback)

	def switch(self, direction):
		self._current_option_index = max(0, min(self._current_option_index + direction, len(self._options_surfaces) - 1))

	def select(self):
		self._callback[self._current_option_index]()

	def draw_sm(self, surf, x, y, option_y_padding):
		for i, option in enumerate(self._options_surfaces):
			option_rect = option.get_rect()
			option_rect.topleft = (x, y + i * option_y_padding)
			if i == self._current_option_index:
				pygame.draw.rect(surf, (0, 100, 0), option_rect)
			surf.blit(option, option_rect)