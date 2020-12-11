import pygame
from settings import *
from weapon import *


class Player(pygame.sprite.Sprite):
    def __init__(self, upgrade):
        pygame.sprite.Sprite.__init__(self)
        self.width = 60
        self.height = 85
        self.blocksize = 37  
        self.number = 8
        
        self.walk_animation = []
        set_sprite(self.walk_animation, self.number, 'wizard', BLACK, self.width, self.height)             
        self.image = self.walk_animation[0]
        self.rect = self.image.get_rect()       

        self.rect.centerx = WIDTH / 4
        self.rect.bottom = HEIGHT - self.blocksize

        self.speedx = 0
        self.speedy = 0
        self.maxspeed = 4 + upgrade[3]
        self.speedjump = 25 + upgrade[2]
        self.gravity = 2
        self.weapon = 1
        
        self.fireball_cost = 15
        self.fire_cost = 30
        self.manaspeed = 0.1
        self.maxhealth = 100 + upgrade[0]
        self.health = self.maxhealth 
        self.maxmana = 100 + upgrade[1]
        self.mana = self.maxmana  
        self.point = 0
        
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 45
               
    def timer(self):
        '''
        Вспомогательный метод, который регулирует частоту смены спрайтов

        Returns None.
        -------
        '''
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == self.number:
                self.frame = 0
            else:
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center
                
    def collision(self):
        '''
        Вспомогательный метод, отслеживающий столкновения игрока со стенами

        Returns None.
        -------
        '''
        if (self.rect.right > WIDTH - self.blocksize) and (self.rect.top < HEIGHT-(self.blocksize + self.height)):
            self.rect.right = WIDTH - self.blocksize
        if (self.rect.left < self.blocksize) and (self.rect.top < HEIGHT-(self.blocksize + self.height)):
            self.rect.left = self.blocksize
        if self.rect.top < self.blocksize:
            self.rect.top = self.blocksize
        if self.rect.bottom > HEIGHT - self.blocksize:
            self.rect.bottom = HEIGHT - self.blocksize
                
    def update(self, mouse_posx):
        '''
        Метод отвечает за проверку нажатия клавиш, т.е. за прыжки,
        перемещение, передвижение игрока и смену спрайтов

        Returns None.
        -------
        '''
        keystate = pygame.key.get_pressed()
        self.speedx = 0
        
        if self.mana < self.maxmana:
            self.mana += self.manaspeed
            
        if abs(self.speedy) <= self.speedjump: 
            self.rect.y -= self.speedy                                                   #### Для двойного прыжка это не пойдет
            self.speedy -= self.gravity   
        
        if (keystate[pygame.K_SPACE]) and (self.rect.bottom >= HEIGHT - self.blocksize) :
            self.speedy = self.speedjump
            
        if keystate[pygame.K_a]:
            self.speedx = -1 * self.maxspeed
            self.rect.x += self.speedx
            self.timer()
            
        if keystate[pygame.K_d]:
            self.speedx = self.maxspeed
            self.rect.x += self.speedx
            self.timer()
            
        if mouse_posx >= self.rect.x:
            self.image = self.walk_animation[self.frame]
        if mouse_posx < self.rect.x:
            self.image = pygame.transform.flip(self.walk_animation[self.frame], True, False)
        self.collision() 

            
    def shoot(self, mouse_pos):
        if self.weapon == 1:
            if self.mana >= self.fireball_cost:
                self.mana -= self.fireball_cost
                fireball = Fireball(self.rect.centerx, (self.rect.center[1] + self.rect.bottom)/2, mouse_pos[0], mouse_pos[1], self.blocksize)
                fireballs_sprites.add(fireball) 
        if self.weapon == 2:
            if self.mana >= self.fire_cost:
                self.mana -= self.fire_cost
                fire = Fire((self.rect.center[0], self.rect.bottomright[1] - 22))                 
                fires_sprites.add(fire)

