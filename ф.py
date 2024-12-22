import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Game")

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Класс для зомби
class Zombie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(1, 3)

    def move(self):
        self.x -= self.speed  # Двигаемся влево по оси X

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 50, 50))

# Список для зомби
zombies = []

# Время последнего спауна
last_spawn_time = time.time()

# Интервал спауна (например, 10 секунд)
spawn_interval = 3

# Основной цикл игры
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Получаем текущее время
    current_time = time.time()

    # Проверяем, прошло ли достаточно времени для спауна
    if current_time - last_spawn_time >= spawn_interval:
        zombies.append(Zombie(WIDTH, random.randint(0, HEIGHT - 50)))
        last_spawn_time = current_time  # Обновляем время последнего спауна

    # Двигаем зомби и отрисовываем
    for zombie in zombies:
        zombie.move()
        zombie.draw()

    # Убираем зомби, которые вышли за экран
    zombies = [z for z in zombies if z.x > 0]

    # Обновление экрана
    pygame.display.flip()

    # Ограничиваем частоту кадров
    clock.tick(60)

pygame.quit()
