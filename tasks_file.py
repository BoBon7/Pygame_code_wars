import random

def generate_simple_task():
    tasks = [
        ("Создать переменную x со значением {}", "{}"),
        ("Написать цикл от 1 до {}", "for i in range(1, {}): pass"),
        ("Создать функцию для возврата суммы {} и {}", "def sum(a, b): return a + b"),
        ("Вывести строку 'Hello, World!'", "print('Hello, World!')"),
        ("Умножить {} на {} и вывести результат", "print({} * {})"),
        ("Создать список из {} элементов и вывести его первый элемент", "lst = list(range({})); print(lst[0])"),
        ("Написать программу, которая возвращает максимальное из {} и {}", "print(max({}, {}))"),
        ("Присвоить переменной результат выражения {} + {} и вывести его", "x = {} + {}; print(x)")
    ]
    x = random.randint(1, 10)
    y = random.randint(1, 10)
    task, solution = random.choice(tasks)
    return task.format(x, y), solution.format(x, y)

def generate_medium_task():
    tasks = [
        ("Написать функцию для нахождения факториала числа {}", "def factorial(n): return 1 if n == 0 else n * factorial(n - 1)"),
        ("Создать список из {} элементов и отсортировать его", "lst = list(range({}, 0, -1)); lst.sort(); print(lst)"),
        ("Реализовать функцию для вычисления числа Фибоначчи с номером {}", "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)"),
        ("Написать функцию для сортировки списка из {} случайных чисел", "import random; lst = [random.randint(0, 100) for _ in range({})]; lst.sort(); print(lst)"),
        ("Создать словарь с {} ключами и произвольными значениями", "dct = {{i: i+1 for i in range({})}}; print(dct)"),
        ("Реализовать программу для поиска суммы всех четных чисел до {}", "print(sum(i for i in range(1, {}) if i % 2 == 0))"),
        ("Создать список чисел и вывести сумму его элементов, кратных {}", "lst = list(range(1, 100)); print(sum(i for i in lst if i % {} == 0))"),
        ("Написать функцию для нахождения НОД чисел {} и {}", "import math; print(math.gcd({}, {}))")
    ]
    x = random.randint(3, 10)
    y = random.randint(3, 10)
    task, solution = random.choice(tasks)
    return task.format(x, y), solution.format(x, y)

def generate_hard_task():
    tasks = [
        ("Реализовать рекурсивную функцию для нахождения всех подмножеств множества", "def subsets(lst): if not lst: return [[]]; res = subsets(lst[1:]); return res + [[lst[0]] + r for r in res]"),
        ("Создать класс для описания автомобиля с атрибутами {} и методами {}", "class Car:\n    def __init__(self, {}):\n        self.{} = None\n    def {}(self):\n        pass"),
        ("Написать программу для нахождения всех простых чисел до числа {}", "def is_prime(n): return all(n % i != 0 for i in range(2, int(n**0.5)+1)); primes = [i for i in range(2, {}) if is_prime(i)]; print(primes)"),
        ("Реализовать игру 'Угадай число' с пользовательским вводом", "import random; num = random.randint(1, 100); guess = int(input('Угадайте число: ')); while guess != num: guess = int(input('Попробуйте снова: '))"),
        ("Написать программу для парсинга HTML-страницы и поиска всех ссылок", "import re; import requests; html = requests.get('http://example.com').text; links = re.findall(r'<a href=\"(.*?)\"', html); print(links)"),
        ("Создать класс 'Студент' с методами для добавления и вывода оценок", "class Student:\n    def __init__(self, name): self.name = name; self.grades = []\n    def add_grade(self, grade): self.grades.append(grade)\n    def show_grades(self): print(self.grades)"),
        ("Написать программу для поиска всех подстрок в строке", "s = 'abc'; subs = [s[i:j] for i in range(len(s)) for j in range(i+1, len(s)+1)]; print(subs)"),
        ("Реализовать задачу на обратную польскую запись", "def rpn(e): stack = []; for i in e.split(): stack.append(i) if i.isdigit() else stack.append(eval(f'{stack.pop(-2)}{i}{stack.pop()}')); return stack[0]; print(rpn('3 4 + 2 *'))")
    ]
    attr = ['марка', 'модель', 'год выпуска']
    methods = ['завести', 'остановить', 'показать характеристики']
    x = random.randint(50, 100)
    task, solution = random.choice(tasks)
    return task.format(x, random.choice(attr), random.choice(methods)), solution

def generate_task_by_level(level):
    if level <= 5:
        return generate_simple_task()
    elif 6 <= level <= 10:
        return generate_medium_task()
    else:
        return generate_hard_task()

def generate_unique_tasks(num_tasks):
    simple_tasks = set()
    medium_tasks = set()
    hard_tasks = set()

    while len(simple_tasks) < 8:
        simple_tasks.add(generate_simple_task())

    while len(medium_tasks) < 8:
        medium_tasks.add(generate_medium_task())

    while len(hard_tasks) < 8:
        hard_tasks.add(generate_hard_task())

    return list(simple_tasks) + list(medium_tasks) + list(hard_tasks)

# Генерация базы из 24 уникальных задач (по 8 каждого уровня) с ответами
tasks_base = generate_unique_tasks(24)
for idx, (task, solution) in enumerate(tasks_base, 1):
    print(f"Задача {idx}: {task}")
    print(f"Правильное решение: {solution}")
    print()
