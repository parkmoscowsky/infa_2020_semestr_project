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


def set_sprite(sprite_list, number, name, color, width, height):
    '''
    Функция обрабатывает спрайты, которые подаются на вход. 
    Сами спрайты находятся в папке king, которая находится 
    в папке с программой. Она удаляет фон и задает размеры
    объекта. Файл должен быть изначально в формате png.
    При этом функция автоматически перевод файл в удобный
    для python формат. Файлы должны иметь общее имя с 
    разными упорядоченными индексами от 1 до number

    Parameters
    ----------
    sprite_list : type list
        Список, в который сохраняются изменённые спрайты.
    number : type int
        Количество спрайтов.
    name : type string
        Общее имя файлов.
    color : type tuple
        Один из описанных в начале программы цветов.
    width : type int
        Ширина, которую должен иметь спрайт, после обработки.
    height : type int
        Высота, которую должен иметь спрайт, после обработки.

    Returns None.
    -------
    '''
    for i in range(1, number+1):
        filename = (name + '{}.png').format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(color)
        img = pygame.transform.scale(img, (width, height))
        sprite_list.append(img)    







class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 60
        self.height = 85
        self.blocksize = 37  
        self.number = 8
        
        self.walk_animation = []
        set_sprite(self.walk_animation, self.number, 'wizard', BLACK, self.width, self.height)             
        self.image = self.walk_animation[0]
        self.rect = self.image.get_rect()       

        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - self.blocksize
        self.speedx = 0
        self.speedy = 0
        self.maxspeed = 4
        self.speedjump = 25
        self.gravity = 2
        self.weapon = 1
        self.direction = True
        
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
                
    def update(self):
        '''
        Метод отвечает за проверку нажатия клавиш, т.е. за прыжки,
        перемещение, передвижение игрока и смену спрайтов

        Returns None.
        -------
        '''
        keystate = pygame.key.get_pressed()
        self.speedx = 0
        
        if abs(self.speedy) <= self.speedjump: 
            self.rect.y -= self.speedy                                                   #### Для двойного прыжка это не пойдет
            self.speedy -= self.gravity   
        
        if (keystate[pygame.K_SPACE]) and (self.rect.bottom >= HEIGHT - self.blocksize) :
            self.speedy = self.speedjump
            
        if keystate[pygame.K_a]:
            self.speedx = -1 * self.maxspeed
            self.rect.x += self.speedx
            self.timer()
            self.image = pygame.transform.flip(self.walk_animation[self.frame], True, False)
            self.direction = False
            
    
        if keystate[pygame.K_d]:
            self.speedx = self.maxspeed
            self.rect.x += self.speedx
            self.timer()
            self.image = self.walk_animation[self.frame]
            self.direction = True
        self.collision()    
            
    def shoot(self):
        if self.weapon == 1:
            fireball = Fireball(self.rect.centerx, (self.rect.center[1] + self.rect.bottom)/2, self.direction, self.blocksize)
            all_sprites.add(fireball)
            fireballs.add(fireball) 
        if self.weapon == 2:
            fire = Fire((self.rect.center[0], self.rect.bottomright[1] - 22))                 
            all_sprites.add(fire)   
            fires.add(fire)                                                                      





class Fire(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.width = 200
        self.height = 40
        self.fire_animation = []
        set_sprite(self.fire_animation, 4, 'fire', BLACK, self.width, self.height)
        self.image = self.fire_animation[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  
        self.duration = 40
        
    def update(self):
        '''
        Метод отвечает за анимированное отображение огня.
        Внутри него встроен счетчик, который отслеживает, 
        как часто надо менять спрайты

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
    def __init__(self, x, y, direction, blocksize):
        pygame.sprite.Sprite.__init__(self)
        self.width = 45
        self.height = 30
        
        self.fireball_animation = []                                                         # Сделать анимацию при выстреле
        set_sprite(self.fireball_animation, 3, 'fireball', BLACK, self.width, self.height)
        if direction:
            self.speedx = 10
            self.image =  self.fireball_animation[0]
        else:
            self.speedx = -10
            self.image = pygame.transform.flip(self.fireball_animation[0], True, False)
            
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.blocksize = blocksize

    def update(self):
        self.rect.x += self.speedx
        if (self.rect.centerx - 0.45*self.width < self.blocksize) or (self.rect.centerx + 0.45*self.width > WIDTH - self.blocksize):
            self.kill()
            

all_sprites = pygame.sprite.Group()                                                
fireballs = pygame.sprite.Group()
fires = pygame.sprite.Group()
player = Player()
all_sprites.add(player)


game_over = False

while not game_over:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.shoot()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                player.weapon = 1
            if event.key == pygame.K_2:
                player.weapon = 2
                

    all_sprites.update()
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()       