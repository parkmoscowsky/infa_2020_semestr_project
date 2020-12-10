import pygame
from os import path
from graphics import Menu
from settings import set_sprite
from settings import set_dic
from weapon import Fire, Fireball
from graphics import bar
from mobs import Mob

pygame.init()
pygame.mixer.init()

pygame.display.set_caption("Dungeon")

'''
Загружаем задний фон из папки с игрой и меняем его масштаб как нам нужно.
'''
img_dir = path.join(path.dirname(__file__), 'king')
background = pygame.image.load(path.join(img_dir, 'test.png')).convert()
background_rect = background.get_rect()
background = pygame.transform.scale(background, 
                                    (set_dic['WIDTH'], set_dic['HEIGHT'])) 


pygame.mixer.music.load('background_music.wav')
sound = pygame.mixer.Sound('background_music.wav')

class Player(pygame.sprite.Sprite):
    def __init__(self, upgrade, set_dic):
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
        '''
        Задают размеры игрока, квадратного блока и количество спрайтов игрока.
        '''
        self.width = 60
        self.height = 85
        self.blocksize = 37  
        self.number = 8
        
        '''
        Создаем список со всеми картинками 
        для анимации игрока в нужном нам виде.
        '''
        self.walk_animation = []
        set_sprite(self.walk_animation, self.number, 'wizard', 
                   set_dic['BLACK'], self.width, self.height)             
        self.image = self.walk_animation[0]
        self.rect = self.image.get_rect()       
        
        '''
        Задаем начальные координаты игрока, скорость перемещения и прыжка,
        значение ускорения свободного падения и изначальный вид оружия.
        '''
        self.rect.centerx = set_dic['WIDTH'] / 4
        self.rect.bottom = set_dic['HEIGHT'] - self.blocksize
        self.speedx = 0
        self.speedy = 0
        self.maxspeed = 4 + upgrade[3]
        self.speedjump = 30
        self.gravity = 2
        self.weapon = 1
        
        '''
        Задаем стоимость по мане для огня/фаирбола, максимальное и 
        изначальное количество жизней, очков.
        '''
        self.fireball_cost = 15
        self.fire_cost = 30
        self.manaspeed = 0.1
        self.maxhealth = 100 + upgrade[0]
        self.health = self.maxhealth 
        self.maxmana = 100 + upgrade[1]
        self.mana = self.maxmana  
        self.point = 0
        
        '''
        Переменные, отвечающие за частоту смены спрайтов игрока
        во время движения.
        '''
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
        if (self.rect.right > set_dic['WIDTH'] - self.blocksize) and (
                self.rect.top < set_dic['HEIGHT']-(self.blocksize + self.height)):
            self.rect.right = set_dic['WIDTH'] - self.blocksize
        if (self.rect.left < self.blocksize) and (
                self.rect.top < set_dic['HEIGHT']-(self.blocksize + self.height)):
            self.rect.left = self.blocksize
        if self.rect.top < self.blocksize:
            self.rect.top = self.blocksize
        if self.rect.bottom > set_dic['HEIGHT'] - self.blocksize:
            self.rect.bottom = set_dic['HEIGHT'] - self.blocksize
                
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
            self.rect.y -= self.speedy                                                   #### Для двойного прыжка это не пойдет
            self.speedy -= self.gravity   
        
        if (keystate[pygame.K_SPACE]) and (self.rect.bottom >= 
                                           set_dic['HEIGHT'] - self.blocksize):
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
            if self.mana >= self.fireball_cost:
                self.mana -= self.fireball_cost
                fireball = Fireball(self.rect.centerx, 
                                    (self.rect.center[1] + self.rect.bottom)/2,
                                    mouse_pos[0], mouse_pos[1], self.blocksize,
                                    set_dic, upgrade[2])
                
                fireballs_sprites.add(fireball) 
        if self.weapon == 2:
            if self.mana >= self.fire_cost:
                self.mana -= self.fire_cost
                fire = Fire((self.rect.center[0], 
                             self.rect.bottomright[1] - 22), set_dic) 
                
                fires_sprites.add(fire)       
    
    
''' 
Создаем объект класса Menu и список upgrade, в котором находятся
вск улучшения для героя, а также общее количество очков.
'''      
menu = Menu(set_dic)
game_over = menu.main_menu()
upgrade = menu.load_data()

'''
Создаем группы для спрайтов, чтобы можно было проверять столкновения с ними.
'''
player_sprites = pygame.sprite.Group()
mob_sprites = pygame.sprite.Group()                                                
fireballs_sprites = pygame.sprite.Group()
fires_sprites = pygame.sprite.Group()

'''
Создаем объекты классов Player, Mob. Fireball, Fires.
'''
player = Player(upgrade, set_dic)
mob = Mob(set_dic)
fireball = Fireball(1, 2, 3, 4, 5, set_dic, upgrade[2])
fire = Fire((1, 2), set_dic)

'''
Добавляем объекты player и mob в соответствующие группы.
'''
player_sprites.add(player)
mob_sprites.add(mob)

'''
Основная переменная, которая отвечает за запуск игрового цикла.
Цикл работает, пока game_over == False.
'''


pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1)

while not game_over:
    
    '''
    Проверяет нажатие клавиш.
    '''
    set_dic['clock'].tick(set_dic['FPS'])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.shoot(event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                player.weapon = 1
            if event.key == pygame.K_2:
                player.weapon = 2
            if event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                game_over = menu.paus_menu(upgrade)
                pygame.mixer.music.play(-1)
                
    '''
    Обновляем координаты всех объектов.
    '''             
    player_sprites.update(pygame.mouse.get_pos()[0])    
    mob_sprites.update(player.rect.x, player.width)
    fireballs_sprites.update()
    fires_sprites.update()

    '''
    Проверяем столкновение спрайтов моба и огня/фаиербола.
    Если количество жизней моба меньше 0, то он уничтожается,
    при этом создается новый моб.
    '''
    if pygame.sprite.groupcollide(mob_sprites, fires_sprites, False, False):
       mob.health -= fire.damage
       if mob.health <= 0:
           mob.kill()
           player.point += 1
           upgrade[4] += 1
           mob = Mob(set_dic)
           mob_sprites.add(mob)
    
    if pygame.sprite.groupcollide(mob_sprites, fireballs_sprites, False, True):
       mob.health -= fireball.damage
       if mob.health <= 0:
           mob.kill()
           player.point += 1
           upgrade[4] += 1
           mob = Mob(set_dic)
           mob_sprites.add(mob)
           
    '''
    Проверяем столкновение игрока с мобом, если они столкнулись, то
    уменьшаем количество жизней игрока и оттталкиваем игрока.
    '''
    if pygame.sprite.groupcollide(mob_sprites, player_sprites, False, False):
        if (player.rect.right >= mob.rect.left and player.rect.left <= 
            mob.rect.right) or (player.rect.left <= mob.rect.right and 
                                player.rect.right >= mob.rect.left):
                                
            if player.rect.center[0] < mob.rect.center[0]:
                player.rect.right = mob.rect.left - player.width    ###отталкивание
            else:
                player.rect.left = mob.rect.right + player.width
            player.health -= mob.damage   
            
    '''
    Отрисовывает задний фон, полоску жизней и здоровья и все спрайты.
    Обновляет экран.
    '''
    set_dic['screen'].blit(background, background_rect)
    bar(50, 40, 150, 20, set_dic['DARKRED'], set_dic['RED'], player.health,
        player.maxhealth, 'health ')
    bar(50, 70, 150, 20, set_dic['DARKBLUE'], set_dic['BLUE'], player.mana,
        player.maxmana, 'mana ')
    player_sprites.draw(set_dic['screen'])
    mob_sprites.draw(set_dic['screen'])
    fireballs_sprites.draw(set_dic['screen'])
    fires_sprites.draw(set_dic['screen'])
    pygame.display.flip()
    
    '''
    Если у игрока кончились жизни, то игра завершается.
    '''
    if player.health <= 0:
        menu.save(upgrade)
        game_over = True
        pygame.mixer.music.stop()
        menu.death(player.point) 



pygame.quit()   