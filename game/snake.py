import pygame
import time

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

segment_size = 30
head_x = width // 2
head_y = height // 2

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


snake = Snake(yellow, black, segment_size, head_x, head_y)

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

    for event in pygame.event.get():
        print(event)
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
