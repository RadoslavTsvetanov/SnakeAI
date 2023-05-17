import pygame
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
font = pygame.font.SysFont('arial', 25)


class Button():  # button za barrieri
    def __init__(self, w, h, screen, x, y, text, state):
        self.screen = screen
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.state = state
        self.text = font.render(text, True, BLACK)

    def draw_button(self):

        self.screen.blit(
            self.text, [self.x + self.w//2 - 20, self.y + self.h//2 - 10])
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(
            self.x, self.y, self.w, self.h))
        self.screen.blit(self.text, [self.x, self.y])

    def return_state(self):
        return self.state

    def check_for_mouse_click(self, point, arr):
        if point['x'] > self.x and point['x'] < self.x + self.w and point['y'] > self.y and point['y'] < self.y + self.h:
            return []
        return arr
# drugite botoni shte izplolzvat nasledqvane ot Bazov klass
