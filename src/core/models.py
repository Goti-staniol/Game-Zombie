from cfg import (
    W, H,
    walking,
    idle,
)

from pygame import *

from time import time
from random import randint

window = display.set_mode((W, H))
display.set_caption('Zombie Survaival')

zombies = []


class Buttons(sprite.Sprite):
    def __init__(self, x, y, w, h, img):
        super().__init__()
        
        self.img = transform.scale(image.load(img), (w, h))
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = x, y
    
    def draw(self):
        window.blit(self.img, (self.rect.x, self.rect.y))


class ZombieModel(sprite.Sprite):
    def __init__(self, w, h, speed):
        super().__init__()
        
        self.img = transform.scale(
            image.load('src/images/player_sprite.png'), 
            (w, h)
        )
        
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = 650, randint(330, 385)
        
        self.speed = speed

    def move(self):
        self.rect.x -= self.speed
    
    def draw(self):
        window.blit(self.img, (self.rect.x, self.rect.y))


class Zombie(ZombieModel):
    def __init__(self, w, h, speed):
        super().__init__(w, h, speed)
        
        self.spawn_time = time()

    def add_zombie(self):
        current_time = time()
                
        if current_time - self.spawn_time >= 3:
            zombies.append(
                ZombieModel(
                    100,
                    100,
                    2
                )
            )
            
            self.spawn_time = current_time
    
    def update(self):
        for zombie in zombies:
            zombie.draw()
            zombie.move() 

class Player(sprite.Sprite):
    def __init__(self, x, y, w, h, speed, hero_img):
        self.initial_image = transform.scale(image.load(hero_img), (w, h))
        
        self.hero_img = transform.scale(image.load(hero_img), (w, h))
        
        self.x, self.y = x, y
        
        self.rect = self.hero_img.get_rect()
        self.w, self.h = w, h
        self.rect.x, self.rect.y = x, y
        
        self.speed = speed
        
        self.step_counting_w = 0
        self.step_counting_s = 0
        self.step_counting_d = 0
        
        self.y_velocity = 0
        self.move_x = 0
        
        self.last_update = time()
        
        self.reload = False
        self.moving = False
        self.is_jumping = False
    
    def control(self, keys):
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
                    
            if keys[K_d] and self.rect.x < W - self.w:
                if self.step_counting_d >= len(walking):
                    self.step_counting_d = 0
                
                self.hero_img = transform.scale(
                    walking[self.step_counting_d], 
                    (self.w, self.h)
                )
                
                self.step_counting_d += 1
                self.move_x -= 5
                
                if self.move_x == -700:
                    self.move_x = 0
                    
                if self.rect.x != 200:
                    self.rect.x += self.speed

            if keys[K_w] and self.rect.y > 230:
                if self.step_counting_w >= len(walking):
                    self.step_counting_w = 0
                
                self.hero_img = transform.scale(
                    walking[self.step_counting_w], 
                    (self.w, self.h)
                )
                
                self.step_counting_w += 1
                self.rect.y -= self.speed
            
            if keys[K_s] and self.rect.y < H - 140:
                if self.step_counting_s >= len(walking):
                    self.step_counting_s = 0
                
                self.hero_img = transform.scale(
                    walking[self.step_counting_s], 
                    (self.w, self.h)
                )
                
                self.step_counting_s += 1
                
                self.rect.y += self.speed
            
            if not (keys[K_d] or keys[K_w] or keys[K_s]):
                self.step_counting_w = 0
                self.step_counting_s = 0
                self.step_counting_d = 0

                self.hero_img = self.initial_image

            if keys[K_a] and self.rect.x > 0:
                self.rect.x -= self.speed
               
    def draw(self):
        window.blit(self.hero_img, (self.rect.x, self.rect.y))


class Gun(sprite.Sprite):
    def __init__(self, w, h, player: Player, img):
        super().__init__()
        
        self.w, self.h = w, h
        self.player = player
        self.bullets = []  
        self.bullet_image = transform.scale(image.load(img), (w, h))
        
        self.rect = self.bullet_image.get_rect()
        
        self.spawn_time = time()
        self.interval = 0.3

    def shot(self, keys):
        if keys[K_LSHIFT]:
            current_time = time()
            
            if current_time - self.spawn_time >= self.interval:
                bullet_rect = self.bullet_image.get_rect(topleft=(self.player.rect.x + 80, self.player.rect.y + 35))
                self.bullets.append(bullet_rect)
                
                self.spawn_time = current_time

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.x += 7 
            
            for zombie in zombies:
                if bullet.colliderect(zombie.rect):
                    self.bullets.remove(bullet)
                    zombies.remove(zombie)

        self.bullets = [bullet for bullet in self.bullets if bullet.left < display.get_surface().get_width()]

    def draw_bullets(self, window):
        for bullet in self.bullets:
            window.blit(self.bullet_image, bullet)
                



        
        