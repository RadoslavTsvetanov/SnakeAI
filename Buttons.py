import pygame

WHITE = (255, 255, 255)


class Button():
    def __init__(self, x, y, w, h, screen, text):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.screen = screen
        self.text = text

    def check_for_click(self, mouse_click):

        if(mouse_click['x'] >= self.x and mouse_click['x'] <= self.x + self.w and mouse_click['y'] >= self.y and mouse_click['y'] <= self.y + self.h):
            return self.action(mouse_click)  # slider

    def draw(self):
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(
            self.x, self.y, self.w, self.h))
        # self.screen.blit(
        #    self.text, [self.x + (self.w)//2, self.y + (self.h)//2])

    def action(self, mouse_click):
        pass


class Crash_button(Button):
    def __init__(self, x, y, w, h, screen, text, state):
        super().__init__(x, y, w, h, screen, text)
        self.state = state

    def action(self, mouse_click):
        self.state = not self.state
        print(self.state)
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
                           (self.x + (self.w//2), self.value), 20)
