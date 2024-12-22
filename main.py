from pygame import *
import pygame

from time import sleep, time

from random import random, randint

init()

W, H = 700, 500

window = display.set_mode((W, H))
display.set_caption('Zombie Survaival')

clock = pygame.time.Clock()
FPS = 30

bg_img = transform.scale(image.load('images/bg.png'), (W, H))

spawn_time = time() 
spawn_interval = 3

walk_right = [
    image.load('images/p_right/one.png'),
    image.load('images/p_right/two.png'),
    image.load('images/p_right/three.png'),
    image.load('images/p_right/four.png'),
    image.load('images/p_right/five.png'),
    image.load('images/p_right/six.png')
    
]

walk_left = [
    image.load('images/p_right/one.png'),
    image.load('images/p_right/two.png'),
    image.load('images/p_right/three.png'),
    image.load('images/p_right/four.png'),
    image.load('images/p_right/five.png'),
    image.load('images/p_right/six.png')
    
]

zombies = []


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
    
    def shoot(self):
        if keys[K_z]:
            for zombie in zombies:
                x, y = zombie.rect.x, zombie.rect.y
                
                if self.rect.x == x and self.rect.y == y:
                    print('Попал')


class Player(sprite.Sprite):
    def __init__(self, x, y, w, h, speed, img):
        super().__init__()
        
        self.w, self.h = w, h
        
        self.start_img = img
        
        self.move_x = 0
        self.speed = speed
        self.img = transform.scale(image.load(img), (w, h))
        
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = x, y
        
        self.count = 0
        
        self.y_velocity = 0
        self.is_jumping = False
    
    def move(self, keys):
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < H - self.rect.height:
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
            
        
    def draw(self):
        window.blit(self.img, (self.rect.x, self.rect.y))

sprite = Player(20, 350, 50, 50, 3, 'images/player_sprite.png')

game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    keys = key.get_pressed()
    
    window.blit(bg_img, (sprite.move_x, 0))
    window.blit(bg_img, (sprite.move_x + 700, 0))
    
    sprite.draw()
    sprite.move(keys)
    
    current_time = time()
    
    if current_time - spawn_time >= spawn_interval:
        y = randint(330, 385)
        zombies.append(Zombie(650, y, 50, 50, 1, 'images/player_sprite.png'))
        
        spawn_time = current_time
        
        if spawn_interval != 1:
            spawn_interval -= 1
       
    for zombie in zombies:
        zombie.draw()
        zombie.move()
        
    display.update()
    clock.tick(FPS)