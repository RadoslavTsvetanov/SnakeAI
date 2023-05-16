import pygame
from Buttons import Crash_button
pygame.init()

RED = (127, 127, 127)


class MainMenu():
    def __init__(self, screen, width, height, x, y):
        self.screen = screen
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.start_button = Crash_button(
            self.x, self.y, self.width, self.height, self.screen, "start simulation", True)
        self.is_showed = self.start_button.state

    def draw(self):
        if(self.is_showed):
            self.screen.fill((255, 255, 255))
            pygame.draw.rect(self.screen, RED, pygame.Rect(
                self.width//2 + 20, self.height // 2 + 10, 400, 200))

    def check_for_click(self, mouse_click):
        self.start_button.check_for_click(mouse_click)
        self.is_showed = self.start_button.state
