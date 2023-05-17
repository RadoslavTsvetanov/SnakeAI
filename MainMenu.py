import pygame
from Buttons import Crash_button
import sys
pygame.init()

RED = (127, 127, 127)


class MainMenu():
    def __init__(self, screen, width, height, start_x, start_y, end_x, end_y):
        self.screen = screen
        self.width = width
        self.height = height
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.start_button = Crash_button(
            self.start_x, self.start_y, self.width, self.height, self.screen, "start simulation", True)
        self.exit_button = Crash_button(
            self.end_x, self.end_y, self.width, self.height, self.screen, "hi", False, "./images/exit_btn.png")
        self.is_showed = self.start_button.state

    def draw(self):
        if(self.is_showed):
            self.screen.fill((255, 255, 255))
            self.start_button.draw()
            self.exit_button.draw()

    def check_for_click(self, mouse_click):
        self.start_button.check_for_click(mouse_click)
        self.is_showed = self.start_button.state
        self.exit_button.check_for_click(mouse_click)
        if self.exit_button.state:
            pygame.quit()
            sys.exit()
            quit()
