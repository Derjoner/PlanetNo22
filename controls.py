import pygame, sys
from bullet import Bullet
from monstro import Monstro
import time

def events(screen, gun, bullets):

	"""обработка событий"""

	for event in pygame.event.get():
		# Выход из игры
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			# Вправо
			if event.key == pygame.K_d:
				gun.mright = True
			# Влево
			elif event.key == pygame.K_a:
				gun.mleft = True
				# Стрельба
			elif event.key == pygame.K_SPACE:
				new_bullet = Bullet(screen, gun)
				bullets.add(new_bullet)
		elif event.type == pygame.KEYUP:
			# Вправо стоп
			if event.key == pygame.K_d:
				gun.mright = False
			# Влево стоп
			elif event.key == pygame.K_a:
				gun.mleft = False

def update(bg_color, screen, stats, sc, gun, monstros, bullets):

	"""обновление экрана"""

	screen.fill(bg_color)
	sc.show_score()
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	gun.output()
	monstros.draw(screen)
	pygame.display.flip()

def update_bullets(screen, stats, sc, monstros, bullets):

	"""обновление позиции пуль"""

	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	
	# Колизия уничтожения
	colisions = pygame.sprite.groupcollide(bullets, monstros, True, True)
	if colisions:
		for monstors in colisions.values():
			stats.score += 5 * len(monstors)
	sc.image_score()
	check_high_score(stats, sc)
	sc.image_lifes()

	if len(monstros) == 0:
		bullets.empty()
		create_army(screen, monstros)


def create_army(screen, monstros):

	"""Cоздание монстров"""

	monstro = Monstro(screen)
	monstro_width = monstro.rect.width
	number_monstro_x = int((700 - 2 * monstro_width) / monstro_width)
	monstro_height = monstro.rect.height
	number_monstro_y = int((800 - 64 - 2 * monstro_height) / monstro_height)

	# Создание монстров
	for row_number in range(number_monstro_y - 14):
		for monstro_number in range(number_monstro_x - 4):
			monstro = Monstro(screen)
			monstro.x = monstro_width + monstro_width * monstro_number
			monstro.y = monstro_height + monstro_height * row_number
			monstro.rect.x = monstro.x + 100
			monstro.rect.y = monstro.rect.height + 2 * monstro.rect.height * row_number
			monstros.add(monstro)

def update_monstros(stats, screen, sc, gun, monstros, bullets):

	"""обновление пришельцев"""

	monstros.update()
	if pygame.sprite.spritecollideany(gun, monstros):
		gun_kill(stats, screen, sc, gun, monstros, bullets)
	monstors_check(stats, screen, sc, gun, monstros, bullets)

def gun_kill(stats, screen, sc, gun, monstros, bullets):

	"""Столкновение космобума и пришельцев"""
	if stats.guns_life > 0:
		stats.guns_life -= 1
		sc.image_lifes()
		monstros.empty()
		bullets.empty()
		create_army(screen, monstros)
		gun.create_gun()
		time.sleep(1)
	else:
		stats.run_game = False
		sys.exit()

def monstors_check(stats, screen, sc, gun, monstros, bullets):

	"""Проверка пришельцев на край карты"""

	screen_rect = screen.get_rect()
	for monstro in monstros.sprites():
		if monstro.rect.bottom > screen_rect.bottom:
			gun_kill(stats, screen, sc, gun, monstros, bullets)
			break

def check_high_score(stats, sc):

	"""Проверка новых рекордов"""

	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sc.image_high_score()
		with open('highscore.txt', 'w') as f:
			f.write(str(stats.high_score))