import pygame
import sys
import random

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_SIZE = 50
ENEMY_SIZE = 30
PRIZE_SIZE = 20
PLAYER_COLOR = (0, 128, 255)
ENEMY_COLOR = (255, 0, 0)
PRIZE_COLOR = (0, 255, 0)
FPS = 60
TOTAL_PRIZES = 5  # Количество призов, необходимое для победы

#PLAYER_IMAGE = 'Dark_glassed_smile_01.png'
PLAYER_IMAGE = 'Cartoon_ant_01.png'
#ENEMY_IMAGE = 'path/to/enemy_image.png'
#PRIZE_IMAGE = 'path/to/prize_image.png'


class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load(PLAYER_IMAGE)
        self.image = pygame.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.stamina = 100  # Начальная стамина

    #        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
    def decrease_stamina(self, amount):
        self.stamina -= amount
        if self.stamina <= 0:
            self.stamina = 0
            print("Вы проиграли!")
            return True
        return False# Флаг состояния окончания игры

    def move(self, dx, dy):
#       self.rect.x += dx
#        self.rect.y += dy
        new_x, new_y = self.rect.x+dx, self.rect.y+dy

        if 0 <= new_x <= SCREEN_WIDTH - PLAYER_SIZE:
            self.rect.x = new_x
        if 0 <= new_y <= SCREEN_HEIGHT - PLAYER_SIZE:
            self.rect.y = new_y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


#        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, ENEMY_COLOR, self.rect)

class Prize:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PRIZE_SIZE, PRIZE_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, PRIZE_COLOR, self.rect)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.player = Player(0, SCREEN_HEIGHT - PLAYER_SIZE)
        self.enemies = []
        self.prizes = []
        self.prize_count = 0
        self.font = pygame.font.Font(None, 36)  # Инициализация шрифта
        self.game_over = False  # Флаг состояния окончания игры

    def run(self):
        goal_reached = False

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


            # Появление врагов и призов
            if random.randint(0, 50) == 0:
                x = random.randrange(SCREEN_WIDTH)
                y = random.randrange(SCREEN_HEIGHT)
                self.enemies.append(Enemy(x, y))
            if len(self.prizes) < TOTAL_PRIZES:
                x = random.randrange(SCREEN_WIDTH)
                y = random.randrange(SCREEN_HEIGHT)
                self.prizes.append(Prize(x, y))

            if self.game_over == False:

                self.screen.fill((50, 100, 50 ))
                self.player.draw(self.screen)
                for enemy in self.enemies:
                    enemy.draw(self.screen)
                    if self.player.rect.colliderect(enemy.rect):
                        self.enemies.remove(enemy)
                        if self.player.decrease_stamina(20):  # Уменьшение стамины и проверка на проигрыш
                            self.game_over = True


                for prize in self.prizes[:]:
                    prize.draw(self.screen)
                    if self.player.rect.colliderect(prize.rect):
                        self.prizes.remove(prize)
                        self.prize_count += 1

            else:
                self.screen.fill((255, 0, 0))  # Заливка экрана красным
                game_over_text = self.font.render('GAME OVER!', True, (255, 255, 255))
                text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(game_over_text, text_rect)

        # Отображение количества призов и стамины
            prize_text = self.font.render(f'Prizes Collected: {self.prize_count}', True, (255, 255, 255))
            self.screen.blit(prize_text, (10, 10))
            stamina_text = self.font.render(f'Stamina: {self.player.stamina}', True, (255, 255, 255))
            self.screen.blit(stamina_text, (10, 50))

            if self.prize_count >= TOTAL_PRIZES and self.player.rect.colliderect(pygame.Rect(SCREEN_WIDTH - PLAYER_SIZE, 0, PLAYER_SIZE, PLAYER_SIZE)):
                goal_reached = True

            pygame.display.flip()
            self.clock.tick(FPS)

            if goal_reached:
                print("Вы достигли цели и собрали все призы!")
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
