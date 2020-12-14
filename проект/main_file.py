import pygame
import random
from os import path
from graphics import Menu
from graphics import bar
from graphics import Health
from settings import set_dic
from settings import snd_dic
from weapon import Fire, Fireball, Heal_fire
from mobs import Mob
from player import Player


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

'''
загружаем музыку
'''
snd_dir = path.join(path.dirname(__file__), 'sound')
pygame.mixer.music.load(path.join(snd_dir, 'background_music.wav'))


global_game = False


while not global_game: 
    
    ''' 
    Создаем объект класса Menu и список upgrade, в котором находятся
    все улучшения для героя, а также общее количество очков.
    '''      
    menu = Menu(set_dic, snd_dic)
    game_over = menu.main_menu()
    global_game = game_over
    upgrade = menu.load_data()
    
    
    heal_weapon = upgrade[5]
    
    '''
    Создаем группы для спрайтов, чтобы можно было проверять столкновения с ними.
    '''
    player_sprites = pygame.sprite.Group()
    mob_sprites = pygame.sprite.Group()                                                
    health_sprites = pygame.sprite.Group()
    
    '''
    Создаем объекты классов Player, Mob. Fireball, Fires, Health.
    '''
    player = Player(upgrade, set_dic, snd_dic)
    mob = Mob(set_dic)
    fireball = Fireball(1, 2, 3, 4, 5, set_dic, upgrade[2])
    fire = Fire((1, 2), set_dic)
    heal_fire = Heal_fire(1, 2, 3, 4, 5, set_dic, 0)
    health = Health(set_dic, 1, 2)
    
    '''
    Добавляем объекты player и mob в соответствующие группы.
    '''
    player_sprites.add(player)
    mob_sprites.add(mob)
    
    '''
    Запускаем музыку.
    '''
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)
    
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
                if event.key == pygame.K_3 and heal_weapon:
                    player.weapon = 3
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    game_over = menu.paus_menu(upgrade)
                    if game_over == False:
                        pygame.mixer.music.play(-1)
                    
        '''
        Обновляем координаты всех объектов.
        '''             
        player_sprites.update(pygame.mouse.get_pos()[0])    
        mob_sprites.update(player.rect.x, player.width)
        player.fireballs_sprites.update()
        player.fires_sprites.update()
        player.heal_fire_sprites.update()
    
        '''
        Проверяем столкновение спрайтов моба и огня/фаиербола.
        Если количество жизней моба меньше 0, то он уничтожается,
        при этом создается новый моб.
        '''
        if pygame.sprite.groupcollide(mob_sprites, player.fires_sprites, False, False):
            mob.health -= fire.damage
            snd_dic['mob_sound'][random.randint(0, 5)].play()
            if mob.health <= 0:
                if random.random() >= 1 - health.chance:
                    health = Health(set_dic, mob.rect.center[0], mob.rect.bottom)
                    health_sprites.add(health)
                mob.kill()
                player.point += 1
                upgrade[4] += 1
                mob = Mob(set_dic)
                mob_sprites.add(mob)
        
        if pygame.sprite.groupcollide(mob_sprites, player.fireballs_sprites, False, True):
            mob.health -= fireball.damage
            snd_dic['mob_sound'][random.randint(0, 5)].play()
            if mob.health <= 0:
                if random.random() >= 1 - health.chance:
                    health = Health(set_dic, mob.rect.center[0], mob.rect.bottom)
                    health_sprites.add(health)
                mob.kill()
                player.point += 1
                upgrade[4] += 1
                mob = Mob(set_dic)
                mob_sprites.add(mob)
               
        if pygame.sprite.groupcollide(mob_sprites, player.heal_fire_sprites, False, True):
            mob.health -= fireball.damage
            snd_dic['mob_sound'][random.randint(0, 5)].play()
            if mob.health <= 0:
                if random.random() >= 1 - health.chance:
                    health = Health(set_dic, mob.rect.center[0], mob.rect.bottom)
                    health_sprites.add(health)
                mob.kill()
                player.point += 1
                upgrade[4] += 1
                mob = Mob(set_dic)
                mob_sprites.add(mob)
             
            if player.health < player.maxhealth:    
                player.health += heal_fire.heal
                snd_dic['heal'].play()
                if player.health > player.maxhealth:
                    player.health = player.maxhealth
                
        '''
        Проверяем столкновение игрока с мобом, если они столкнулись, то
        уменьшаем количество жизней игрока и оттталкиваем игрока.
        '''
        if pygame.sprite.groupcollide(mob_sprites, player_sprites, False, False):
            snd_dic['pain_sound'][random.randint(0,5)].play()
            if (player.rect.right >= mob.rect.left and player.rect.left <= 
                mob.rect.right) or (player.rect.left <= mob.rect.right and 
                                    player.rect.right >= mob.rect.left):
                                    
                if player.rect.center[0] < mob.rect.center[0]:
                    player.rect.right = mob.rect.left - player.width    
                else:
                    player.rect.left = mob.rect.right + player.width
                player.health -= mob.damage   
                
        if pygame.sprite.groupcollide(health_sprites, player_sprites, False, 
                                      False) and (player.health < 
                                                  player.maxhealth):
            player.health += health.heal
            snd_dic['heal'].play()
            if player.health > player.maxhealth:
                player.health = player.maxhealth
            pygame.sprite.groupcollide(health_sprites, player_sprites, True, False)
            
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
        player.fireballs_sprites.draw(set_dic['screen'])
        player.fires_sprites.draw(set_dic['screen'])
        player.heal_fire_sprites.draw(set_dic['screen'])
        health_sprites.draw(set_dic['screen'])
        
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