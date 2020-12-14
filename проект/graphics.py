import pygame
import time
from settings import set_sprite
from settings import set_dic
from settings import snd_dic

# Достаем из словаря необходимые нам константы.
screen = set_dic['screen']



def bar(coord_barx, coord_bary, bar_width, bar_height, back_color, 
        front_color, health, maxhealth, text):
    '''
    Функция позволяет рисовать полоску здоровья/маны в заданного размера, в 
    заданном месте, заданного цвета и с заданным текстом.

    Parameters
    ----------
    coord_barx : type int
        Координата по x верхнего левого угла полоски.
    coord_bary : type int
        Координата по y верхнего левого угла полоски.
    bar_width : type int
        Длина полоски.
    bar_height : type int
        высота полоски.
    back_color : type tuple
        Цвет заднего фона полоски.
    front_color : type tuple
        Цвет основного (переднего) фона полоски.
    health : type int
        Значение здоровья/маны, которое надо отображать.
    maxhealth : type int
        Максимальное значение здоровья/маны.
    text : type string
        Текст, который необходимо написать рядом с полоской.

    Returns None.
    -------
    '''
    pygame.draw.rect(screen, back_color, 
                     (coord_barx, coord_bary, bar_width, bar_height))
    pygame.draw.rect(screen, front_color, 
                     (coord_barx, coord_bary, 
                      health * bar_width // maxhealth, bar_height))
    f = pygame.font.Font(None, 20)
    t = f.render(text + str(round(health)), True, (0, 0, 0))
    screen.blit(t, (coord_barx + bar_width, coord_bary))


class Health(pygame.sprite.Sprite):
    def __init__(self, set_dic, coord_x, coord_y):
        '''
        Конструктор класса Health.
        
        Parameters
        ----------
        set_dic : type mapping
            Словарь со всеми основными переменными, 
            который импортируется из settings.
        coord_x : type
            Координата смерти моба по оси x.
        coord_y : type
            Координата смерти моба по оси y.

        Returns None.
        -------
        '''
        pygame.sprite.Sprite.__init__(self)
        
        # Достаем из словаря необходиымые константы.
        self.BLACK = set_dic['BLACK']
        
        # Задаем размеры выпадающего сердечка, количество восстанавливаемых 
        # им жизней и шанс его появления. 
        self.width = 20
        self.height = 20
        self.heal = 5
        self.chance = 0.3
        
        # Устанавливаем спрайт сердечка на месте смерти моба.
        self.health_sprite = []
        set_sprite(self.health_sprite, 1, 'health', self.BLACK, 
                   self.width, self.height)
        self.image = self.health_sprite[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = coord_x
        self.rect.bottom = coord_y


class Menu(pygame.sprite.Sprite):
    def __init__(self, set_dic, snd_dic):
        '''
        Конструктор класса Menu.

        Parameters
        ----------
        set_dic : type mapping
            Словарь со всеми основными переменными, 
            который импортируется из settings.

        Returns None.
        -------
        '''
        pygame.sprite.Sprite.__init__(self)
        
        # Извлекаем нужные нам переменные из словарей.
        self.WIDTH = set_dic['WIDTH']
        self.HEIGHT = set_dic['HEIGHT']
        self.BLACK = set_dic['BLACK']
        self.WHITE = set_dic['WHITE']
        self.clock = set_dic['clock']
        self.screen = set_dic['screen']      
        self.FPS = set_dic['FPS']
        self.clock = set_dic['clock']
        self.screen = set_dic['screen']
        self.click_sound = snd_dic['click_sound']
        self.buy_sound = snd_dic['buy_sound']
        
        # Создаем список со всеми картинками для меню.
        self.menu_sprite = []
        set_sprite(self.menu_sprite, 3, 'menu', self.BLACK, 
                   self.WIDTH, self.HEIGHT)
        self.image = self.menu_sprite[0]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        
        self.upgrade_sprite = []
        set_sprite(self.upgrade_sprite, 5, 'upgrade', self.BLACK, 50, 50)
        
        # Переменная, отвечающая за выход из меню
        self.game_exit = False

        
    def main_menu(self):
        '''
        Данный метод вызывает основное меню в начале игры 
        или после смерти игрока.

        Returns None.
        -------
        '''
        while True:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (event.button == 1) and (230 < event.pos[0] < 580) and (
                            80 < event.pos[1] < 130):
                        self.click_sound.play()
                        time.sleep(0.1)
                        self.shop_menu()
                        
                    if (event.button == 1) and (230 < event.pos[0] < 580) and (
                            150 < event.pos[1] < 200):
                        self.click_sound.play()
                        time.sleep(0.1)
                        return(self.game_exit)
                    
                    if (event.button == 1) and (230 < event.pos[0] < 580) and (
                            230 < event.pos[1] < 280):
                        self.click_sound.play()
                        time.sleep(0.1)
                        return(self.game_exit)
                    
                    if (event.button == 1) and (230 < event.pos[0] < 580) and (
                            300 < event.pos[1] < 350):
                        self.click_sound.play()
                        time.sleep(0.1)
                        self.help_menu()
                        
                    if (event.button == 1) and (230 < event.pos[0] < 580) and (
                            370 < event.pos[1] < 420):
                        self.click_sound.play()
                        time.sleep(0.1)
                        return(self.game_exit)
                    
                    if (event.button == 1) and (230 < event.pos[0] < 580) and (
                            440 < event.pos[1] < 490):
                        self.click_sound.play()
                        time.sleep(0.1)
                        self.game_exit = True
                        return(self.game_exit)
                        
            self.screen.blit(self.image, self.rect)
            pygame.display.flip()


    def paus_menu(self, upgrade):
        '''
        Данный метод открывает меню паузы во время игры

        Parameters
        ----------
        upgrade : type list
            Содержит в себе значение, которые необходимо сохранить в файл.

        Returns None.
        -------
        '''
        while True:
            self.image = self.menu_sprite[1]
            self.rect = self.image.get_rect()
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                        
                    if (event.button == 1) and (230 < event.pos[0] < 580) and (
                            150 < event.pos[1] < 200):
                        self.click_sound.play()
                        return(self.game_exit)
                    
                    if (event.button == 1) and (230 < event.pos[0] < 580) and (
                            230 < event.pos[1] < 280):
                        self.click_sound.play()
                        return(self.game_exit)
                    
                    if (event.button == 1) and (230 < event.pos[0] < 580) and (
                            300 < event.pos[1] < 350):
                        self.click_sound.play()
                        self.help_menu()
                    
                    if (event.button == 1) and (230 < event.pos[0] < 580) and (
                            370 < event.pos[1] < 420):
                        self.click_sound.play()
                        self.save(upgrade)
                    
                    if (event.button == 1) and (230 < event.pos[0] < 580) and (
                            440 < event.pos[1] < 490):
                        self.click_sound.play()
                        self.save(upgrade)
                        self.game_exit = True
                        return(self.game_exit)
                        
            self.screen.blit(self.image, self.rect)
            pygame.display.flip()


    def shop_menu(self):
        '''
        Данный метод отвечает за работу меню shop.

        Returns None.
        -------
        '''
        # Создаем список со всеми улучшениями.
        upgrade = self.load_data()
        
        # Настраиваем расположение всех спрайтов, используемых в магазине.
        self.image = self.menu_sprite[2]
        self.rect = self.image.get_rect() 

        image_1 = self.upgrade_sprite[0]
        rect_1 = image_1.get_rect()
        rect_1.x = 10
        rect_1.y = 90
        
        image_2 = self.upgrade_sprite[1]
        rect_2 = image_2.get_rect()
        rect_2.x = 10
        rect_2.y = 160
        
        image_3 = self.upgrade_sprite[2]
        rect_3 = image_3.get_rect()
        rect_3.x = 10
        rect_3.y = 230
        
        image_4 = self.upgrade_sprite[3]
        rect_4 = image_4.get_rect()
        rect_4.x = 10
        rect_4.y = 300
        
        image_5 = self.upgrade_sprite[4]
        rect_5 = image_5.get_rect()
        rect_5.x = 10
        rect_5.y = 370
        
        # Переменная, отвечающая за то, что игрок находится в магазине.
        t = True
        
        while t:
            
            # Устанавливаем стоимость каждого улучшения в магазине.
            hp_up_cost = (upgrade[0]/5 + 1)*4
            mana_up_cost = (upgrade[1]/5 + 1)*4
            damage_up_cost = (upgrade[2]/2 + 1)*5
            speed_up_cost = (upgrade[3] + 1) * 20
            heal_weapon_cost = 300
            
            # Здесь задается шрифт, стиль написания букв в магазине.
            self.screen.blit(self.image, self.rect)
            f = pygame.font.Font(None, 26)
            
            # Отрисовываем спрайты улучшений.
            self.screen.blit(image_1, rect_1)
            self.screen.blit(image_2, rect_2)
            self.screen.blit(image_3, rect_3)
            self.screen.blit(image_4, rect_4)
            self.screen.blit(image_5, rect_5)
            
            # Создаем текст, который пишем около спрайтов.
            # Если у игрока куплено максимальное улучшение, 
            # то выводим ему сообщение об этом.
            if upgrade[0] < 50:
                t_1 = f.render('Улучшение здоровья. +5 к здоровью. Текущее ' 
                               'доп. здоровье '+ str(int(upgrade[0])) + 
                               '. Стоимость '+ str(int(hp_up_cost)), True, 
                               self.BLACK)
            else:
                t_1 = f.render('Здоровье max', True, self.BLACK)
            
            if upgrade[1] < 50:
                t_2 = f.render('Улучшение маны. +5 к мане. Текущая доп. мана '
                               + str(int(upgrade[1])) + '. Стоимость ' + 
                               str(int(mana_up_cost)), True, self.BLACK)
            else:
                t_2 = f.render('Мана max', True, self.BLACK)
            
            if upgrade[2] < 10:
                t_3 = f.render('Улучшение урона фаирбола. +2 к урону. Текущий'
                               ' доп. урон ' +str(int(upgrade[2])) + 
                               '. Стоимость ' +str(int(damage_up_cost)), 
                               True, self.BLACK)
            else:
                t_3 = f.render('Урон max', True, self.BLACK)
                
            if upgrade[3] < 5:
                t_4 = f.render('Улучшение скорости. +1 к скорости. Текущая' 
                               ' доп. скорость ' + str(int(upgrade[3])) + 
                               '. Стоимость '+ str(int(speed_up_cost)), True, 
                               self.BLACK)
            else:
                t_4 = f.render('Скорость max', True, self.BLACK)
            
            if upgrade[5] == 0:
                t_5 = f.render('Восстанавливающее оружие. Стоимость 300 очков'
                               , True, self.BLACK)
            else:
                t_5 = f.render('У вас приобретен этот навык', True, self.BLACK)
            
            t = f.render('Ваш счёт ' + str(int(upgrade[4])), True, self.BLACK)
            
            # Отрисовка текста.
            self.screen.blit(t_1, (rect_1.right + 15, rect_1.center[1] - 5))
            self.screen.blit(t_2, (rect_2.right + 15, rect_2.center[1] - 5))
            self.screen.blit(t_3, (rect_3.right + 15, rect_3.center[1] - 5))
            self.screen.blit(t_4, (rect_4.right + 15, rect_4.center[1] - 5))
            self.screen.blit(t_5, (rect_5.right + 15, rect_5.center[1] - 5))
            self.screen.blit(t, (350, 20))
            
            # Основной цикл, в котором происходит проверка нажатия на кнопки.
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    
                    if  (rect_1.left < event.pos[0] < rect_1.right) and (
                            rect_1.top < event.pos[1] < rect_1.bottom) and (
                                upgrade[4] >= hp_up_cost) and (
                                    upgrade[0] < 50):
                        upgrade[4] -= hp_up_cost               
                        upgrade[0] += 5
                        self.buy_sound.play()
                        
                    if (rect_2.left < event.pos[0] < rect_2.right) and (
                            rect_2.top < event.pos[1] < rect_2.bottom) and (
                                upgrade[4] >= mana_up_cost) and (
                                    upgrade[1] < 50):
                        upgrade[4] -= mana_up_cost
                        upgrade[1] += 5
                        self.buy_sound.play()
                        
                    if (rect_3.left < event.pos[0] < rect_3.right) and (
                            rect_3.top < event.pos[1] < rect_3.bottom) and (
                                upgrade[4] >= damage_up_cost) and (
                                    upgrade[2] < 10):
                        upgrade[4] -= damage_up_cost
                        upgrade[2] += 2
                        self.buy_sound.play()
                        
                    if (rect_4.left < event.pos[0] < rect_4.right) and (
                            rect_4.top < event.pos[1] < rect_4.bottom) and (
                                upgrade[4] >= speed_up_cost) and (
                                    upgrade[3] < 5):
                        upgrade[4] -= speed_up_cost
                        upgrade[3] += 1
                        self.buy_sound.play()
                    
                    if (rect_5.left < event.pos[0] < rect_5.right) and (
                            rect_5. top < event.pos[1] < rect_5.bottom) and (
                                upgrade[4] >= 300) and (upgrade[5] == 0):
                        upgrade[4] -= heal_weapon_cost
                        upgrade[5] = 1
                        self.buy_sound.play()
                        
                    self.save(upgrade)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.image = self.menu_sprite[0]
                        self.rect = self.image.get_rect()
                        t = False
            
            pygame.display.flip()        


    def help_menu(self):
        '''
        Данный метод открывает меню помощи

        Returns None.
        -------
        '''
        t = True
        while t:
            self.screen.fill(self.WHITE)
            f = pygame.font.Font(None, 26)
            t = f.render('Здесь должно что-то появиться потом ...', 
                         True, self.BLACK)
            self.screen.blit(t, (self.WIDTH/2, self.HEIGHT/2))
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        t = False
            pygame.display.flip()
            
            
    def save(self, upgrade):
        '''
        Данный метод отвечает за сохранение данных в файл.

        Parameters
        ----------
        upgrade : type list
            Список, содержащий в себе данные, которые необходимо сохранить.

        Returns None.
        -------
        '''
        
        lines = ["hp_up = " + str(upgrade[0]),
                 "mana_up = " + str(upgrade[1]),
                 "damage_up = " + str(upgrade[2]),
                 "sp_up = " + str(upgrade[3]),
                 "global_point = " + str(upgrade[4]),
                 "heal_weapon = " + str(upgrade[5])] 
        with open("text.txt", "w") as file:
            for  line in lines:
                file.write(line + '\n')
    
    
    def load_data(self):
        '''
        Данный метод отвечает за загрузку данных об игре из файла.

        Returns None.
        -------
        '''
        upgrade = []
        with open("text.txt") as file:
            for line in file:
                upgrade.append(float(line.split()[2]))
        return(upgrade)
    
    
    def death(self, point):
        '''
        Данный метод отвечает за то, что после смерти игрока ему выводится
        сообщение о том, что он умер, а также количество его очков.

        Parameters
        ----------
        point : type int
            Количество заработанных за игру очков.

        Returns None.
        -------
        '''
        # Устанавливаем нужный фон.
        self.image = self.menu_sprite[2]
        self.rect = self.image.get_rect() 
        
        # Переменная, отвечающая за то, что игроку показывается сообщение.
        # Когда она принимает значение False, сообщение пропадает и ирок 
        # переносится в основное меню.
        run = True
        
        while run:
            # Выводим игроку текстовое сообщение.
            self.screen.blit(self.image, self.rect)
            f = pygame.font.Font(None, 26)
            t1 = f.render('Вы умерли. Нажмите пробел, чтобы продолжить ...', 
                          True, self.BLACK)
            t2 = f.render('Ваш счёт ' + str(point), True, self.BLACK)
            self.screen.blit(t1, (self.WIDTH/4, self.HEIGHT/2))
            self.screen.blit(t2, (self.WIDTH/2, self.HEIGHT/3))
            self.clock.tick(self.FPS)
            
            # Проверка нажатия клавиши space.
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.image = self.menu_sprite[0]
                        self.rect = self.image.get_rect()
                        run = False
                        
            pygame.display.flip()      