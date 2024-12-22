import pygame

# Инициализация Pygame
pygame.init()

# Задаем размеры экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Загружаем изображение персонажа
character = pygame.image.load('images/bg.png')  # Убедитесь, что файл существует в вашем каталоге
character_rect = character.get_rect()  # Получаем прямоугольник для персонажа

# Начальная позиция персонажа
x_position = 100
y_position = 250

# Скорость движения персонажа
speed = 5

# Главный игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновляем позицию персонажа
    x_position += speed  # Двигаем персонажа вправо

    # Если персонаж выходит за экран, возвращаем его на начало
    if x_position > screen_width:
        x_position = 0

    # Обновляем прямоугольник для нового положения
    character_rect.topleft = (x_position, y_position)

    # Заполнение экрана черным цветом
    screen.fill((0, 0, 0))

    # Отображаем персонажа на экране
    screen.blit(character, character_rect)

    # Обновляем экран
    pygame.display.flip()

    # Устанавливаем частоту обновления экрана
    pygame.time.Clock().tick(60)

# Завершаем работу Pygame
pygame.quit()
