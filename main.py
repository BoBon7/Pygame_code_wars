import pygame
import time

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 1000, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Code Collector")
# correct_sound = pygame.mixer.Sound('correct.wav')
# wrong_sound = pygame.mixer.Sound('wrong.wav')

# Шрифты
font = pygame.font.SysFont(None, 40)


def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


class Game:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.time_limit = 60  # начальное время для каждого уровня
        self.bonus_time = 0
        self.bonuses = {"hint": 1, "extra_time": 1}
        self.tasks = []
        self.load_tasks()
        self.running = True
        self.input_text = ""

    def load_tasks(self):
        # Задания
        self.tasks = [Task("Create a variable 'x' equal to 5", "x = 5"),
                      Task("Write a for loop from 1 to 10", "for i in range(1, 11):"),
                      Task("Create a function that returns the sum of two numbers",
                           "def sum(a, b): return a + b")]

    def start_level(self):
        current_task = self.tasks[self.level - 1]
        start_time = time.time()

        while self.running:
            screen.fill(WHITE)
            draw_text(f"Level {self.level}: {current_task.text}", font, BLACK, 20, 20)
            elapsed_time = time.time() - start_time
            remaining_time = self.time_limit + self.bonus_time - elapsed_time
            if remaining_time <= 0:
                print("Time's up!")
                self.end_game()
                return

            draw_text(f"Time: {int(remaining_time)}s", font, BLACK, 20, 100)
            draw_text(f"Score: {self.score}", font, BLACK, 20, 150)
            draw_text(f"Bonuses: Hint({self.bonuses['hint']}), Extra Time({self.bonuses['extra_time']})", font, BLACK,
                      20, 250)
            draw_text(f"Your code: {self.input_text}", font, BLACK, 20, 300)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h and self.bonuses["hint"] > 0:
                        self.bonuses["hint"] -= 1
                        print(f"Hint: {current_task.get_hint()}")
                    elif event.key == pygame.K_t and self.bonuses["extra_time"] > 0:
                        self.bonuses["extra_time"] -= 1
                        self.bonus_time += self.time_limit * 0.2
                    elif event.key == pygame.K_RETURN:
                        if current_task.check_answer(self.input_text):
                            print("Correct!")
                            self.score += self.level
                            self.input_text = ""
                            self.time_limit += 1
                            self.level_up()
                            # correct_sound.play()
                        else:
                            print("Try again.")
                            # wrong_sound.play()
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode

    def save_progress(self):
        with open('progress.txt', 'w') as f:
            f.write(f"Level: {self.level}, Score: {self.score}\n")

    def end_game(self):
        print(f"Your score: {self.score}")
        self.save_progress()
        self.running = False
        pygame.quit()

    def level_up(self):
        self.level += 1
        if self.level > len(self.tasks):
            print("You won!")
            self.end_game()
        else:
            self.start_level()


class Task:
    def __init__(self, text, correct_answer):
        self.text = text
        self.correct_answer = correct_answer

    def check_answer(self, answer):
        return answer == self.correct_answer

    def get_hint(self):
        # Возвращаем простую подсказку
        return "Think about using a variable or a loop."


# Запуск игры
game = Game()
game.start_level()
