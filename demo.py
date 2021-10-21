import pygame
from pygame.locals import *

pygame.init()

screen_width = 800
screen_height = 600

#FPS
fpsclock = pygame.time.Clock()
FPS = 60

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Demo Game")

#load images
bGround1 = pygame.image.load("image/bg1.png")


tile_size = 40

#layout
def draw_layout():
	for line in range(0,20):
		pygame.draw.line(screen,(255,255,255),(0,line * tile_size),(screen_width,line * tile_size))
		pygame.draw.line(screen,(255,255,255),(line * tile_size,0),(line * tile_size,screen_height))

#draw land
class World():
	def __init__(self,data):
		self.tile_list = []

		#load images
		woodBlock = pygame.image.load("image/woodBlock.png")
		key = pygame.image.load("image/key.png")

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

				col_count+=1
			row_count+=1

	def drawWorld(self):
		for tile in self.tile_list:
			screen.blit(tile[0] ,tile[1])


world_data = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0],
[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

#instance world
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

	def update(self):
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

		#update player
		self.rect.x += dx				
		self.rect.y += dy

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
		pygame.draw.rect(screen,(0,0,0),self.rect,2)
		

#instance player
player = Player(tile_size*2,screen_height-(tile_size*4))

#Main
run = True
while run:
	fpsclock.tick(FPS)
	screen.blit(bGround1,(0,0))
	draw_layout()
	world.drawWorld()
	player.update()
	pygame.draw.line(screen,(0,0,0),(0,520),(800,520))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	pygame.display.update()
	

pygame.quit()