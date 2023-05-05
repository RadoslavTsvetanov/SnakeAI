import pygame
import random
from enum import Enum
from collections import namedtuple
import pygame_gui
from Button import Button
pygame.init()
#font = pygame.font.Font('arial.ttf', 25)
font = pygame.font.SysFont('arial', 25)
crash_into_walls = False


def load_from_file(filename):
    with open(filename, 'r') as f:
        for i in f.read():
            print(i)


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

    def __init__(self, w=840, h=600, load_previous=not True):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.load = True
        self.direction = Direction.RIGHT
        self.obstacles_list = self.load_from_file(
            "arr.txt") if load_previous else []
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self.Barriers_button = Button(170, 70, self.display, self.w-190, 50)
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w - 200 - BLOCK_SIZE) //
                           BLOCK_SIZE)*BLOCK_SIZE
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
                if(mouse_x < self.w - 200):
                    for i in range(0, self.w, 20):
                        if mouse_x < i:
                            mouse_x = i - 20
                            break
                    for i in range(0, self.h, 20):
                        if mouse_y < i:
                            mouse_y = i - 20
                            break
                    mouse_pos = (mouse_x, mouse_y)
                    self.obstacles_list.append(mouse_pos)
        self._move(self.direction)  # update the head
        self.snake.insert(0, self.head)

        game_over = False
        if self._is_collision():
            # TODO:fix
            self.save_to_file("arr.txt", self.obstacles_list)
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
        if self.head.x > self.w - BLOCK_SIZE - 200 or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE - 200 or self.head.y < 0:
            if(crash_into_walls):
                return True
            self.head = Point(0, 0)
            return False
        for block in self.obstacles_list:
            block_object = Point(block[0], block[1])
            if(self.head == block_object):
                return True
        if self.head in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)
        # button for obstacles
        self.Barriers_button.draw_button()
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(
                pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2,
                             pygame.Rect(pt.x+4, pt.y+4, 12, 12))
        print("self.obstacles_list")
        print(self.obstacles_list)
        if(len(self.obstacles_list) > 0):
            print("list not empty")
            for obstacle in self.obstacles_list:
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

    def save_to_file(self, filename, arr):
        print("saving to file")
        with open(filename, 'w') as f:
            for i in arr:
                f.write(str(i) + '\n')

    def load_from_file(self, filename):
        coordinates_list = []
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                print(line)
                if(line[0] != '\n'):
                    x = 0
                    y = 0
                    for j in range(1, 4, 1):
                        if(line[j] >= '0' and line[j] <= '9'):
                            x = x * 10 + int(line[j])
                            continue
                        break
                    for j in range(6, 9, 1):
                        if(line[j] >= '0' and line[j] <= '9'):
                            y = y * 10 + int(line[j])
                            continue
                        break
                    coordinates_list.append((x, y))
        print(coordinates_list)
        return coordinates_list


if __name__ == '__main__':
    game = SnakeGame()

    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()
