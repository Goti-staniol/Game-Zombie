from cfg import (
    W, H,
    walk_right,
    idle
)

from pygame import *
from time import time

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


class Zombie(sprite.Sprite):
    def __init__(self, x, y, w, h, speed, img):
        super().__init__()
        
        self.w, self.h = w, h
        
        self.speed = speed
        
        self.img = transform.scale(image.load(img), (w, h))
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = x, y
        
    
    def draw(self):
        window.blit(self.img, (self.rect.x, self.rect.y))
    
    def move(self):
        self.rect.x -= self.speed


class Guns(sprite.Sprite):
    def __init__(self, x, y, w, h, speed, img, sprite):
        super().__init__()
        
        self.w, self.h = w, h
        
        self.speed = speed
        
        self.img = transform.scale(image.load(img), (w, h))
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = x, y
    
    def shoot(self, keys):
        if keys[K_z]:
            for zombie in zombies:
                x, y = zombie.rect.x, zombie.rect.y
                
                if self.rect.x == x and self.rect.y == y:
                    print('Попал')


class Player(sprite.Sprite):
    def __init__(self, x, y, w, h, speed, img):
        super().__init__()
        
        self.w, self.h = w, h
        
        self.is_run = False
        
        self.start_img = img
        
        self.move_x = 0
        self.speed = speed
        self.img = transform.scale(image.load(img), (w, h))
        
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = x, y
        
        self.count = 0
        self.count_is_run = 0
        
        self.last_update = time()
        
        self.moving = False
        
        self.y_velocity = 0
        self.is_jumping = False
    
    def move(self, keys):
        if self.moving:
            self.last_update = time()
            
            if keys[K_w] and self.rect.y > 230:
                self.rect.y -= self.speed
            if keys[K_s] and self.rect.y < H - 140:
                self.rect.y += self.speed
            if keys[K_a] and self.rect.x > 0:
                self.rect.x -= self.speed
            
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
            
            if keys[K_d] and self.rect.x < W - self.rect.width:
                self.img = transform.scale(
                    walk_right[self.count], 
                    (self.rect.width, self.rect.height)
                )
                self.count += 1
                
                if self.count >= 5:
                    self.count = 0
                
                self.move_x -= 5
                
                if self.move_x == -700:
                    self.move_x = 0
                    
                if self.rect.x != 200:
                    self.rect.x += self.speed
            else:
                self.count = 0
                
                self.img = transform.scale(
                    image.load(self.start_img),
                    (self.rect.width, self.rect.height)
                )
        else:
            if keys[K_w]:
                self.moving = True
            elif keys[K_s]:
                self.moving = True
            elif keys[K_a]:
                self.moving = True
            elif keys[K_d]:
                self.moving = True
            else:
                self.moving = False
               
                if not self.moving:
                    current_time = time()
                    if current_time - self.last_update > 0.3:  # задержка на смену картинки
                        self.count_is_run += 1
                        if self.count_is_run >= 2:
                            self.count_is_run = 0
                        self.img = transform.scale(
                            idle[self.count_is_run], 
                            (self.w, self.h)
                        )
                        self.last_update = current_time 
               
    def draw(self):
        window.blit(self.img, (self.rect.x, self.rect.y))