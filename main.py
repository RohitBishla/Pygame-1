import pygame 
import os
pygame.font.init()
pygame.mixer.init()

WIDTH,HEIGHT=1360,680
SPACESHIP_HIGHT,SPACESHIP_WIDTH=65,75

Health_font=pygame.font.SysFont('comicsans',50)
winner_font=pygame.font.SysFont("comicsans",80)

VEL=5
Bullet_speed=16
max_bullets=3
bullet_hit_sound=pygame.mixer.Sound(os.path.join("Assets","collide1.wav"))
bullet_fire_sound=pygame.mixer.Sound(os.path.join("Assets","fire.wav"))

Yellow_hit=pygame.USEREVENT + 1
Red_hit=pygame.USEREVENT + 2

BOARDER=pygame.Rect(WIDTH//2-5,0,10,HEIGHT)


WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("BISHlA")

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)

Yellow_splaceship_image=pygame.image.load(os.path.join("Assets","spaceship_yellow.png"))
Yellow_spaceship=pygame.transform.rotate(pygame.transform.scale(Yellow_splaceship_image,(SPACESHIP_WIDTH,SPACESHIP_HIGHT)),90)

Red_splaceship_image=pygame.image.load(os.path.join("Assets","spaceship_red.png"))
Red_spaceship=pygame.transform.rotate(pygame.transform.scale(Red_splaceship_image,(SPACESHIP_WIDTH,SPACESHIP_HIGHT)),270)

SPACE= pygame.transform.scale(pygame.image.load(os.path.join("Assets","space.png")),(WIDTH,HEIGHT))

FPS=60

def draw_Winner_text(Text):
	text=winner_font.render(Text,1,WHITE)
	WIN.blit(text,(WIDTH//2-text.get_width()//2,HEIGHT//2-text.get_height()//2))
	pygame.display.update()
	pygame.time.delay(4000)

def handle_bullets(Yellow_Bullet,Red_Bullet,yellow,red):
	for bullet in Yellow_Bullet:
		bullet.x+=Bullet_speed
		if red.colliderect(bullet):
			pygame.event.post(pygame.event.Event(Red_hit))
			Yellow_Bullet.remove(bullet)
		elif bullet.x>WIDTH:
			Yellow_Bullet.remove(bullet)

	for bullet in Red_Bullet:
		bullet.x-=Bullet_speed
		if yellow.colliderect(bullet):
			pygame.event.post(pygame.event.Event(Yellow_hit))
			Red_Bullet.remove(bullet)
		elif bullet.x<0:
			Red_Bullet.remove(bullet)



def yellow_movement(key_pressed,yellow):
		if key_pressed[pygame.K_a] and yellow.x-VEL>0:#left
			yellow.x-=VEL 
		if key_pressed[pygame.K_d] and yellow.x+VEL+yellow.width-12<BOARDER.x:#left
			yellow.x+=VEL 
		if key_pressed[pygame.K_s] and yellow.y+VEL+yellow.height+11<HEIGHT:#left
			yellow.y+=VEL 
		if key_pressed[pygame.K_w] and yellow.y-VEL-1>0:#left
			yellow.y-=VEL 


def red_movement(key_pressed,red):
		if key_pressed[pygame.K_LEFT] and red.x-VEL>BOARDER.x+10:#left
			red.x-=VEL 
		if key_pressed[pygame.K_RIGHT] and red.x+VEL+red.width-12<WIDTH :#left
			red.x+=VEL 
		if key_pressed[pygame.K_DOWN] and red.y+VEL+red.height+12<HEIGHT:#left
			red.y+=VEL
		if key_pressed[pygame.K_UP] and red.y-VEL >0:#left
			red.y-=VEL 

def draw_window(yellow,red,Yellow_Bullet,Red_Bullet,yellow_health,red_health):
	WIN.blit(SPACE,(0,0))
	pygame.draw.rect(WIN, BLACK, BOARDER)

	yellow_health_text=Health_font.render(str(yellow_health),1,WHITE)
	red_health_text=Health_font.render(str(red_health),1,WHITE)
	WIN.blit(yellow_health_text,(0,0))
	WIN.blit(red_health_text,(WIDTH-red_health_text.get_width(),0))

	WIN.blit(Yellow_spaceship,(yellow.x,yellow.y))
	WIN.blit(Red_spaceship,(red.x,red.y))
	for bullet in Red_Bullet:
		pygame.draw.rect(WIN,RED,bullet)
	for bullet in Yellow_Bullet:
		pygame.draw.rect(WIN,YELLOW,bullet)

	pygame.display.update()

def main():
	red= pygame.Rect(1280,340,SPACESHIP_WIDTH,SPACESHIP_HIGHT)
	yellow= pygame.Rect(10,340,SPACESHIP_WIDTH,SPACESHIP_HIGHT)
	clock=pygame.time.Clock()
	Yellow_Bullet=[]
	Red_Bullet=[]
	red_health=10
	yellow_health=10

	run=True
	while run:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				run=False
				pygame.quit()

			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_TAB and len(Yellow_Bullet)<=max_bullets:
					bullet =pygame.Rect(yellow.x+yellow.width-3,yellow.y+yellow.height//2 -3,12,6)
					Yellow_Bullet.append(bullet)
					bullet_fire_sound.play()

				if event.key==pygame.K_RCTRL and len(Red_Bullet)<=max_bullets:
					bullet=pygame.Rect(red.x-3,red.y+red.height//2,12,6)
					Red_Bullet.append(bullet)
					bullet_fire_sound.play()

			if event.type==Yellow_hit:
				yellow_health-=1
				bullet_hit_sound.play()
			if event.type==Red_hit:
				red_health-=1
				bullet_hit_sound.play()

		winner_text=""
		if yellow_health<=0:
			winner_text="RED WIN!"
		if red_health<=0:
			winner_text="YELLOW WIN!"
		if winner_text!="":
			draw_window(yellow,red, Yellow_Bullet,Red_Bullet,yellow_health,red_health)
			draw_Winner_text(winner_text)
			break

		key_pressed=pygame.key.get_pressed()
		yellow_movement(key_pressed,yellow)
		red_movement(key_pressed,red)

		handle_bullets(Yellow_Bullet,Red_Bullet,yellow,red)

		draw_window(yellow,red, Yellow_Bullet,Red_Bullet,yellow_health,red_health)
		
	main()


if __name__=="__main__":
	main()