from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:

speed = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка || shift - спринт, 1/2/3 - смена скорости')


# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """Базовый класс объектов игры."""

    def __init__(self, color) -> None:
        """инизиализация Объекта"""
        self.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.body_color = color

    # Заготовка под функцию для наследования
    def draw(self) -> None:
        """заготовка"""
        raise NotImplementedError('Метод draw() должен быть реализован')


class Apple(GameObject):
    """
    Класс яблока.

    Увеличивающий длинну змейки при съедении.
    Имеет случайную позицию.
    """

    # инизиализация яблока
    def __init__(self, color, snake_position):
        super().__init__(color)
        self.randomize_position(snake_position)
        self.draw()

    def draw(self):
        """Отрисовка яблока на поле."""
        # Создание квадрата
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        # Отрисовка
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, snake_position) -> None:
        """Создание случайной позиции яблока."""
        if snake_position is None:
            snake_position = []

        while True:
            # Если объединить rand_x и rand_y, то строка будет длинне 79,
            # и не будет выполнять pep8
            rand_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            rand_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            # создаем новую позицию
            full_position = (rand_x, rand_y)
            if full_position not in snake_position:
                self.position = full_position
                break


class Snake(GameObject):
    """
    Класс змея.
    Управляется игроком,
    Меняет направление.
    """

    # Инизиализирует змею
    def __init__(self, color):
        super().__init__(color)
        self.reset()
        self.next_direction = None
        self.last = None

    def update_direction(self) -> None:
        """Изменяет напрвавление."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Движение Змейки."""
        d_x, d_y = self.direction
        h_x, h_y = self.positions[0]
        self_x = (h_x + (d_x * GRID_SIZE)) % SCREEN_WIDTH
        self_y = (h_y + (d_y * GRID_SIZE)) % SCREEN_HEIGHT
        self.position = (self_x, self_y)
        self.positions.insert(0, self.position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовка змейки и затирание последнего объекта."""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает первый элемент змеи."""
        return self.positions[0]

    def reset(self):
        """Возвращает в обычное состояние игру."""
        self.length = 1
        # Длинна сравнения
        self.new_length = self.length
        # Массив позиций частей змейки.
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT


def handle_keys(game_object):
    """Управление движением.

    Не смог додуматься как сделать закрытие на ESC,
    без получения ошибки
    ./the_snake.py:162:1: C901 'handle_keys' is too complex (15).
    """

    global speed
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_1:
                speed = 5
            elif event.key == pg.K_2:
                speed = 10
            elif event.key == pg.K_3:
                speed = 20
            elif event.key == pg.K_LSHIFT:
                speed *= 2

        if event.type == pg.KEYUP:
            if event.key == pg.K_LSHIFT:
                speed /= 2


def main():
    """Основная функция программы."""
    # Инициализация pg:
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR, snake.positions)
    # Прорисовываем первое яблоко
    while True:
        clock.tick(speed)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка на съеденное яблоко.
        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Проверяем смерть змейки.
        elif snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
