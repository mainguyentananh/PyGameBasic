import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path

pygame.mixer.pre_init(44100,-16,2,512)
mixer.init()
pygame.init()

BLUE = (0 ,0 , 255)


#define map
num = 1
max_num = 3

#define door and state game
game_over = 0
oDoor = 0

#define menu
main_menu = -1

#FPS
fpsclock = pygame.time.Clock()
FPS = 60

#Config 
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Demo Game")
pygame.mixer.music.load('sound/start.mp3')
pygame.mixer.music.play(-1,0,5000)


#load images
bGround1 = pygame.image.load("image/bg1.png")
bGround2 = pygame.image.load("image/bg2.png")
bGround3 = pygame.image.load("image/bg3.png")
start_img = pygame.image.load("image/start.png")
restart_img = pygame.image.load("image/restart.png")
win = pygame.image.load("image/win.jpg")

#load sound
sJump = pygame.mixer.Sound("sound/jump.wav")
sJump.set_volume(0.5)

sCoin = pygame.mixer.Sound("sound/coin.wav")
sCoin.set_volume(0.5)

sDead = pygame.mixer.Sound("sound/Dead.wav")
sDead.set_volume(0.5)

sNext = pygame.mixer.Sound("sound/next_map.wav")
sNext.set_volume(0.5)



tile_size = 40


def next_map(num):
	player.reset(tile_size, screen_height/2)
	key_grp.empty()
	door_grp.empty()
	lava_grp.empty()
	enemy_grp.empty()

	#load in level data and create world
	if path.exists(f'map{num}.pickle'):
		pickle_in = open(f'map{num}.pickle', 'rb')
		world_data = pickle.load(pickle_in)
	world = World(world_data)

	return world


#layout
def draw_layout():
	for line in range(0,20):
		pygame.draw.line(screen,(255,255,255),(0,line * tile_size),(screen_width,line * tile_size))
		pygame.draw.line(screen,(255,255,255),(line * tile_size,0),(line * tile_size,screen_height))

#draw world
class World():
	def __init__(self,data):
		self.tile_list = []
		#load images
		woodBlock = pygame.image.load("image/woodBlock.png")
		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(woodBlock,(tile_size,tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					key = Key(col_count * tile_size,row_count * tile_size)
					key_grp.add(key)
				if tile == 3:
					door = Door(col_count * tile_size,row_count * tile_size)
					door_grp.add(door)
				if tile == 4:
					lava = Lava(col_count * tile_size,row_count * tile_size)
					lava_grp.add(lava)
				if tile == 5:
					enemy = Enemy(col_count * tile_size,row_count * tile_size)
					enemy_grp.add(enemy)
				col_count+=1
			row_count+=1

	def drawWorld(self):
		for tile in self.tile_list:
			screen.blit(tile[0] ,tile[1])


class Door(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load("image/door.png")
		self.image = pygame.transform.scale(img,(55,90))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Key(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load("image/key.png")
		self.image = pygame.transform.scale(img,(30,30))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('image/lava.png')
		self.image = pygame.transform.scale(img, (40,40))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('image/enemy.png')
		self.image = pygame.transform.scale(img,(50,50))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if self.move_counter > 100:
			self.move_direction *= -1
			self.move_counter *= -1
			if self.move_direction < 0:
				self.image = pygame.transform.flip(self.image,True,False)
			else:
				self.image = pygame.transform.flip(self.image,True,False)


door_grp = pygame.sprite.Group()
key_grp = pygame.sprite.Group()
lava_grp = pygame.sprite.Group()
enemy_grp = pygame.sprite.Group()

#instance world
if path.exists(f'map{num}.pickle'):
	pickle_in = open(f'map{num}.pickle', 'rb')
	world_data = pickle.load(pickle_in)

world = World(world_data)


class Player():
	def __init__(self,x,y):
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.count = 0
		for num in range(1,5):  
			img = pygame.image.load(f"image/guy{num}.png")
			img_r = pygame.transform.scale(img,(40,80))
			img_l = pygame.transform.flip(img_r,True,False)
			self.images_right.append(img_r)
			self.images_left.append(img_l)
		
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.rect.x = x
		self.rect.y = y
		self.vel_y = 0
		self.jump = False
		self.direct = 0
		self.check_jump = 0
		

	def oDoor(self,oDoor):
		if pygame.sprite.spritecollide(self,key_grp,True):
			oDoor += 1
			sCoin.play()
		return oDoor

	def update(self,game_over):
		dx = 0  
		dy = 0
		walk_col = 15
		
		
		#get keypresses
		keyPress = pygame.key.get_pressed()

		#Nếu thiết lập khối đất làm nền thì khỏi cần cái này, Khi nào chạm ngưỡng nền mới được nhảy tiếp
		if self.rect.bottom - 520 == 0:
			self.check_jump = 0

		#Reset state jump , khi k có event space thì mới có thể space tiếp , tránh trường hợp giữ space nhân vật bay hoài
		if keyPress[pygame.K_SPACE] == False:
			self.jump = False


		if keyPress[pygame.K_SPACE] and self.jump == False and self.check_jump == 0:
			sJump.play()
			self.vel_y = -15 #2,5 ô top 455 - jump(335) = 120 / 40 (1 ô) = >> 2,5 ô , tính từ recttop
			self.jump = True
			self.check_jump = 1
			
		if keyPress[pygame.K_LEFT]:
			dx -= 5
			self.count += 5
			self.direct = -1

		if keyPress[pygame.K_RIGHT]:
			dx += 5
			self.count += 5
			self.direct = 1

		#stop 
		if keyPress[pygame.K_LEFT] == False and keyPress[pygame.K_RIGHT] == False:
			self.count = 0
			self.index = 0
			if self.direct == 1:
				self.image = self.images_right[self.index]
			if self.direct == -1:
				self.image = self.images_left[self.index]

		#handle animation 
		if self.count > walk_col:
			self.count = 0
			self.index += 1
			if self.index >= len(self.images_right):
				self.index = 0
			if self.direct == 1:
				self.image = self.images_right[self.index]
			if self.direct == -1:
				self.image = self.images_left[self.index]
		

		#add gravity
		self.vel_y += 1
		if self.vel_y > 15:
			self.vel_y = 15

		dy += self.vel_y



		#check for collision
		for tile in world.tile_list:
			#check x 
			if tile[1].colliderect(self.rect.x + dx,self.rect.y,self.width,self.height):
				dx = 0 #Khong di xuyen qua
			
			#check y 
			if tile[1].colliderect(self.rect.x,self.rect.y + dy,self.width,self.height):
				#check jump
				if self.vel_y < 0:
					dy = tile[1].bottom - self.rect.top
					self.vel_y = 0
				elif self.vel_y >= 0:
					dy = tile[1].top - self.rect.bottom
					self.vel_y = 0
				#Khi nào có va chạm xong chạm vật mới tiếp tục nhảy tiếp
				self.check_jump = 0


		#check for collision with exit
		# Show Door and Next Map
		if oDoor >=3:
			if pygame.sprite.spritecollide(self, door_grp, False):
				game_over = 1
				sNext.play()

		if pygame.sprite.spritecollide(self,lava_grp,False):
			game_over = -1
			sDead.play()


		if pygame.sprite.spritecollide(self,enemy_grp,False):
			game_over = -1
			sDead.play()

		#update player
		self.rect.x += dx				
		self.rect.y += dy

		if game_over == -1:
			self.rect.y = -200

		# print(dy)
		# print(self.rect.top)

		#limited
		if self.rect.bottom > 520:
			self.rect.bottom = 520
			
		if self.rect.left < 0:
			self.rect.left = 0

		if self.rect.right > 800:
			self.rect.right = 800

		screen.blit(self.image,self.rect)
		return game_over

	def reset(self,x,y):
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.count = 0
		for num in range(1,5):  
			img = pygame.image.load(f"image/guy{num}.png")
			img_r = pygame.transform.scale(img,(40,80))
			img_l = pygame.transform.flip(img_r,True,False)
			self.images_right.append(img_r)
			self.images_left.append(img_l)
		
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.rect.x = x
		self.rect.y = y
		self.vel_y = 0
		self.jump = False
		self.direct = 0
		self.check_jump = 0
		
		

#instance player
# player = Player(tile_size*2,screen_height-(tile_size*4))

player = Player(tile_size*2,screen_height/2)

class Button():
	def __init__(self, x, y, image):
		self.image = pygame.transform.scale(image,(120,80))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False


		#draw button
		screen.blit(self.image, self.rect)

		return action

start_button = Button((screen_width / 2) - 40, (screen_height / 2) - 120, start_img)
restart_button = Button((screen_width / 2) - 40, (screen_height / 2) - 120, restart_img)

#Text Win
font = pygame.font.Font("OpenSans-Bold.ttf",40)
text = font.render("PHÁ ĐẢO",True,BLUE)


#Main
run = True
while run:
	fpsclock.tick(FPS)

	if num == 1:
		screen.blit(bGround1,(0,0))
	if num ==2:
		screen.blit(bGround2,(0,0))
	if num ==3:
		screen.blit(bGround3,(0,0))
	
	world.drawWorld()

	if main_menu == -1:
		if start_button.draw():
			main_menu = 0
			pygame.mixer.music.stop()

	if main_menu == 0:
		game_over = player.update(game_over)
		oDoor = player.oDoor(oDoor)
		
		#Show Door
		if oDoor >=3:		
			door_grp.draw(screen)
		key_grp.draw(screen)
		lava_grp.draw(screen)
		enemy_grp.draw(screen)
		enemy_grp.update()
		
		if game_over == -1:
			if restart_button.draw():
				num = 1
				world = next_map(num)
				game_over = 0
				oDoor = 0

		if game_over == 1:
			num += 1
			if num <= max_num:
				world = next_map(num)
				game_over = 0
			else:
				main_menu = 1
			oDoor = 0
	if main_menu == 1:
		screen.blit(win,(0,0))
		screen.blit(text,((screen_width / 2) - 60, (screen_height / 2) - 200))
		if restart_button.draw():
			num = 1
			world = next_map(num)
			game_over = 0
			oDoor = 0

	#draw_layout()
	#pygame.draw.line(screen,(0,0,0),(0,520),(800,520))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	pygame.display.update()
	

pygame.quit()

