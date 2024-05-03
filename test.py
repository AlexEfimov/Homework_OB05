import pygame
pygame.init()
print(pygame.font.get_fonts())
# Настройки окна
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Font Example")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Очистка экрана
    screen.fill(BLACK)

    # Рендеринг текста
    for font in pygame.font.get_fonts():
        text = font.render('Hello, Pygame!', True, WHITE)
        screen.blit(text, (50, 50))

    # Обновление экрана
    pygame.display.flip()

# Завершение работы Pygame
pygame.quit()
