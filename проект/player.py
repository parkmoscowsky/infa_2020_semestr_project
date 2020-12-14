import pygame
from settings import set_sprite
from settings import set_dic
from settings import snd_dic
from weapon import Fire, Fireball, Heal_fire


class Player(pygame.sprite.Sprite):
    def __init__(self, upgrade, set_dic, snd_dic):
        '''
        Конструктор класса Player.

        Parameters
        ----------
        upgrade : type list
            Задаёт улучшения, которые должен получать 
            персонаж во время начала игры.
        set_dic : type mapping
            Словарь со всеми основными переменными, 
            который импортируется из settings.

        Returns None.
        -------
        '''
        pygame.sprite.Sprite.__init__(self)
        
        # Из словаря достаем размеры экрана, звуки огня и фаирбола.
        self.WIDTH = set_dic['WIDTH']
        self.HEIGHT = set_dic['HEIGHT']
        self.fire_sound = snd_dic['fire_sound']
        self.fireball_sound = snd_dic['fireball_sound']
        
        # Задаем размеры и количество спрайтов игрока, 
        # размеры квадратного блока.
        self.width = 60
        self.height = 85
        self.number = 8
        self.blocksize = 37  
        
        # Создаем список со всеми спрайтами для анимации игрока.
        self.walk_animation = []
        set_sprite(self.walk_animation, self.number, 'wizard', 
                   set_dic['BLACK'], self.width, self.height)             
        self.image = self.walk_animation[0]
        self.rect = self.image.get_rect() 
        
        # Создаем список с улучшениями для игрока
        self.upgrade = upgrade
        
        # Задаем начальные координаты игрока, скорость перемещения и прыжка,
        # значение ускорения свободного падения и изначальный вид оружия.
        self.rect.centerx = self.WIDTH / 4
        self.rect.bottom = self.HEIGHT - self.blocksize
        self.speedx = 0
        self.speedy = 0
        self.maxspeed = 4 + self.upgrade[3]
        self.speedjump = 30
        self.gravity = 2
        self.weapon = 1
        
        # Задаем скорость восстановления маны стоимость по мане для
        # огня/фаирбола, максимальное и изначальное количество жизней, очков.
        self.manaspeed = 0.1
        self.maxhealth = 100 + self.upgrade[0]
        self.health = self.maxhealth 
        self.maxmana = 100 + self.upgrade[1]
        self.mana = self.maxmana  
        self.point = 0
                
        # Создаем группы для всех видов оружия.
        self.fireballs_sprites = pygame.sprite.Group()
        self.fires_sprites = pygame.sprite.Group()
        self.heal_fire_sprites = pygame.sprite.Group()
        
        # Переменные, отвечающие за частоту смены спрайтов игрока
        # во время движения.
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 45
             
        
    def timer(self):
        '''
        Вспомогательный метод, который регулирует частоту смены спрайтов игрока.

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
        Вспомогательный метод, отслеживающий столкновения игрока со стенами.

        Returns None.
        -------
        '''
        if (self.rect.right > self.WIDTH - self.blocksize) and (
                self.rect.top < self.HEIGHT - (self.blocksize + self.height)):
            self.rect.right = self.WIDTH - self.blocksize
        if (self.rect.left < self.blocksize) and (
                self.rect.top < self.HEIGHT - (self.blocksize + self.height)):
            self.rect.left = self.blocksize
        if self.rect.top < self.blocksize:
            self.rect.top = self.blocksize
        if self.rect.bottom > self.HEIGHT - self.blocksize:
            self.rect.bottom = self.HEIGHT - self.blocksize
           
            
    def update(self, mouse_posx):
        '''
        Метод отвечает за проверку нажатия клавиш, т.е. за прыжки,
        перемещение, передвижение игрока и смену спрайтов, в том числе
        и повороты за курсором мыши.
        
        Parameters
        ----------
        mouse_posx : type int
            Переменная, содержащая положение курсора мыши по x.
        Returns None.
        -------
        '''
        keystate = pygame.key.get_pressed()
        self.speedx = 0
        
        if self.mana < self.maxmana:
            self.mana += self.manaspeed
            
        if abs(self.speedy) <= self.speedjump: 
            self.rect.y -= self.speedy
            self.speedy -= self.gravity   
        
        if (keystate[pygame.K_SPACE]) and (self.rect.bottom >= 
                                           self.HEIGHT - self.blocksize):
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
            self.image = pygame.transform.flip(self.walk_animation[self.frame],
                                               True, False)
        self.collision() 

            
    def shoot(self, mouse_pos):
        '''
        Данный метод отвеччает за стрельбу фаирболом в указанном 
        направлении / применение огня вокруг игрока.
        
        Parameters
        ----------
        mouse_pos : type tuple
            Список, содержащий положение курсора мыши по x и y.
        Returns None.
        -------
        '''
        if self.weapon == 1:
            fireball = Fireball(self.rect.centerx, 
                                (self.rect.center[1] + self.rect.bottom)/2, 
                                 mouse_pos[0], mouse_pos[1], 
                                 self.blocksize, set_dic, self.upgrade[2])
            if self.mana >= fireball.cost:
                self.mana -= fireball.cost
                self.fireballs_sprites.add(fireball) 
                self.fireball_sound.play()
                
        if self.weapon == 2:
            fire = Fire((self.rect.center[0], self.rect.bottomright[1] - 22), 
                         set_dic)
            if self.mana >= fire.cost:
                self.mana -= fire.cost               
                self.fires_sprites.add(fire)
                self.fire_sound.play()
        
        if self.weapon == 3:
            heal_fire = Heal_fire(self.rect.centerx, 
                                  (self.rect.center[1] + self.rect.bottom)/2, 
                                  mouse_pos[0], mouse_pos[1], self.blocksize, 
                                  set_dic, 0)
            if self.mana >= heal_fire.cost:
                self.mana -= heal_fire.cost
                self.heal_fire_sprites.add(heal_fire)
                self.fireball_sound.play()
