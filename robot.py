import pygame
import math

GRID_SIZE = 50


class Robot:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
        self.angle = 0
        self.path = []
        self.movement_generator = None

    def move_forward(self, distance):
        if self.x is None or self.y is None:
            print("Please select a starting point for the robot.")
            return
        self.x += distance * math.cos(self.angle)
        self.y += distance * math.sin(self.angle)
        self.record_path()

    def rotate(self, angle):
        self.angle += angle
        self.angle %= 2 * math.pi

    def record_path(self):
        if self.x is not None and self.y is not None:
            self.path.append((self.x, self.y))

    def set_movement(self, movement_generator):
        if movement_generator:
            self.movement_generator = iter(movement_generator)

    def update(self):
        if self.movement_generator:
            try:
                next(self.movement_generator)
            except StopIteration:
                self.movement_generator = None

    def move_to(self, x, y):
        self.x = x
        self.y = y
        self.record_path()

    def draw(self, screen):
        if self.x is not None and self.y is not None:
            if len(self.path) > 1:
                pygame.draw.lines(screen, (0, 0, 255), False, self.path, 2)
            pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 10)
