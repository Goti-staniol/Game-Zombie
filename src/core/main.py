from cfg import (
    player_img,
    start_btn_img,
    hover_start_img,
    exit_btn_img,
    hover_exit_img,
    check_box_c,
    check_box_u,
    bg_img,
    bullet_img,
    FPS,
)

from .models import (
    Player,
    Zombie,
    Buttons,
    CheckBox,
    window,
)

import pygame

from pygame import *
from time import time
from random import randint

init()

clock = pygame.time.Clock()


def start_game(status: bool, current_window: str = 'main') -> None:
    player = Player((20, 350), (100, 100), 3, player_img, bullet_img)
    zombie = Zombie((100, 100), 2, player_img)

    start_btn = Buttons((350, 250), (50, 50), start_btn_img)
    exit_btn = Buttons((250, 280), (200, 100), exit_btn_img)
    
    checkbox = CheckBox((10, 10), (30, 30), 'Музыка', check_box_c)
    
    music = True
    music_play = False
    
    while status:
        mouse_pos = mouse.get_pos()
        
        if current_window == 'main':
            window.blit(bg_img, (0, 0))
            
            if music and not music_play:
                mixer.music.load('src/music/bg_music.mp3')
                mixer.music.play(-1)  
                music_play = True 
        
            if not music and music_play:
                mixer.music.stop()  
                music_play = False
                        
            start_btn.draw()
            exit_btn.draw()
            checkbox.draw()
            
            if start_btn.rect.collidepoint(mouse_pos):
                start_btn = Buttons((200, 180), (300, 100), hover_start_img)
            else:
                start_btn = Buttons((200, 180), (300, 100), start_btn_img)
                
            if exit_btn.rect.collidepoint(mouse_pos):
                exit_btn = Buttons((235, 280), (200, 100), hover_exit_img)
            else:
                exit_btn = Buttons((250, 280), (200, 100), exit_btn_img)

        if current_window == 'start':
            keys = key.get_pressed()
            
            window.blit(bg_img, (player.move_x, 0))
            window.blit(bg_img, (player.move_x + 700, 0))
            
            player.draw()
            player.control(keys)
            
            player.gun.update_bullets()
            player.gun.draw_bullets()
            
            zombie.add_zombie()
            zombie.update()
        
        for e in event.get():
            if e.type == QUIT:
                status = False
            
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1: 
                if exit_btn.rect.collidepoint(mouse_pos):
                    status = False
            
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1: 
                if start_btn.rect.collidepoint(mouse_pos):
                    current_window = 'start'
                    
                if checkbox.rect.collidepoint(mouse_pos):
                    if music:
                        checkbox = CheckBox((10, 10), (30, 30), 'Музыка', check_box_u)
                        music = False
                    else:
                        checkbox = CheckBox((10, 10), (30, 30), 'Музыка', check_box_c)
                        music = True
                
                
        display.update()
        clock.tick(FPS)