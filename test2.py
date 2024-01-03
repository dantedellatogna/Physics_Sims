import pygame
import sys

colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
}


class Body:
    def __init__(self, color, mass, pos, speed, gravity):
        self.color = color
        self.mass = mass
        self.pos = pos
        self.speed = speed
        self.gravity = gravity


class Ball(Body):
    def __init__(self, color, mass, pos, speed, gravity, radius):
        super().__init__(color, mass, pos, speed, gravity)
        self.radius = radius


width = 800
height = 800

g = 0.00000981

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

spawn = [100, 700]
ball = Ball(color=colors["red"], mass=1, pos=spawn, speed=0, gravity=True, radius=40)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(1000)
