import pygame
WHITE = (255, 255, 255)


class Button():
    def __init__(self, w, h, screen, x, y, text):
        self.screen = screen
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.state = False
        self.text = text

    def draw_button(self):
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(
            self.x, self.y, self.w, self.h))

    def return_state(self):
        return self.state

    def check_for_mouse_click(self, point, arr):
        if point['x'] > self.x and point['x'] < self.x + self.w and point['y'] > self.y and point['y'] < self.y + self.h:
            return []
        return arr
