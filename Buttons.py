import pygame
import os
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
font = pygame.font.SysFont('arial', 25)


class Button():  # base class
    def __init__(self, x, y, w, h, screen, text, image_path="./images/start_btn.png"):
        self.image_path = image_path
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.screen = screen
        self.text = font.render(text, True, BLACK)

    def check_for_click(self, mouse_click):
        self.screen.blit(self.text, [self.x, self.y])
        if(mouse_click['x'] >= self.x and mouse_click['x'] <= self.x + self.width and mouse_click['y'] >= self.y and mouse_click['y'] <= self.y + self.height):
            return self.action(mouse_click)  # slider

    def draw(self):

        pygame.draw.rect(self.screen, WHITE, pygame.Rect(
            self.x, self.y, self.width, self.height))
        self.screen.blit(
            self.text, [self.x + self.width//2 - 20, self.y + self.height//2 - 10])
        # self.screen.blit(
        #    self.text, [self.x + (self.width)//2, self.y + (self.height)//2])
        self.screen.blit(pygame.transform.scale(pygame.image.load(
            self.image_path), (self.width, self.height)), [self.x, self.y])

    def action(self, mouse_click):
        pass


class Crash_button(Button):  # for all kinds of buttons which just hold a state
    def __init__(self, x, y, w, h, screen, text, state, image_path="./images/start_btn.png"):
        super().__init__(x, y, w, h, screen, text, image_path)
        self.state = state

    def action(self, mouse_click):
        self.state = not self.state
        return self.state


class Slider(Button):
    def __init__(self, x, y, w, h, screen, text, value):
        super().__init__(x, y, w, h, screen, text)
        self.min = min
        self.max = max
        self.value = value

    def action(self, mouse_click):
        print(mouse_click['y'] - self.y)
        self.value = mouse_click['y']
        return mouse_click['y'] - self.y

    def draw_circle(self):
        pygame.draw.circle(self.screen, (0, 0, 0),
                           (self.x + (self.width//2), self.value), 20)
