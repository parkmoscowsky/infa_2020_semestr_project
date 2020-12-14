import pygame
from os import path


pygame.mixer.init()

# Задаем длину и высоту окна игры, частоту обновления экрана. 
WIDTH = 800
HEIGHT = 600
FPS = 60

# Объявляем основные цвета, которые используются во всей программе.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARKRED = (100, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARKBLUE = (24, 168, 173)
YELLOW = (255, 255, 0)

# Создаем экран с заданными размерами и переменную, отвечающую за счет кадров. 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Создаем единый словарь из всех объявленных выше переменных, который будем 
# экспортировать во все остальные модули.
set_dic = {'WIDTH' : WIDTH, 'HEIGHT' : HEIGHT, 'FPS' : FPS, 'WHITE' : WHITE, 
           'BLACK' : BLACK, 'RED' : RED, 'DARKRED' : DARKRED, 'GREEN' : GREEN,
           'BLUE' : BLUE, 'DARKBLUE' : DARKBLUE,'YELLOW' : YELLOW, 
           'screen' : screen, 'clock' : clock}

# Задаем папку, из которой будем брать все звуки.
snd_dir = path.join(path.dirname(__file__), 'sound')

# Далее из файла загружаются все основные звуки. 
# Для удобства оним разбиты на блоки.
click_sound = pygame.mixer.Sound(path.join(snd_dir, 'click.wav'))
fireball_sound = pygame.mixer.Sound(path.join(snd_dir, 'fireball.wav'))
fire_sound = pygame.mixer.Sound(path.join(snd_dir, 'fire.wav'))
heal = pygame.mixer.Sound(path.join(snd_dir, 'heal.wav'))

mob1 = pygame.mixer.Sound(path.join(snd_dir, 'mob1.wav'))
mob2 = pygame.mixer.Sound(path.join(snd_dir, 'mob2.wav'))
mob3 = pygame.mixer.Sound(path.join(snd_dir, 'mob3.wav'))
mob4 = pygame.mixer.Sound(path.join(snd_dir, 'mob4.wav'))
mob5 = pygame.mixer.Sound(path.join(snd_dir, 'mob5.wav'))
mob6 = pygame.mixer.Sound(path.join(snd_dir, 'mob6.wav'))
mob_sound = [mob1, mob2, mob3, mob4, mob5, mob6]

pain1 = pygame.mixer.Sound(path.join(snd_dir, 'pain1.wav'))
pain2 = pygame.mixer.Sound(path.join(snd_dir, 'pain2.wav'))
pain3 = pygame.mixer.Sound(path.join(snd_dir, 'pain3.wav'))
pain4 = pygame.mixer.Sound(path.join(snd_dir, 'pain4.wav'))
pain5 = pygame.mixer.Sound(path.join(snd_dir, 'pain5.wav'))
pain6 = pygame.mixer.Sound(path.join(snd_dir, 'pain6.wav'))
pain_sound = [pain1, pain2, pain3, pain4, pain5, pain6]

# Создаем словарь из звуков, который будем экспортировать в остальные модули.
snd_dic = {'click_sound' : click_sound, 'fireball_sound' : fireball_sound, 
           'fire_sound' : fire_sound, 'heal' : heal, 'mob_sound' : mob_sound, 
           'pain_sound' : pain_sound}


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
    img_dir = path.join(path.dirname(__file__), 'king')
    for i in range(1, number+1):
        filename = (name + '{}.png').format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(color)
        img = pygame.transform.scale(img, (width, height))
        sprite_list.append(img)  