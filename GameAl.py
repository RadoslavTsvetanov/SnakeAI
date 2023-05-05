import pygame
import random
from enum import Enum
from collections import namedtuple
import pygame_gui
pygame.init()
#font = pygame.font.Font('arial.ttf', 25)
font = pygame.font.SysFont('arial', 25)
obstacles_list = []
crash_into_walls = False


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')


WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 20

SCROLL_WIDTH = 200  # width of the scroll bar
SCROLL_HEIGHT = 10  # height of the scroll bar
SCROLL_POS_X = 440  # x position of the scroll bar
SCROLL_POS_Y = 10  # y position of the scroll bar
SCROLL_MIN_VALUE = 1  # minimum value of the scroll bar
SCROLL_MAX_VALUE = 50  # maximum value of the scroll bar


class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()

        self.scroll_value = SPEED  # initial speed value

        # initialize the scroll bar
        self.scroll_bar = pygame.Rect(
            SCROLL_POS_X, SCROLL_POS_Y, SCROLL_WIDTH, SCROLL_HEIGHT)
        self.scroll_bar_pos = (self.scroll_value - SCROLL_MIN_VALUE) / (
            SCROLL_MAX_VALUE - SCROLL_MIN_VALUE) * (SCROLL_WIDTH - SCROLL_HEIGHT)
        self.scroll_bar_handle = pygame.Rect(
            SCROLL_POS_X + self.scroll_bar_pos, SCROLL_POS_Y, SCROLL_HEIGHT, SCROLL_HEIGHT)

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print(mouse_x, mouse_y)
                for i in range(0, self.w, 20):
                    if mouse_x < i:
                        mouse_x = i - 20
                        break
                for i in range(0, self.h, 20):
                    if mouse_y < i:
                        mouse_y = i - 20
                        break
                mouse_pos = (mouse_x, mouse_y)
                obstacles_list.append(mouse_pos)
                print("Mouse position:", mouse_pos)
        self._move(self.direction)  # update the head
        self.snake.insert(0, self.head)

        game_over = False
        if self._is_collision():
            # TODO:fix
            game_over = True
            return game_over, self.score

        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        self._update_ui()
        self.clock.tick(SPEED)

        return game_over, self.score

    def _is_collision(self):
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            if(crash_into_walls):
                return True
            self.head = Point(0, 0)
            return False
        for block in obstacles_list:
            block_object = Point(block[0], block[1])
            print(self.head == block_object)
            if(self.head == block_object):
                return True
        if self.head in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(
                pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2,
                             pygame.Rect(pt.x+4, pt.y+4, 12, 12))
        for obstacle in obstacles_list:
            pygame.draw.rect(self.display, WHITE, pygame.Rect(
                obstacle[0], obstacle[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, RED, pygame.Rect(
            self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)


if __name__ == '__main__':
    game = SnakeGame()

    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()
