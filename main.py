import pygame
import sys
import random

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600  # Ширина и высота игрового поля
EXTRA_HEIGHT = 50  # Дополнительная высота для текста
TOTAL_SCREEN_HEIGHT = SCREEN_HEIGHT + EXTRA_HEIGHT  # Общая высота экрана
PLAYER_SIZE = 50
ENEMY_SIZE = 40
PRIZE_SIZE = 40
FPS = 60
TOTAL_PRIZES = 5  # Количество призов, необходимое для победы
SCORE_PER_PRIZE = 10  # Очки за каждый собранный приз
PLAYER_IMAGE = 'IMAGES/Cartoon_ant_01.png'
ENEMY_IMAGE = 'IMAGES/Spider_01.png'
PRIZE_IMAGE = 'IMAGES/strawberry-01.png'
HEADER_IMAGE = 'IMAGES/wood.png'
BACKGROUND_IMAGE = 'IMAGES/grass.png'
DOOR_CLOSED = 'IMAGES/door_closed.png'
DOOR_OPENED = 'IMAGES/door_opened_01.png'
DOOR_SIZE = (50, 50)
DOOR_SOUND = 'SOUNDS/'
FONT_NAME = 'FONTS/MarkerFelt.ttc'
FONT_SIZE = 36


class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load(PLAYER_IMAGE)
        self.image = pygame.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.stamina = 100  # Начальная стамина

    def decrease_stamina(self, amount):
        self.stamina -= amount
        if self.stamina <= 0:
            self.stamina = 0
            print("Вы проиграли!")
            return True
        return False  # Флаг состояния окончания игры

    def move(self, dx, dy):
        new_x, new_y = self.rect.x + dx, self.rect.y + dy

        if 0 <= new_x <= SCREEN_WIDTH - PLAYER_SIZE:
            self.rect.x = new_x
        if EXTRA_HEIGHT <= new_y <= TOTAL_SCREEN_HEIGHT - PLAYER_SIZE:
            self.rect.y = new_y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load(ENEMY_IMAGE)
        self.image = pygame.transform.scale(self.image, (ENEMY_SIZE, ENEMY_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Prize:
    def __init__(self, x, y):
        self.image = pygame.image.load(PRIZE_IMAGE)
        self.image = pygame.transform.scale(self.image, (PRIZE_SIZE, PRIZE_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Door:
    def __init__(self, door_closed_path, door_opened_path, door_size, x, y):
        self.closed_image = pygame.image.load(door_closed_path)
        self.closed_image = pygame.transform.scale(self.closed_image, door_size)
        self.open_image = pygame.image.load(door_opened_path)
        self.open_image = pygame.transform.scale(self.open_image, door_size)
        self.image = self.closed_image  # Изначально дверь закрыта
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.is_open = False

    def open(self):
        if not self.is_open:  # Проверяем, была ли дверь уже открыта
            self.image = self.open_image
            self.is_open = True
            game.door_open_sound.play()  # Воспроизведение звука открывания двери

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, TOTAL_SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.player = Player(0, SCREEN_HEIGHT - PLAYER_SIZE + EXTRA_HEIGHT)
        self.enemies = []
        self.prizes = []
        self.prize_count = 0
        self.score = 0
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)  # Инициализация шрифта
        self.game_over = False  # Флаг состояния окончания игры
        self.victory = False  # Флаг победы в игре
        pygame.mixer.init()  # Инициализация микшера
        pygame.mixer.music.load('SOUNDS/space-popcorn-24886.mp3')  # Загрузка фоновой музыки
        pygame.mixer.music.play(-1)  # Воспроизведение музыки на повторе
        self.collect_sound = pygame.mixer.Sound('SOUNDS/pop-up-something-160353.mp3')
        self.collision_sound = pygame.mixer.Sound('SOUNDS/ahh-2-93961.mp3')
        self.header_bg = pygame.image.load(HEADER_IMAGE)
        self.header_bg = pygame.transform.scale(self.header_bg, (SCREEN_WIDTH, EXTRA_HEIGHT))
        self.background_image = pygame.image.load(BACKGROUND_IMAGE)
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.door = Door(DOOR_CLOSED, DOOR_OPENED, DOOR_SIZE, SCREEN_WIDTH - 50, 50)  # Позиция двери
        self.door_open_sound = pygame.mixer.Sound('SOUNDS/wooden-door-creaking-102413.mp3')  # Загрузка звука открывания двери

    def restart_game(self):
        self.enemies.clear()
        self.prizes.clear()
        self.prize_count = 0
        self.score = 0
        self.player.stamina = 100
        self.game_over = False
        self.victory = False
        self.player.rect.topleft = (0, SCREEN_HEIGHT - PLAYER_SIZE + EXTRA_HEIGHT)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move(-5, 0)
            if keys[pygame.K_RIGHT]:
                self.player.move(5, 0)
            if keys[pygame.K_UP]:
                self.player.move(0, -5)
            if keys[pygame.K_DOWN]:
                self.player.move(0, 5)

            # Отрисовка фонового изображения
            self.screen.blit(self.background_image, (0, EXTRA_HEIGHT))
            self.door.draw(self.screen)  # Отрисовка двери
            # Появление врагов и призов
            if random.randint(0, 50) == 0:
                x = random.randrange(SCREEN_WIDTH)
                y = random.randrange(EXTRA_HEIGHT, TOTAL_SCREEN_HEIGHT)
                self.enemies.append(Enemy(x, y))
            if len(self.prizes) < TOTAL_PRIZES:
                x = random.randrange(SCREEN_WIDTH)
                y = random.randrange(EXTRA_HEIGHT, TOTAL_SCREEN_HEIGHT)
                self.prizes.append(Prize(x, y))

            if not self.game_over:
                self.screen.blit(self.header_bg, (0, 0))
                self.player.draw(self.screen)
                for enemy in self.enemies:
                    enemy.draw(self.screen)
                    if self.player.rect.colliderect(enemy.rect):
                        self.enemies.remove(enemy)
                        self.collision_sound.play()  # Воспроизведение звука при столкновении
                        if self.player.decrease_stamina(20):  # Уменьшение стамины и проверка на проигрыш
                            self.game_over = True
                            self.victory = False   # Пометить, что игрок проиграл

                for prize in self.prizes[:]:
                    prize.draw(self.screen)
                    if self.player.rect.colliderect(prize.rect):
                        self.prizes.remove(prize)
                        self.prize_count += 1
                        self.collect_sound.play()  # Воспроизведение звука при сборе
                        self.score += SCORE_PER_PRIZE
                        if self.prize_count >= TOTAL_PRIZES and not self.door.is_open:
                            self.door.open()  # Открываем дверь, если собраны все приз

                # Отображение стамины и очков в верхней панели
                stamina_text = self.font.render(f'STAMINA: {self.player.stamina}', True, (70, 30, 10))
                score_text = self.font.render(f'SCORE: {self.score}', True, (70, 30, 10))
                self.screen.blit(stamina_text, (10, 10))  # Размещение немного ниже верхней границы
                self.screen.blit(score_text, (600, 10))

            #    if (self.prize_count >= TOTAL_PRIZES and
            #        self.player.rect.colliderect(pygame.Rect(SCREEN_WIDTH - PLAYER_SIZE,
            #                                                 EXTRA_HEIGHT, PLAYER_SIZE, PLAYER_SIZE))):
                if self.prize_count >= TOTAL_PRIZES and self.player.rect.colliderect(self.door.rect):
                    self.victory = True
                    self.game_over = True

            else:
                if not self.victory:

                    self.screen.fill((255, 0, 0))  # Заливка экрана красным
                    game_over_text = self.font.render('GAME OVER!', True, (255, 255, 255))
                    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
                    self.screen.blit(game_over_text, text_rect)

                else:
                    self.screen.fill((75, 150, 75))  # Зеленый фон для финального экрана
                    victory_text = self.font.render('Congratulations! Level Completed!', True, (0, 255, 255))
                    score_text = self.font.render(f'Your Score: {self.score}', True, (0, 255, 255))
                    # Расположение текста по центру экрана
                    victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
                    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
                    self.screen.blit(victory_text, victory_rect)
                    self.screen.blit(score_text, score_rect)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
                if keys[pygame.K_SPACE]:
                    self.restart_game()  # Функция для рестарта игры

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
