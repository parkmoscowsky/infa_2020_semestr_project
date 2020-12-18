import pygame
from settings import set_sprite
from settings import set_dic


class Mob(pygame.sprite.Sprite):
    def __init__(self, set_dic):
        '''
        Конструктор класса Mob

        Parameters
        ----------
        set_dic : type mapping
            Словарь со всеми основными переменными, 
            который импортируется из settings.

        Returns None.
        -------
        '''
        pygame.sprite.Sprite.__init__(self)
        
        self.gachi_mode_activate = set_dic['gachi_mode_activate']
        
        # Задаем папку, из которой будем брать спррайты.
        if self.gachi_mode_activate == 0:
            self.folder = 'king'
        else:
            self.folder = 'king_gachi'
        
        # Задаем размеры моба и количество спрайтов в его анимации.
        self.width = 80
        self.height = 70
        self.number = 9
        
        # Создаем список со всеми картинками анимации моба.
        self.mob_animation = []
        set_sprite(self.mob_animation, self.number, 'slime', set_dic['BLACK'],
                   self.width, self.height, self.folder)
        self.image = self.mob_animation[0]
        self.rect = self.image.get_rect()
        
        # Задаем изначальные коорднаты моба, его скорость, урон и здоровье.
        self.rect.centerx = set_dic['WIDTH'] 
        self.rect.bottom = set_dic['HEIGHT'] - 37
        self.speedx = 2
        self.damage = 5
        self.health = 20
        
        # Переменные, отвечающие за частоту смены спрайтов моба
        # во время движения.
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 

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
        
    def update(self, player_coordinate, player_width):
        '''
        Метод, который отвечает за то, чтобы моб шел в сторону игрока

        Parameters
        ----------
        player_coordinate : type int
            Координата игрока по x.
        player_width : type int
            Ширина игрока.

        Returns None.
        -------
        '''
        if player_coordinate + player_width <= self.rect.x:
            self.rect.x -= self.speedx
            self.timer()
            self.image = self.mob_animation[self.frame]
            
        if player_coordinate >= self.rect.right:
            self.rect.x += self.speedx
            self.timer()
            self.image = pygame.transform.flip(self.mob_animation[self.frame],
                                               True, False)
            
class Gorilla(pygame.sprite.Sprite):
    def __init__(self, set_dic):
        '''
        Конструктор класса Mob

        Parameters
        ----------
        set_dic : type mapping
            Словарь со всеми основными переменными, 
            который импортируется из settings.

        Returns None.
        -------
        '''
        pygame.sprite.Sprite.__init__(self)
        
        self.gachi_mode_activate = set_dic['gachi_mode_activate']
        
        # Задаем папку, из которой будем брать спррайты.
        if self.gachi_mode_activate == 0:
            self.folder = 'king'
        else:
            self.folder = 'king_gachi'
        
        # Задаем размеры моба и количество спрайтов в его анимации.
        self.width = 130    #110
        self.height = 120    #50
        self.number_1 = 6
        self.number_2 = 6
        
        # Создаем список со всеми картинками анимации моба.
        self.mob_animation = []
        set_sprite(self.mob_animation, self.number_1, 'gorilla', set_dic['WHITE'],
                   self.width, self.height, self.folder)
        self.image = self.mob_animation[0]
        self.rect = self.image.get_rect()
        
        self.mob_animation_attack = []
        set_sprite(self.mob_animation_attack, self.number_2, 'gorilla_hit', 
                   set_dic['WHITE'], self.width, self.height, self.folder)
        
        # Задаем изначальные коорднаты моба, его скорость, урон и здоровье.
        self.rect.centerx = set_dic['WIDTH'] 
        self.rect.bottom = set_dic['HEIGHT'] - 37
        self.speedx = 1
        self.damage = 50
        self.health = 100
        
        # Расстояние, на котором срабатывает анимация атаки.
        self.distance = 20
        
        # Переменные, отвечающие за частоту смены спрайтов моба
        # во время движения.
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 90

    def timer(self, number):
        '''
        Вспомогательный метод, который регулирует частоту смены спрайтов

        Returns None.
        -------
        '''
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == number:
                self.frame = 0
            else:
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center
        
    def update(self, player_coordinate, player_width):
        '''
        Метод, который отвечает за то, чтобы моб шел в сторону игрока

        Parameters
        ----------
        player_coordinate : type int
            Координата игрока по x.
        player_width : type int
            Ширина игрока.

        Returns None.
        -------
        '''
        if player_coordinate + player_width + self.distance <= self.rect.left:
            self.rect.x -= self.speedx
            self.timer(self.number_1)
            self.image = self.mob_animation[self.frame]
            
        if player_coordinate + player_width <= self.rect.left <= player_coordinate + player_width + self.distance:
            if self.frame >= self.number_2:
                self.frame = 0
            self.rect.x -= self.speedx
            self.timer(self.number_2)
            self.image = self.mob_animation_attack[self.frame]
            
        if player_coordinate - self.distance >= self.rect.right:
            self.rect.x += self.speedx
            self.timer(self.number_1)
            self.image = pygame.transform.flip(self.mob_animation[self.frame],
                                               True, False)
            

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            