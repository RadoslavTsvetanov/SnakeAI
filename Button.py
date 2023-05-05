import pygame


class Button():
    def __init__(self, w, h, screen, x, y):
        self.screen = screen
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.state = False

    def draw_button(self):
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(
            self.x, self.y, self.w, self.h))

    def check_for_click(self, mouse_click):
        if mouse_click.x > self.x and mouse_click.x < self.x + self.w and mouse_click.y > self.y and mouse_click.y < self.y + self.h:
            self.state = not(self.state)

    def return_state(self):
        return self.state
