from cfg import (
    W, H,
    walking,
    back_walk,
    reload_gun
)

from typing import Tuple

from pygame import *
import pygame

from time import time
from random import randint

window = display.set_mode((W, H))
display.set_caption('Zombie Survaival')

zombies = []


class Buttons(sprite.Sprite):
    def __init__(
        self,
        position: Tuple[int, int],
        size: Tuple[int, int],
        img
    ):
        super().__init__()
        self.img = transform.scale(image.load(img), size)
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = position
    
    def draw(self):
        window.blit(self.img, (self.rect.x, self.rect.y))


class CheckBox(sprite.Sprite):
    def __init__(
        self,
        position: Tuple[int, int],
        size: Tuple[int, int],
        text: str,
        img: str
    ):
        super().__init__()
        self.position = position
        self.size = size
        self.img = transform.scale(
            image.load(img),
            size
        )
        self.rect = self.img.get_rect()
        
        font = pygame.font.Font(None, 23)
        self.text = font.render(text, True, (0, 0, 0))
        self.text_pos = (
            self.rect.x + 50, 
            self.rect.y + 20
        )
    
    def draw(self):
        window.blit(self.text, self.text_pos)
        window.blit(self.img, self.position)


class ZombieModel(sprite.Sprite):
    def __init__(self, size: Tuple[int, int], speed: int, img: str):
        super().__init__()
        self.img = transform.scale(
            image.load(img), 
            size
        )
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = 650, randint(330, 385)
        self.speed = speed

    def move(self):
        self.rect.x -= self.speed

    def draw(self):
        window.blit(self.img, (self.rect.x, self.rect.y))


class Zombie:
    def __init__(self, size: Tuple[int, int], speed: int, img: str):
        self.size = size
        self.speed = speed
        self.img = img
        self.spawn_time = time()

    def add_zombie(self) -> None:
        current_time = time()
                
        if current_time - self.spawn_time >= 3:
            zombies.append(
                ZombieModel(
                    self.size,
                    self.speed,
                    self.img
                )
            )
            
            self.spawn_time = current_time
    
    def update(self) -> None:
        for zombie in zombies:
            zombie.draw()
            zombie.move() 


class Player(sprite.Sprite):
    def __init__(
        self, 
        position: Tuple[int, int],
        size: Tuple[int, int],
        speed: int, 
        hero_img: str,
        bullets_img: str
    ):
        self.initial_image = transform.scale(image.load(hero_img), size)
        self.hero_img = transform.scale(image.load(hero_img), size)
        self.rect = self.hero_img.get_rect()
        self.w, self.h = size
        self.rect.x, self.rect.y = position
        self.speed = speed
        self.gun = Gun((10, 10), self, bullets_img)
        self.step_counting = {'w': 0, 'a': 0, 's': 0, 'd': 0}
        self.y_velocity = 0
        self.move_x = 0
        self.reload_frame = 0
        self.last_update = time()
        self.reload = False
        self.moving = False
        self.is_jumping = False
    
    def control(self, keys) -> None:
        if not self.reload:
            if keys[K_SPACE] and not self.is_jumping:
                self.start_y = self.rect.y
                self.y_velocity = -10
                self.is_jumping = True

            if self.is_jumping:
                self.y_velocity += 1
                self.rect.y += self.y_velocity

                if self.rect.y >= self.start_y:
                    self.rect.y = self.start_y
                    self.y_velocity = 0
                    self.is_jumping = False

            if keys[K_w] and self.rect.y > H - 230:
                self.logik_move('w')
            else:
                self.hero_img = self.initial_image
            
            if keys[K_a] and self.rect.x > 0:
                self.logik_move('a')

            if keys[K_s] and self.rect.y < 365:
                self.logik_move('s')
            elif keys[K_s]:
                self.hero_img = self.initial_image

            if keys[K_d]:
                self.logik_move('d')
                self.move_x -= 5

                if self.move_x == -700:
                    self.move_x = 0

            if keys[K_r]:
                self.reload = True
            
            if keys[K_LSHIFT]:
                self.gun.shot()

            if not (keys[K_d] or keys[K_w] or keys[K_s] or keys[K_a]):
                self.step_counting = {'w': 0, 'a': 0, 's': 0, 'd': 0}
                self.hero_img = self.initial_image
        else:
            self.hero_img = self.initial_image
            current_frame = reload_gun[self.reload_frame // 5]  
            window.blit(current_frame, (self.rect.x, self.rect.y))
            
            self.reload_frame += 1
            
            if self.reload_frame >= len(reload_gun) * 5:  
                self.reload_frame = 0
                self.reload = False
        
    def logik_move(self, key: str) -> None:
        if self.step_counting[key] >= len(walking):
            self.step_counting[key] = 0
        
        # step_list = walking if key != 'a' else back_walk
        
        self.hero_img = transform.scale(
            walking[self.step_counting[key]], 
            (self.w, self.h)
        )
        self.step_counting[key] += 1 
        
        self.rect.x += self.speed if key == 'd' and self.rect.x != 200\
            else -self.speed if key == 'a' else 0
        self.rect.y += self.speed if key == 's' else\
            -self.speed if key == 'w' else 0

    def draw(self) -> None:
        print(f'Позиция игрока: <{self.rect.x, self.rect.y}>')
        window.blit(self.hero_img, (self.rect.x, self.rect.y))


class Gun(sprite.Sprite):
    def __init__(
        self,
        bullet_size: Tuple[int, int],
        player: 'Player', 
        img: str
    ):
        super().__init__()
        
        self.w, self.h = bullet_size
        self.player = player
        self.bullets = []  
        self.bullet_image = transform.scale(image.load(img), bullet_size)
        
        self.rect = self.bullet_image.get_rect()
        
        self.spawn_time = time()
        self.interval = 0.3

    def shot(self) -> None:
        current_time = time()
        
        if current_time - self.spawn_time >= self.interval:
            bullet_rect = self.bullet_image.get_rect(topleft=(self.player.rect.x + 80, self.player.rect.y + 35))
            self.bullets.append(bullet_rect)
            
            self.spawn_time = current_time

    def update_bullets(self) -> None:
        for bullet in self.bullets:
            bullet.x += 7 
            
            for zombie in zombies:
                if bullet.colliderect(zombie.rect):
                    self.bullets.remove(bullet)
                    zombies.remove(zombie)

        self.bullets = [bullet for bullet in self.bullets if bullet.left < display.get_surface().get_width()]

    def draw_bullets(self) -> None:
        for bullet in self.bullets:
            window.blit(self.bullet_image, bullet)
                