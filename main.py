from pygame import *

init()

W, H = 700, 500

window = display.set_mode((W, H))
display.set_caption('Zombie Survaival')

clock = time.Clock()
FPS = 30

bg_img = transform.scale(image.load('images/bg.png'), (W, H))

class Player(sprite.Sprite):
    def __init__(self, x, y, w, h, speed, img, move_x):
        super().__init__()
        
        self.w, self.h = w, h
        
        self.move_x = move_x
        self.speed = speed
        self.img = transform.scale(image.load(img), (w, h))
        
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = x, y
    
    def move(self, keys):
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < H - self.rect.height:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < W - self.rect.width:
            self.move_x -= 5
    
            if self.move_x == -700:
                self.move_x = 0
                
            if self.rect.x != 200:
                self.rect.x += self.speed
    
    def draw(self):
        window.blit(self.img, (self.rect.x, self.rect.y))

bg_x = 0
sprite = Player(20, 350, 100, 50, 5, 'images/sprite.png', bg_x)

game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    window.blit(bg_img, (sprite.move_x, 0))
    window.blit(bg_img, (sprite.move_x + 700, 0))
    
    keys = key.get_pressed()
    
    sprite.draw()
    sprite.move(keys)
    
    display.update()
    clock.tick(FPS)