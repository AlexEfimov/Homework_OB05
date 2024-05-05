from abc import ABC, abstractmethod
import pygame
import sys
import random

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600  # Ширина и высота игрового поля
EXTRA_HEIGHT = 50  # Дополнительная высота для текста
TOTAL_SCREEN_HEIGHT = SCREEN_HEIGHT + EXTRA_HEIGHT  # Общая высота экрана
PLAYER_SIZE = (50, 50)
ENEMY_SIZE = (40, 40)
PRIZE_SIZE = (40, 40)
FPS = 60
TOTAL_PRIZES = 5  # Количество призов, необходимое для победы
SCORE_PER_PRIZE = 10  # Очки за каждый собранный приз
INJURY = 20  # Урон от соприкосновения с врагом
PLAYER_IMAGE = 'IMAGES/Cartoon_ant_01.png'
ENEMY_IMAGE = 'IMAGES/Spider_01.png'
PRIZE_IMAGE = 'IMAGES/strawberry-01.png'
HEADER_IMAGE = 'IMAGES/wood.png'
BG_IMAGE = 'IMAGES/grass.png'
DOOR_CLOSED = 'IMAGES/door_closed.png'
DOOR_OPENED = 'IMAGES/door_opened_01.png'
DOOR_SIZE = (50, 50)
DOOR_SOUND = 'SOUNDS/wooden-door-creaking-102413.mp3'
FONT_NAME = 'FONTS/MarkerFelt.ttc'
FONT_SIZE = 36
FONT_COLOR = (255, 255, 255)


# Определим абстрактный класс GameObject,
# который будет служить базовым классом для всех объектов в игре: Player, Enemy, Prize, Door.
class GameObject(ABC):
    def __init__(self, image_path, position, size):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=position)

    @abstractmethod
    def draw(self, screen):
        """ Отрисовка объекта на экране """
        screen.blit(self.image, self.rect)

    def update(self):
        """ Обновление состояния объекта """
        pass


class Player(GameObject):
    def __init__(self, image_path, position, size):
        super().__init__(image_path, position, size)
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

        if 0 <= new_x <= SCREEN_WIDTH - PLAYER_SIZE[0]:
            self.rect.x = new_x
        if EXTRA_HEIGHT <= new_y <= SCREEN_HEIGHT - PLAYER_SIZE[1]:
            self.rect.y = new_y

    def draw(self, screen):
        super().draw(screen)


class Enemy(GameObject):
    def __init__(self, image_path, position, size):
        super().__init__(image_path, position, size)

    def draw(self, screen):
        super().draw(screen)


class Prize(GameObject):
    def __init__(self, image_path, position, size):
        super().__init__(image_path, position, size)

    def draw(self, screen):
        super().draw(screen)


class Door(GameObject):
    def __init__(self, closed_image_path, position, size, opened_image_path):
        super().__init__(closed_image_path, position, size)
        self.closed_image = self.image
        self.opened_image = pygame.image.load(opened_image_path)
        self.opened_image = pygame.transform.scale(self.opened_image, size)
        self.is_open = False
        self.sound_manager = SoundManager()

    def open(self):
        if not self.is_open:  # Проверяем, была ли дверь уже открыта
            self.image = self.opened_image
            self.is_open = True
            self.sound_manager.play_sound('door_open')  # Воспроизведение звука открывания двери

    def close(self):
        if self.is_open:
            self.image = self.closed_image
            self.is_open = False


    def draw(self, screen):
        super().draw(screen)


class GameScreen(ABC):
    def __init__(self, width, height, bg_image, font_name, font_size, font_color, position):
        self.position = position
        self.size = (width, height)
        self.font = pygame.font.Font(font_name, font_size)
        self.font_color = font_color
        try:
            self.background = pygame.image.load(bg_image)
            self.background = pygame.transform.scale(self.background, self.size)
        except Exception as e:
            self.background = pygame.Surface(self.size)


    @abstractmethod
    def draw(self, screen):
        screen.blit(self.background, (0, 0))

class Playground(GameScreen):
    def __init__(self, width, height, bg_image, font_name, font_size, font_color, position):
        super().__init__(width, height, bg_image, font_name, font_size, font_color, position)

    def draw(self, screen):
        screen.blit(self.background, self.position)

class Header(GameScreen):
    def __init__(self, width, height, bg_image, font_name, font_size, font_color, position, score, stamina):
        super().__init__(width, height, bg_image, font_name, font_size, font_color, position)
        self.stamina = stamina
        self.score = score
        self.font_color = font_color  # (70, 30, 10)

    def draw(self, screen):
        super().draw(screen)
        stamina_text = self.font.render(f'STAMINA: {self.stamina}', True, self.font_color)
        score_text = self.font.render(f'SCORE: {self.score}', True, self.font_color)

        # Отображение стамины и очков в верхней панели
        screen.blit(stamina_text, (10, 10))  # Размещение немного ниже верхней границы
        screen.blit(score_text, (600, 10))

    def change_stamina(self, new_stamina):
        self.stamina = new_stamina

    def change_score(self, new_score):
        self.score = new_score


class LostScreen(GameScreen):
    def __init__(self, width, height, bg_image, font_name, font_size, font_color, position, score):
        super().__init__(width, height, None, font_name, font_size, font_color, position)
        self.score = score
        self.text = self.font.render(f'GAME OVER', True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.score_text = self.font.render(f'SCORE: {self.score}', True, (70, 30, 10))
        self.score_text_rect = self.score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        self.control_text = self.font.render(f'[Пробел] - продолжить, [ESC] - выйти', True, (255, 255, 255))
        self.control_text_rect = self.control_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10))


    def draw(self, screen):
        screen.fill((255, 0, 0))
        screen.blit(self.text, self.text_rect)
        screen.blit(self.score_text, self.score_text_rect)
        screen.blit(self.control_text, self.control_text_rect)

class WinScreen(GameScreen):
    def __init__(self, width, height, bg_image, font_name, font_size, font_color, position, score):
        super().__init__(width, height, bg_image, font_name, font_size, font_color, position)
        self.score = score
        self.text = self.font.render(f'Поздравляю! Вы прошли уровень!', True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.score_text = self.font.render(f'Счёт: {self.score}', True, (70, 30, 10))
        self.score_text_rect = self.score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        self.control_text = self.font.render(f'[Пробел] - продолжить, [ESC] - выйти', True, (255, 255, 255))
        self.control_text_rect = self.control_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10))


    def draw(self, screen):
        super().draw(screen)
        screen.fill((50, 100, 50))
        screen.blit(self.text, self.text_rect)
        screen.blit(self.score_text, self.score_text_rect)
        screen.blit(self.control_text, self.control_text_rect)

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            'background': pygame.mixer.Sound('SOUNDS/space-popcorn-24886.mp3'),
            'collect': pygame.mixer.Sound('SOUNDS/pop-up-something-160353.mp3'),
            'collision': pygame.mixer.Sound('SOUNDS/ahh-2-93961.mp3'),
            'door_open': pygame.mixer.Sound('SOUNDS/wooden-door-creaking-102413.mp3')
        }

    def play_sound(self, sound_name):
        self.sounds[sound_name].play()

    def play_background_music(self):
        self.sounds['background'].play(-1)


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, TOTAL_SCREEN_HEIGHT))
        self.game_screen = Playground(SCREEN_WIDTH, SCREEN_HEIGHT, BG_IMAGE, FONT_NAME, FONT_SIZE, FONT_COLOR, (0, EXTRA_HEIGHT))
        self.header = Header(SCREEN_WIDTH, EXTRA_HEIGHT, HEADER_IMAGE, FONT_NAME, FONT_SIZE, FONT_COLOR, (0, 0), 0, 0)
        self.door = Door(DOOR_CLOSED, (SCREEN_WIDTH - DOOR_SIZE[0], EXTRA_HEIGHT), DOOR_SIZE, DOOR_OPENED)
        self.player = Player(PLAYER_IMAGE, (0, SCREEN_HEIGHT - PLAYER_SIZE[1]), PLAYER_SIZE)
        self.score = 0
        self.lost_screen = LostScreen(SCREEN_WIDTH, SCREEN_HEIGHT, 'None', FONT_NAME, FONT_SIZE, FONT_COLOR, (0, 0), self.score)
        self.win_screen = WinScreen(SCREEN_WIDTH, SCREEN_HEIGHT, 'None', FONT_NAME, FONT_SIZE, FONT_COLOR, (0, 0), self.score)
        self.sound_manager = SoundManager()
        self.enemies = []
        self.prizes = []
        self.prize_count = 0
        self.game_over = False  # Флаг состояния окончания игры
        self.victory = False    # Флаг победы в игре

    def restart_game(self):
        self.enemies.clear()
        self.prizes.clear()
        self.prize_count = 0
        self.score = 0
        self.player.stamina = 100
        self.game_over = False
        self.victory = False
        self.player.rect.topleft = (0, SCREEN_HEIGHT - PLAYER_SIZE[1])
        self.door.close()

    def run(self):
        # Воспроизведение фоновой музыки
        self.sound_manager.play_background_music()
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
            self.header.draw(self.screen)
            self.game_screen.draw(self.screen)
            self.door.draw(self.screen)

            # Появление врагов и призов
            if random.randint(0, 50) == 0:
                x = random.randrange(SCREEN_WIDTH)
                y = random.randrange(EXTRA_HEIGHT, TOTAL_SCREEN_HEIGHT)
                self.enemies.append(Enemy(ENEMY_IMAGE, (x, y), ENEMY_SIZE))
            if len(self.prizes) < TOTAL_PRIZES:
                x = random.randrange(SCREEN_WIDTH)
                y = random.randrange(EXTRA_HEIGHT, TOTAL_SCREEN_HEIGHT)
                self.prizes.append(Prize(PRIZE_IMAGE, (x, y), PRIZE_SIZE))

            if not self.game_over:
                self.player.draw(self.screen)
                for enemy in self.enemies:
                    enemy.draw(self.screen)
                    if self.player.rect.colliderect(enemy.rect):
                        self.enemies.remove(enemy)                      # Удаляем противника
                        self.sound_manager.play_sound('collision')      # Воспроизведение звука при столкновении
                        status = self.player.decrease_stamina(INJURY)   # Уменьшение стамины и проверка на проигрыш
                        if status:
                            self.game_over = True  # Поднятие флага окончания игры
                            self.victory = False   # Пометить, что игрок проиграл

                for prize in self.prizes[:]:
                    prize.draw(self.screen)
                    if self.player.rect.colliderect(prize.rect):
                        self.prizes.remove(prize)                 # Удаление собранного приза
                        self.prize_count += 1                     # Подсчет собранных призов
                        self.sound_manager.play_sound('collect')  # Воспроизведение звука при сборе приза
                        self.score += SCORE_PER_PRIZE             # Увеличение счета
                        if self.prize_count >= TOTAL_PRIZES and not self.door.is_open:
                            self.door.open()  # Открываем дверь, если собрано минимальное кол-во призов

                # Изменение стамины и очков в верхней панели
                self.header.change_score(self.score)
                self.header.change_stamina(self.player.stamina)
                self.header.draw(self.screen)
                if self.prize_count >= TOTAL_PRIZES and self.player.rect.colliderect(self.door.rect):
                    self.game_over = True
                    self.victory = True
            else:
                if not self.victory:
                    self.lost_screen.draw(self.screen)
                else:
                    self.win_screen.draw(self.screen)

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
