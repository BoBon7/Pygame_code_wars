import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Создаем экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гоночная игра")


# Создаем класс Машины
class PlayerCar:
    def __init__(self):
        self.image = pygame.Surface((50, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 120))
        self.speed = 5
        self.dx = 0
        self.dy = 0
        self.score = 0
        self.invincible = False
        self.invincible_timer = 0
        self.slowdown_timer = 0
        self.slowdown_timer = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.dx = -self.speed
        elif keys[pygame.K_d]:
            self.dx = self.speed
        else:
            self.dx = 0

        if keys[pygame.K_w]:
            self.dy = -self.speed
        elif keys[pygame.K_s]:
            self.dy = self.speed
        else:
            self.dy = 0

        # Движение игрока
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Ограничение по экрану
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        # Уменьшаем таймер неуязвимости
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False  # Неуязвимость закончилась

    def draw(self, screen):
        # Если неуязвимость активна, цвет машины меняется на зелёный
        if self.invincible:
            self.image.fill((0, 255, 0))  # Зелёный цвет при неуязвимости
        else:
            self.image.fill(WHITE)  # Стандартный цвет
        screen.blit(self.image, self.rect)


# Класс для бонусов
class Bonus:
    def __init__(self, bonus_type):
        self.bonus_type = bonus_type
        self.image = pygame.Surface((30, 30))
        if self.bonus_type == 'invincibility':
            self.image.fill((20, 255, 20))  # Зеленый для неуязвимости
        elif self.bonus_type == 'slowdown':
            self.image.fill((0, 0, 255))  # Синий для замедления
        elif self.bonus_type == 'coin':
            self.image.fill((255, 255, 0))  # Желтый для монет
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH - 50), -50))
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(50, WIDTH - 50), -50)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# Класс для препятствий
class Obstacle:
    def __init__(self):
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH - 50), -50))
        self.base_speed = 2
        self.speed = round(random.uniform(self.base_speed, self.base_speed * 1.5), 1)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(50, WIDTH - 50), -50)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def increase_difficulty(timer):
    if timer % 300 == 0:  # Каждые 5 секунд увеличивается сложность
        for obstacle in obstacles:
            obstacle.base_speed += 0.5  # Увеличение скорости препятствий
        player.speed += 0.1  # Увеличение скорости машины


def draw_interface(screen, score, speed, invincible_timer):
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    speed_text = font.render(f"Speed: {round(speed, 2)}", True, WHITE)
    invincible_text = font.render(f"Invincibility: {invincible_timer // 60}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(speed_text, (10, 50))
    screen.blit(invincible_text, (WIDTH - 200, 10))


def check_collisions(player, obstacles):
    if not player.invincible:  # Если нет неуязвимости
        for obstacle in obstacles:
            if player.rect.colliderect(obstacle.rect):
                return True  # Столкновение произошло
    return False


def check_bonus_collision(player, bonuses, obstacles):
    for bonus in bonuses[:]:
        if player.rect.colliderect(bonus.rect):
            if bonus.bonus_type == 'invincibility':
                player.invincible = True
                player.invincible_timer += 600
            elif bonus.bonus_type == 'slowdown':
                for obstacle in obstacles:
                    obstacle.speed -= 2
                player.slowdown_timer += 600
            elif bonus.bonus_type == 'coin':
                player.score += 10  # Добавляем очки
            bonuses.remove(bonus)


# Обновление препятствий с учётом временного замедления
def update_obstacle(obstacle, player):
    obstacle.update()
    if player.slowdown_timer > 0:
        player.slowdown_timer -= 1
    else:
        if obstacle.speed < 3:
            obstacle.speed += 1  # Восстановление скорости после замедления


clock = pygame.time.Clock()
player = PlayerCar()
obstacles = [Obstacle() for _ in range(5)]
bonuses = []
bonus_timer = 0

running = True
while running:
    clock.tick(FPS)
    bonus_timer += 1

    if player.invincible_timer > 0:
        player.invincible_timer -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Увеличение сложности
    increase_difficulty(pygame.time.get_ticks())

    # Обновление объектов
    player.update()
    for obstacle in obstacles:
        obstacle.update()
        update_obstacle(obstacle, player)

    if bonus_timer % 200 == 0:  # Появление бонуса каждые 3-4 секунды
        bonus_type = random.choice(['invincibility', 'slowdown', 'coin'])
        bonuses.append(Bonus(bonus_type))

    for bonus in bonuses:
        bonus.update()

    # Проверка столкновений с бонусами
    check_bonus_collision(player, bonuses, obstacles)

    # Проверка столкновений с препятствиями
    if check_collisions(player, obstacles):
        print("Игра окончена!")  # Здесь можно добавить логику окончания игры
        running = False

    # Рендеринг объектов
    screen.fill(BLACK)
    player.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)
    for bonus in bonuses:
        bonus.draw(screen)

    # Отрисовка интерфейса
    draw_interface(screen, player.score, obstacle.base_speed, player.invincible_timer)
    pygame.display.flip()

pygame.quit()
