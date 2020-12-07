import pygame
from os import path

WIDTH = 800
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon")
clock = pygame.time.Clock()

img_dir = path.join(path.dirname(__file__), 'king')
background = pygame.image.load(path.join(img_dir, 'test.png')).convert()
background_rect = background.get_rect()
background = pygame.transform.scale(background, (WIDTH, HEIGHT)) 


def set_sprite(sprite_list, number, name, color, width, height):  # только для png с нумерацией в папке king
#number - количество
    for i in range(1, number+1):
        filename = (name + '{}.png').format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(color)
        img = pygame.transform.scale(img, (width, height))
        sprite_list.append(img)    
    
    
    

fire_animation = []
'''for i in range(1, 5):
    filename = 'fire{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img = pygame.transform.scale(img, (200, 40))
    fire_animation.append(img)'''

set_sprite(fire_animation, 4, 'fire', BLACK, 200, 40) 





class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 60
        self.height = 85
        self.blocksize = 37        
        
        self.walk_animation = []
        for i in range(1, 19):
            filename = '{}.png'.format(i)
            img = pygame.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey(BLACK)
            img = pygame.transform.scale(img, (self.width, self.height))
            self.walk_animation.append(img)        
        
        self.image = self.walk_animation[0]
        self.rect = self.image.get_rect()       


        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - self.blocksize
        self.speedx = 0
        self.speedy = 0
        self.maxspeed = 4
        self.speedjump = 25
        self.gravity = 2
        

        
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 45
        

    def timer(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == 18:
                self.frame = 0
            else:
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center
                
    def collision(self):
        if (self.rect.right > WIDTH - self.blocksize) and (self.rect.top < HEIGHT-(self.blocksize + self.height)):
            self.rect.right = WIDTH - self.blocksize
        if (self.rect.left < self.blocksize) and (self.rect.top < HEIGHT-(self.blocksize + self.height)):
            self.rect.left = self.blocksize
        if self.rect.top < self.blocksize:
            self.rect.top = self.blocksize
        if self.rect.bottom > HEIGHT - self.blocksize:
            self.rect.bottom = HEIGHT - self.blocksize
        
    def update(self):
        keystate = pygame.key.get_pressed()
             
        self.rect.y -= self.speedy
        self.speedy -= self.gravity
        
        if (keystate[pygame.K_j]) and (self.rect.bottom >= HEIGHT - self.blocksize) :
            self.speedy = self.speedjump
            
        if keystate[pygame.K_a]:
            self.speedx = -1 * self.maxspeed
            self.rect.x += self.speedx
            self.timer()
            self.image = pygame.transform.flip(self.walk_animation[self.frame], True, False)
    
        if keystate[pygame.K_d]:
            self.speedx = self.maxspeed
            self.rect.x += self.speedx
            self.timer()
            self.image = self.walk_animation[self.frame]
        self.collision()    
        
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        bullets.add(bullet)







class Fire(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = fire_animation[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  
        self.duration = 200
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == self.duration:
                self.kill()
            else:
                center = self.rect.center
                self.image = fire_animation[self.frame % 4]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 10

    def update(self):
        self.rect.x += self.speedx
        if self.rect.bottom < 0:
            self.kill()
            

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
fire = Fire((player.rect.bottomright[0], player.rect.bottomright[1] - 22))     # НЕЗАБЫТЬ поставить вместо 22 параметр
all_sprites.add(fire)

game_over = False
while not game_over:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()


    all_sprites.update()
    screen.fill(BLUE)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()       