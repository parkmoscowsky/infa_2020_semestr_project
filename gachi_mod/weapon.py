import pygame
import math
from settings import set_sprite
from settings import set_dic


class Fire(pygame.sprite.Sprite):
    
    def __init__(self, center, set_dic):
        '''
        Конструктор класса Fire. 

        Parameters
        ----------
        center : type tuple
            Координаты центра игрока, где и появляется сам огонь.
        set_dic : type mapping
            Словарь со всеми основными переменными, 
            который импортируется из settings.

        Returns None.
        -------
        '''
        pygame.sprite.Sprite.__init__(self)
        
        # Достаем из словаря необходимые константы.
        self.BLACK = set_dic['BLACK']
        
        # Задаем размеры огня, его урон, стоимость и продолжительность горения.
        self.width = 200
        self.height = 40
        self.damage = 0.2
        self.cost = 30
        self.duration = 40
        
        # Создаем список со спрайтами для анимации огня.
        self.fire_animation = []
        set_sprite(self.fire_animation, 4, 'fire', self.BLACK, 
                   self.width, self.height)
        self.image = self.fire_animation[0]
        self.rect = self.image.get_rect()
        
        # Задаем начальное положение огня
        self.rect.center = center
        
        # Задаем переменные, отвечающие за частоту смены спрайтов.
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  

    
    def update(self):
        '''
        Метод отвечает за анимированное отображение огня.
        Внутри него встроен счетчик, который отслеживает, 
        как часто надо менять спрайты.

        Returns None.
        -------
        '''
        now = pygame.time.get_ticks()
        
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == self.duration:
                self.kill()
            else:
                center = self.rect.center
                self.image = self.fire_animation[self.frame % 4]
                self.rect = self.image.get_rect()
                self.rect.center = center
                
                
                
class Fireball(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y, mouse_x, mouse_y, blocksize, 
                 set_dic, damage_up):
        '''
        Конструктор класса Fireball.

        Parameters
        ----------
        player_x : type int
            Координата игрока по оси x.
        player_y : type int
            Координата игрока по оси y.
        mouse_x : type int
            Координата мыши по оси x.
        mouse_y : type int
            Координата мыши по оси y.
        blocksize : type int
            Размер блока.
        set_dic : type mapping
            Словарь со всеми основными переменными, 
            который импортируется из settings.
        damage_up : type int
            Улучшение урона фаирбола, которое
            купил игрок в магазине.

        Returns None.
        -------
        '''
        pygame.sprite.Sprite.__init__(self)
        
        # Достаем из словаря все необходимые значения констант.
        self.WIDTH = set_dic['WIDTH']
        self.HEIGHT = set_dic['HEIGHT']
        self.BLACK = set_dic['BLACK']
        
        # Задаем размеры фаирбола, его урон и полную скорость и стоимость.
        self.width = 45
        self.height = 30
        self.damage = 10 + damage_up
        self.speed = 10
        self.cost = 15
        
        # Вычисляем скорость фаирбола по осям x и y в зависимости от того,
        # куда направлен курсор мыши.
        self.r = ((player_x - mouse_x)**2 + (player_y - mouse_y)**2)**0.5
        self.speedx = self.speed * (mouse_x - player_x)/self.r
        self.speedy = self.speed * (mouse_y - player_y)/self.r
        
        # Вычисляем угол, на который необходимо повернуть спрайт фаирбола 
        # в зависимости от того, куда был направлен курсор мыши при выстреле.
        # Поворачиваем спрайт на найденный угол.
        if mouse_x > player_x:
            self.angle = math.atan((player_y - mouse_y)/(mouse_x - player_x)
                                   )*180/math.pi
        else:
            self.angle = math.atan((player_y - mouse_y)/(mouse_x - player_x)
                                   )*180/math.pi + 180
            
        self.fireball_animation = []                                                         
        set_sprite(self.fireball_animation, 3, 'fireball', self.BLACK, 
                   self.width, self.height)
        
        self.image = pygame.transform.rotate(self.fireball_animation[0], 
                                             self.angle)
        self.rect = self.image.get_rect()
        
        # Устанавливаем координаты появления фаирбола и размер блока.
        self.rect.centerx = player_x
        self.rect.centery = player_y
        self.blocksize = blocksize

    def update(self):
        '''
        Отвечает за движение фаирбола и его уничтожение, 
        если он вылетает за границы.
        Returns
        -------
        None.
        '''
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.centerx - 0.45*self.width < self.blocksize) or (
            self.rect.centerx + 0.45*self.width > self.WIDTH -
            self.blocksize):
            self.kill()
            
            
class Heal_fire(Fireball):
    def __init__(self, player_x, player_y, mouse_x, mouse_y, blocksize, 
                 set_dic, damage_up):
        '''
        Parameters
        ----------
        player_x : type int
            Координата игрока по оси x.
        player_y : type int
            Координата игрока по оси y.
        mouse_x : type int
            Координата мыши по оси x.
        mouse_y : type int
            Координата мыши по оси y.
        blocksize : type int
            Размер блока.
        set_dic : type mapping
            Словарь со всеми основными переменными, 
            который импортируется из settings.
        damage_up : type int
            Улучшение урона фаирбола, которое
            купил игрок в магазине.

        Returns None.
        -------
        '''
        # Наследуем все переменные и методы класса Fireball.
        super().__init__(player_x, player_y, mouse_x, mouse_y, blocksize,
                         set_dic, damage_up)
        
        # Задаем новые значения размеров, урона скорости, стоимости для 
        # данного класса. Также вводим переменную heal, которая отвечает 
        # за количество восстанавливаемых игроком жизней.
        self.width = 45
        self.height = 30
        self.damage = 10
        self.speed = 10
        self.cost = 25
        self.heal = 5
        
        # Устанавливаем новый спрайт для данного класса.
        self.fireball_animation = []                                                         
        set_sprite(self.fireball_animation, 1, 'heal_fire', self.BLACK, 
                   self.width, self.height)
        self.image = pygame.transform.rotate(self.fireball_animation[0], 
                                             self.angle)


