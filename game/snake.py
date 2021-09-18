import pygame
import time
import random

pygame.init()

# constant
width = 1200
height = 780
speed_game = 100

pink = (255, 182, 193)
yellow = (173, 255, 47)
black = (0, 0, 0)
red = (213, 50, 80)
white = (255, 255, 255)
steelblue = (70, 130, 180)

segment_size = 30
head_x = width // 2 // segment_size * segment_size
head_y = height // 2 // segment_size * segment_size

list_segments_snake = [[head_x, head_y]]
count_segments_snake = 1

display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake game')


class Snake(object):

    def __init__(self, color_main, color_circuit, size, head_x, head_y):
        self.color_main = color_main        # Основной цвет змейки
        self.color_circuit = color_circuit  # Цвет контура змейки, для ее видимости на поле (ну и для красоты)
        self.size = size                    # Размер сегмента змейки
        self.head_x = head_x                # Положение головного сегмента змейки по оси X
        self.head_y = head_y                # Положение головного сегмента змейки по оси Y
        self.speed_x = 0                    # Изменчивая переменная объекта, проекция скорости перемещения змейки по X
        self.speed_y = 0                    # Проекция скорости перемещения змейки по оси Y

# Отображение змейки на экране
    def drawing(self):
        pygame.draw.rect(display, self.color_main, [self.head_x, self.head_y, self.size, self.size])
        pygame.draw.rect(display, self.color_circuit, [self.head_x, self.head_y, self.size, self.size], 3)

# Изменение движения змейки вверх
    def go_up(self):
        self.speed_y = -self.size
        self.speed_x = 0

# Изменение движения змейки вниз
    def go_down(self):
        self.speed_y = self.size
        self.speed_x = 0

# Изменение движения змейки влево
    def go_left(self):
        self.speed_y = 0
        self.speed_x = -self.size

# Изменение движения змейки вправо
    def go_right(self):
        self.speed_y = 0
        self.speed_x = self.size

# Функция непосредственного движения змейки по полю игры
    def movement(self):
        self.head_x += self.speed_x
        self.head_y += self.speed_y

# Функция полной остановки змейки, вызывается после проигрыша
    def stop(self):
        self.speed_x = 0
        self.speed_y = 0

# Проверка жизнеспособности змейки (она передвигается в пределах видимости, не вышла за груницы поля
    def check_valid(self):
        if self.head_x < 0 or self.head_x > width - segment_size or self.head_y < 0 or self.head_y > height - \
                segment_size:
            self.stop()
            return False
        return True

    def get_position(self):
        return self.head_x, self.head_y


class InfoMessage(object):

    def __init__(self, text_message, text_color, type_text, size_text, pos_x, pos_y, size_x, size_y, color_form,
                 color_circuit, padding_left, padding_top):
        self.text_message = text_message    # Сам текст сообщения
        self.text_color = text_color        # Цвет текста сообщения
        self.type_text = type_text          # Тип шрифта сообщения
        self.size_text = size_text          # Размер шрифта сообщения
        self.pos_x = pos_x                  # Расположение сообщения по оси Х
        self.pos_y = pos_y                  # Расположение сообщения по оси Y
        self.size_x = size_x                # ⤵
        ''' Ширина бокса сообщения. Если сообщение выводится на фоне игры, 
                                                        то задать нулевое значение '''
        self.size_y = size_y                # Высота бокса сообщения
        self.color_form = color_form        # Цвет фона бокса. Если бокс отсутствует, задать любой цвет
        self.color_circuit = color_circuit  # Цвет рамки бокса
        self.padding_left = padding_left    # Отступ слева текста сообщения внутри бокса
        self.padding_top = padding_top      # Отступ справа текста сообщения внутри бокса

# Функция добавления бокса сообщения, текст сообщения будет напечатан в рамке
    def add_form(self, frame_thickness):
        pygame.draw.rect(display, self.color_form, [self.pos_x, self.pos_y, self.size_x, self.size_y])
        pygame.draw.rect(display, self.color_circuit, [self.pos_x, self.pos_y, self.size_x, self.size_y],
                         frame_thickness)

# Пишем текст сообщения на экране игры
    def write_text(self):
        font = pygame.font.SysFont(self.type_text, self.size_text)
        message = font.render(self.text_message, True, self.text_color)
        display.blit(message, [self.pos_x + self.padding_left, self.pos_y + self.padding_top])

# Функция-двигатель класса. В ней задаются параметры, печатается текст сообщения в рамке или на фоне поля игры
# Если бокс сообщения имеет значение False, то значение frame_thickness задать нулевое
    def set_message(self, bool_form, frame_thickness):
        if bool_form:
            self.add_form(frame_thickness)
        self.write_text()


class Fruit(object):

    def __init__(self, fruit_color, size):
        self.fruit_color = fruit_color
        self.pos_x = 0
        self.pos_y = 0
        self.size = size

    def generate_random_position(self):
        self.pos_x = random.randint(0, width - segment_size) // segment_size * segment_size
        self.pos_y = random.randint(0, height - segment_size) // segment_size * segment_size
        return self.pos_x, self.pos_y

    def draw_fruit(self, pos_x, pos_y):
        self.generate_random_position()
        pygame.draw.rect(display, self.fruit_color, [pos_x, pos_y, self.size, self.size])


snake = Snake(yellow, black, segment_size, head_x, head_y)

fruit = Fruit(steelblue, segment_size)
fruit_x, fruit_y = fruit.generate_random_position()

run = True
while run:
    if not snake.check_valid():
        lose_message = InfoMessage("GAME OVER!", red, "None", 35, width / 2 - 100, height / 2 - 40, 220, 80, white,
                                   black, 30, 30)
        lose_message.set_message(True, 5)

        pygame.display.flip()

        time.sleep(2)

        pygame.quit()
        quit()

    pygame.time.delay(speed_game)

    display.fill(pink)

    snake.movement()
    snake.drawing()

    fruit.draw_fruit(fruit_x, fruit_y)
    head_x, head_y = snake.get_position()
    if head_x == fruit_x and head_y == fruit_y:
        fruit_x, fruit_y = fruit.generate_random_position()
        count_segments_snake += 1
        list_segments_snake.append([head_x, head_y])

    print([head_x, head_y], list_segments_snake, len(list_segments_snake), count_segments_snake)

    if len(list_segments_snake) > 1:
        for i in reversed(range(1, len(list_segments_snake))):
            list_segments_snake[i] = list_segments_snake[i-1]
        print(head_x, head_y)
        for i in list_segments_snake:
            pygame.draw.rect(display, black, [i[0], i[1], segment_size - 1, segment_size - 1], 3)
            pygame.draw.rect(display, yellow, [i[0], i[1], segment_size + 1, segment_size + 1])
    list_segments_snake[0] = [head_x, head_y]

    for event in pygame.event.get():
#        print(event)
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.go_up()
            elif event.key == pygame.K_DOWN:
                snake.go_down()
            elif event.key == pygame.K_LEFT:
                snake.go_left()
            elif event.key == pygame.K_RIGHT:
                snake.go_right()

    pygame.display.flip()

pygame.quit()
