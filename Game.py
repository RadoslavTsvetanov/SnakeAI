import pygame
import random
from enum import Enum
from collections import namedtuple
import pygame_gui
import pygame_widgets
from Button import Button
import numpy as np
from Buttons import Crash_button, Slider
pygame.init()
# font = pygame.font.Font('arial.ttf', 25)
font = pygame.font.SysFont('arial', 25)
SPEED = 40


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
SPEED = 40


class SnakeGameAI:

    def __init__(self, w=840, h=600, load_previous=not True):
        self.show_main_menu = True
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset(load_previous)
        self.crash_into_walls = True
        self.speed = 40
        self.slider = Slider(self.w - 100, 300, 70, 200,
                             self.display, "speed", 300 + 40)  # 40 -> self.speed idk it does not work with self.speed
        self.Crash_button = Crash_button(
            x=self.w - 190, y=170, w=180, h=100, screen=self.display, text="crash into walls", state=True)
        self.Barriers_button = Button(
            170, 70, self.display, self.w-190, 50, "clear barriers")

    def reset(self, load_previous):

        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.obstacles_list = self.load_from_file(
            "arr.txt") if load_previous else []
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def save_to_file(self, filename, arr):
        with open(filename, 'w') as f:
            for i in arr:
                f.write(str(i) + '\n')

    def load_from_file(self, filename):
        coordinates_list = []
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
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
        return coordinates_list

    def _place_food(self):
        while True:
            x = random.randint(0, (self.w-BLOCK_SIZE - 200) //
                               BLOCK_SIZE)*BLOCK_SIZE
            y = random.randint(0, (self.h-BLOCK_SIZE - 200) //
                               BLOCK_SIZE)*BLOCK_SIZE
            if not([x, y] in self.obstacles_list):
                self.food = Point(x, y)
                break
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.obstacles_list = self.Barriers_button.check_for_mouse_click(point={
                    'x': mouse_x, 'y': mouse_y
                }, arr=self.obstacles_list)
                self.crash_into_walls = self.Crash_button.check_for_click(
                    mouse_click={'x': mouse_x, 'y': mouse_y})
                self.speed = self.slider.check_for_click(
                    mouse_click={'x': mouse_x, 'y': mouse_y})
                if(mouse_x < self.w - 200):
                    for i in range(0, self.w, 20):
                        if mouse_x < i:
                            mouse_x = i - 20
                            break
                    for i in range(0, self.h, 20):
                        if mouse_y < i:
                            mouse_y = i - 20
                            break
                    should_add = True
                    for i in range(len(self.obstacles_list)):
                        if self.obstacles_list[i][0] == mouse_x and self.obstacles_list[i][1] == mouse_y:
                            self.obstacles_list.pop(i)
                            should_add = False
                            break
                    if(should_add):
                        mouse_pos = (mouse_x, mouse_y)
                        self.obstacles_list.append(mouse_pos)
        self._move(action)
        self.snake.insert(0, self.head)

        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        self._update_ui()
        self.clock.tick(self.speed or 40)

        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        if pt.x > self.w - BLOCK_SIZE - 200 or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            if(self.crash_into_walls):
                return True
            self.head = Point(300, 300)
            return False
        for block in self.obstacles_list:
            block_object = Point(block[0], block[1])
            if(self.head == block_object):
                return True
        if pt in self.snake[1:]:
            return True

        return False

    def _update_ui(self):

        self.display.fill(BLACK)
        self.slider.draw()
        self.slider.draw_circle()
        self.Barriers_button.draw_button()
        self.Crash_button.draw()
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(
                pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2,
                             pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(
            self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        if(len(self.obstacles_list) > 0):
            for obstacle in self.obstacles_list:
                pygame.draw.rect(self.display, WHITE, pygame.Rect(
                    obstacle[0], obstacle[1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, RED, pygame.Rect(
                self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        if(len(self.obstacles_list) > 0):
            self.save_to_file("arr.txt", self.obstacles_list)
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN,
                      Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)
