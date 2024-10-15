import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 1400, 800
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
        self.image = pygame.image.load("rocket.png")
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 120))
        self.speed = 6
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
            self.image = pygame.image.load("rocket-invincible.png")
        else:
            self.image = pygame.image.load("rocket.png")
        screen.blit(self.image, self.rect)


# Класс для бонусов
class Bonus:
    def __init__(self, bonus_type):
        self.bonus_type = bonus_type
        if self.bonus_type == 'invincibility':
            self.image = pygame.image.load("guard.png")
        elif self.bonus_type == 'slowdown':
            self.image = pygame.image.load("back-in-time.png")
        elif self.bonus_type == 'coin':
            self.image = pygame.image.load("dollar.png")
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH - 50), -50))
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(50, WIDTH - 50), -50)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Bullet:
    def __init__(self, x, y):
        self.image = pygame.image.load("laser.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed  # Движение вверх
        if self.rect.bottom < 0:
            return False  # Снаряд исчезает при выходе за экран
        return True

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def update_bullets(bullets, bonuses, obstacles):
    for bullet in bullets[:]:
        if not bullet.update():
            bullets.remove(bullet)

        # Проверяем столкновения с бонусами
        for bonus in bonuses[:]:
            if bullet.rect.colliderect(bonus.rect):
                bonuses.remove(bonus)  # Уничтожаем бонус
                bullets.remove(bullet)  # Уничтожаем снаряд
                break  # Выходим, так как снаряд уже уничтожен

        # Проверяем столкновения с препятствиями
        for obstacle in obstacles[:]:
            if bullet.rect.colliderect(obstacle.rect):
                obstacles.remove(obstacle)  # Уничтожаем препятствие
                obstacles.append(Obstacle())
                bullets.remove(bullet)  # Уничтожаем снаряд
                break  # Выходим, так как снаряд уже уничтожен


# Класс для препятствий
class Obstacle:
    def __init__(self):
        self.image = pygame.image.load("ufo.png")
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH - 50), -50))
        self.base_speed = 1
        self.speed = round(random.uniform(self.base_speed, self.base_speed * 1.5), 2)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(50, WIDTH - 50), -50)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont(None, 48)
        self.color = WHITE

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.rect.x + 20, self.rect.y + 20))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# Функция для стартового экрана
def main_menu():
    global game_mode
    play_button = Button(WIDTH // 2 - 150 // 2, HEIGHT // 2 - 50, 150, 80, "Играть")
    exit_button = Button(WIDTH // 2 - 150 // 2, HEIGHT // 2 + 50, 150, 80, "Выйти")
    menu_running = True

    while menu_running:
        screen.fill(BLACK)
        play_button.draw(screen)
        exit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.is_clicked(event.pos):
                    game_mode = "game"
                    return
                if exit_button.is_clicked(event.pos):
                    pygame.quit()
                    quit()

        pygame.display.flip()
        clock.tick(FPS)


def reset():
    global player, obstacles, bonuses, bullets, bonus_timer
    player = PlayerCar()
    obstacles = [Obstacle() for _ in range(5)]
    bonuses = []
    bullets = []
    bonus_timer = 0


def lose_menu():
    global game_mode
    play_button = Button(WIDTH // 2 - 270 // 2, HEIGHT // 2 - 50, 270, 80, "Играть снова")
    exit_button = Button(WIDTH // 2 - 150 // 2, HEIGHT // 2 + 50, 150, 80, "Выйти")
    menu_running = True

    while menu_running:
        screen.fill(BLACK)
        play_button.draw(screen)
        exit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.is_clicked(event.pos):
                    game_mode = "game"
                    reset()
                    return
                if exit_button.is_clicked(event.pos):
                    pygame.quit()
                    quit()

        pygame.display.flip()
        clock.tick(FPS)


def increase_difficulty(timer):
    if timer % 300 == 0:  # Каждые 5 секунд увеличивается сложность
        for obstacle in obstacles:
            obstacle.base_speed += 0.4  # Увеличение скорости препятствий
        player.speed += 0.15  # Увеличение скорости машины
        player.score += 5


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
                    obstacle.speed /= 2
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
        if obstacle.speed < obstacle.base_speed:
            obstacle.speed += abs(obstacle.base_speed - obstacle.speed)  # Восстановление скорости после замедления


clock = pygame.time.Clock()
player = PlayerCar()
obstacles = [Obstacle() for _ in range(5)]
bonuses = []
bullets = []
bonus_timer = 0

game_mode = "menu"
running = True
while running:
    if game_mode == "menu":
        main_menu()
    elif game_mode == "lose":
        lose_menu()
    clock.tick(FPS)
    bonus_timer += 1

    if player.invincible_timer > 0:
        player.invincible_timer -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Стрельба левой кнопкой мыши
            bullet = Bullet(player.rect.centerx, player.rect.top)
            bullets.append(bullet)

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
    update_bullets(bullets, bonuses, obstacles)

    # Проверка столкновений с препятствиями
    if check_collisions(player, obstacles):
        game_mode = "lose"

    # Рендеринг объектов
    screen.fill(BLACK)
    player.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)
    for bonus in bonuses:
        bonus.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)

    # Отрисовка интерфейса
    draw_interface(screen, player.score, obstacles[0].base_speed, player.invincible_timer)
    pygame.display.flip()

pygame.quit()
