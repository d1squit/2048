from random import randint
from pygame import *

init()
font.init()

window_size = (475, 475)
window = display.set_mode(window_size, NOFRAME)
display.set_caption('2048')

font_object = font.SysFont('Verdana', 58)
win = font_object.render('You win!', True, (255, 255, 255))
lose = font_object.render('You lose!', True, (255, 255, 255))

background = image.load('tiles/background.png')

clock = time.Clock()
fps = 60
play = True
clickable = True
end_game_lose = False
end_game_win = False

score = 0

def create_rand_tile ():
	counter = 0
	for row in tiles:
		for tile in row:
			if tile: counter += 1
	if counter == 16: return False

	x, y, num = randint(0, 3), randint(0, 3), randint(0, 9)
	while tiles[x][y] != 0: x, y = randint(0, 3), randint(0, 3)

	if num: tiles[x][y] = 2
	else: tiles[x][y] = 4


def left (matrix):
	def clear_left ():
		for x, row in enumerate(matrix):
			for y in range(1, len(row)):
				if not row[y - 1] and sum(row[y:]):
					matrix[x][y - 1] = matrix[x][y]
					matrix[x][y] = 0

		for x, row in enumerate(matrix):
			for y in range(1, len(row)):
				if not row[y - 1] and sum(row[y:]):
					clear_left()		

	clear_left()
	

	for x, row in enumerate(matrix):
		for y in range(len(row) - 1):
			if row[y] == row[y + 1] and row[y] and row[y + 1]:
				matrix[x][y + 1] = 0
				matrix[x][y] *= 2
				global score
				score += matrix[x][y]

	clear_left()
	return matrix

def right (matrix):
	for row in matrix:
		row.reverse()

	left(matrix)

	for row in matrix:
		row.reverse()
	return matrix

def up (matrix):
	_tiles = matrix.copy()

	rotated = list(zip(*_tiles))[::-1]
	for row in range(len(rotated)): rotated[row] = list(rotated[row])

	left(rotated)
	_tiles = list(zip(*rotated[::-1]))
	for row in range(len(_tiles)): _tiles[row] = list(_tiles[row])
	return _tiles

def down (matrix):
	_tiles = matrix.copy()

	rotated = list(zip(*_tiles[::-1]))
	for row in range(len(rotated)): rotated[row] = list(rotated[row])

	left(rotated)
	_tiles = list(zip(*rotated))[::-1]
	for row in range(len(_tiles)): _tiles[row] = list(_tiles[row])
	return _tiles


def init_board ():
	global tiles, clickable, end_game_win, end_game_lose, score
	clickable = True
	end_game_win = False
	end_game_lose = False
	score = 0

	tiles = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
	create_rand_tile()
	create_rand_tile()

def exit ():
	global play
	play = False

def end_game(text):
	global clickable
	clickable = False

	alpha = Surface(window_size)
	alpha.set_alpha(128)
	alpha.fill((230, 230, 50))
	window.blit(alpha, (0, 0))
	
	exit_button.draw()
	again_button.draw()

	score_text = font_object.render('Score is ' + str(score), True, (255, 255, 255))

	text_rect = text.get_rect(center=(window_size[0] / 2, window_size[0] / 2 - 50))
	score_rect = score_text.get_rect(center=(window_size[0] / 2, window_size[0] / 2 + 25))
	window.blit(text, text_rect)
	window.blit(score_text, score_rect)
	display.update()

def check_empty (board):
	zero = 0

	for row in board:
		for tile in row:
			if tile == 0: zero += 1

	return not zero

init_board()



class GameButton:
	def __init__ (self, pos: tuple, size: tuple, text: str):
		self.event = event
		self.text = text
		button_surface = Surface(size)
		self.button_surface_rect = button_surface.get_rect(center=pos)
		

	def draw (self):
		draw.rect(window, (115, 100, 80), tuple(self.button_surface_rect), border_radius=7)

		font_object = font.SysFont('Verdana', 22)
		text_object = font_object.render(self.text, True, (255, 255, 255))
		text_rect = text_object.get_rect(center=(self.button_surface_rect.width / 2 + self.button_surface_rect.x, self.button_surface_rect.height / 2 + self.button_surface_rect.y))
		window.blit(text_object, text_rect)


while play:
	window.blit(background, (0, 0))

	exit_button = GameButton((window_size[0] / 2 - 100, window_size[0] / 2 + 100), (150, 50), "Keep going")
	again_button = GameButton((window_size[0] / 2 + 100, window_size[0] / 2 + 100), (150, 50), "Try again")

	for e in event.get():
		if e.type == QUIT:
			play = False
		if e.type == KEYDOWN and clickable:
			if e.key == K_a or e.key == K_LEFT:
				tiles = left(tiles)
				create_rand_tile()
			if e.key == K_d or e.key == K_RIGHT:
				tiles = right(tiles)
				create_rand_tile()
			if e.key == K_w or e.key == K_UP:
				tiles = up(tiles)
				create_rand_tile()
			if e.key == K_s or e.key == K_DOWN:
				tiles = down(tiles)
				create_rand_tile()
		if e.type == MOUSEBUTTONDOWN and not clickable:
			mouse_pressed = mouse.get_pressed()
			if mouse_pressed[0]:
				if again_button.button_surface_rect.collidepoint(mouse.get_pos()):
					init_board()
				if exit_button.button_surface_rect.collidepoint(mouse.get_pos()):
					exit()

	for y, row in enumerate(tiles):
		for x, tile in enumerate(row):
			window.blit(image.load('tiles/' + str(tile) + '.svg'), (x * 115 + 15, y * 115 + 15))

	for row in tiles:
		for tile in row:
			if tile == 2048:
				end_game_win = True

	if end_game_lose: end_game(lose)
	if end_game_win: end_game(win)

	if check_empty(tiles) and clickable:
		if check_empty(left(tiles)) and check_empty(right(tiles)) and check_empty(up(tiles)) and check_empty(down(tiles)):
			end_game_lose = True
			end_game(lose)

	display.update()
	clock.tick(fps)