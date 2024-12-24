from cfg import (
    start_btn_img,
    hover_start_img,
    exit_btn_img,
    hover_exit_img,
    bg_img,
    bullet_img,
    FPS,
)

from .models import (
    Player,
    Zombie,
    Buttons,
    window,
    Gun,
    zombies,
    bullets
)

import pygame

from pygame import *
from time import time
from random import randint

init()

clock = pygame.time.Clock()

music = True

if music:
    mixer.music.load('src/music/bg_music.mp3')
    mixer.music.play(-1)

def start_game(status: bool, current_window = 'main') -> None:
    player = Player(20, 350, 100, 100, 3, 'src/images/player_sprite.png')
    gun = Gun(10, 10, player, bullet_img)
    print(f"Позиция игрока: {player.rect}")

    start_btn = Buttons(350, 250, 50, 50, start_btn_img)
    exit_btn = Buttons(250, 280, 200, 100, exit_btn_img)
    
    spawn_time = time() 
    spawn_interval = 3
    
    while status:
        mouse_pos = mouse.get_pos()
        
        if current_window == 'main':
            window.blit(bg_img, (0, 0))
            
            start_btn.draw()
            exit_btn.draw()
            
            if start_btn.rect.collidepoint(mouse_pos):
                start_btn = Buttons(200, 180, 300, 100, hover_start_img)
            else:
                start_btn = Buttons(200, 180, 300, 100, start_btn_img)
                
            if exit_btn.rect.collidepoint(mouse_pos):
                exit_btn = Buttons(235, 280, 200, 100, hover_exit_img)
            else:
                exit_btn = Buttons(250, 280, 200, 100, exit_btn_img)
        
        if current_window == 'start':
            keys = key.get_pressed()
            
            window.blit(bg_img, (player.move_x, 0))
            window.blit(bg_img, (player.move_x + 700, 0))
            
            player.draw()
            player.control(keys)
            
            gun.shot(keys)  
            gun.update_bullets()        
            gun.draw_bullets(window)
            
            current_time = time()
            
            if current_time - spawn_time >= spawn_interval:
                y = randint(330, 385)
                zombies.append(Zombie(650, y, 50, 50, 1, 'src/images/player_sprite.png'))
                
                spawn_time = current_time
                
                if spawn_interval != 1:
                    spawn_interval -= 1
            
            for zombie in zombies:
                zombie.draw()
                zombie.move()
        
        for e in event.get():
            if e.type == QUIT:
                status = False
            
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1: 
                if exit_btn.rect.collidepoint(mouse_pos):
                    status = False
            
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1: 
                if start_btn.rect.collidepoint(mouse_pos):
                    current_window = 'start'
            
        display.update()
        clock.tick(FPS)