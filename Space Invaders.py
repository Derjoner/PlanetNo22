import pygame, controls, sys
from cosmoboom import Gun
from pygame.sprite import Group
from stats import Stats
from scores import Scores
from StartMenu import StartMenu

def Run():

	pygame.init()
	screen = pygame.display.set_mode((700, 800))
	pygame.display.set_caption("Космобум")
	bg_color =  (0, 0 , 0)
	gun = Gun(screen)
	bullets = Group()
	monstros = Group()
	controls.create_army(screen, monstros)
	stats = Stats()
	sc = Scores(screen, stats)

	while True:
		controls.events(screen, gun, bullets)
		if stats.run_game:
			gun.update_gun()
			controls.update(bg_color, screen, stats, sc, gun, monstros, bullets)
			controls.update_bullets(screen, stats, sc, monstros, bullets)
			controls.update_monstros(stats, screen, sc, gun, monstros, bullets)

def Start():
	pygame.init()
	size = (700, 800)
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("Космобум")
	startmenu = StartMenu()
	startmenu.append_option("Start", Run)
	startmenu.append_option("Quit", quit)
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w:
					startmenu.switch(-1)
				elif event.key == pygame.K_s:
					startmenu.switch(1)
				elif event.key == pygame.K_SPACE:
					startmenu.select()
		screen.fill((0, 0, 0))

		startmenu.draw_sm(screen, 100, 100, 75)

		pygame.display.flip()
	quit()

"""Сцены"""
current_scene = None
def switch_scene(scene):
		global current_scene
		current_scene = scene

switch_scene(Start)
while current_scene is not None:
	current_scene()