from random import randint

import pygame

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
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    def __init__(self) -> None:
        self.position = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.body_color = None

    def draw(self) -> None:
        pass


class Apple(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = (255, 0, 0)
        self.randomize_position()

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    # Создание случайной позиции яблока.
    def randomize_position(self) -> None:
        rand_x = randint(0, GRID_WIDTH-1)*GRID_SIZE
        rand_y = randint(0, GRID_HEIGHT-1)*GRID_SIZE
        self.position = (rand_x, rand_y)


class Snake(GameObject):
    def __init__(self):
        super().__init__()
        # Стандартная длинна.
        self.length = 1
        # Длинна сравнения
        self.new_length = self.length
        # Массив позиций частей змейки.
        self.positions = [self.position]
        self.direction = (1, 0)
        self.next_direction = None
        self.body_color = (0, 255, 0)
        self.last = None

    def update_direction(self) -> None:
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    # Двигаем змейку.
    def move(self) -> None:
        # Корректируем длинну направления.
        new_direction = [vector * 20 for vector in self.direction]
        # Обновлённая позиция головы.
        self.last = self.positions[-1]
        # Получаем картеж с движением.
        direction_x = self.positions[0][0] + new_direction[0]
        direction_y = self.positions[0][1] + new_direction[1]
        full_direction = (direction_x, direction_y)

        # Проверка увеличения длинны.
        if self.length > self.new_length:
            self.positions.insert(0, full_direction)
            self.new_length += 1
        # Если длинна не изменилась.
        elif self.length == self.new_length:
            self.positions.insert(0, full_direction)
            self.positions.pop()
        else:
            self.positions.pop()

        self.check_edges()

    # Проверка граней.
    def check_edges(self):
        """
        Проверяем части змейки на выход за зону
        """
        for position in self.positions:
            # Если за правой границей
            if position[0] >= SCREEN_WIDTH:
                self.positions.pop(0)
                self.positions.insert(0, (0, position[1]))

            # Если за левой границей
            if position[0] < 0:
                self.positions.pop(0)
                width = SCREEN_WIDTH - GRID_SIZE
                self.positions.insert(0, (width, position[1]))

            # Если за нижней границей
            if position[1] >= SCREEN_HEIGHT:
                self.positions.pop(0)
                self.positions.insert(0, (position[0], 0))

            # Если за верхней границей
            if position[1] < 0:
                self.positions.pop(0)
                height = SCREEN_HEIGHT - GRID_SIZE
                self.positions.insert(0, (position[0], height))

    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.positions = [self.position]


def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def draw_bg() -> None:
    new_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, new_rect)


def main() -> None:
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    # Прорисовываем первое яблоко
    apple.draw()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка на съеденное яблоко.
        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position()
            apple.draw()

        # Проверяем смерть змейки.
        if snake.get_head_position() in snake.positions[1:]:
            draw_bg()
            apple.randomize_position()
            apple.draw()
            snake.reset()

        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
