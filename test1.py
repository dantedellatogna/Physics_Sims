import pygame
import sys
import random

colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
}


class Ball:
    def __init__(self, color, radius, mass, pos):
        self.color = color
        self.radius = radius
        self.mass = mass
        self.pos = pos


width = 800
height = 800

g = 0.00000981
speed = [0, 0]
past_speed = [0, 0]

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


ball = Ball(colors["red"], radius=40, mass=1, pos=[400, 100])

ball_obj = pygame.draw.circle(
    surface=screen, color=ball.color, center=ball.pos, radius=ball.radius
)

while True:  # Main loop
    # nx = random.randint(200, 700)
    # ny = random.randint(200, 700)
    # past_speed = [0, 0]

    # ball.pos = [400, 100]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # physics loop
    while width - ball.pos[1] > 40:
        speed[1] = g * pygame.time.get_ticks() + past_speed[1]
        past_speed[1] = speed[1]

        ball.pos[1] = pygame.time.get_ticks() * speed[1]

        # draw circle each frame
        screen.fill((0, 0, 0))
        pygame.draw.circle(
            surface=screen, color=ball.color, center=ball.pos, radius=ball.radius
        )

        # print(pygame.time.get_ticks())
        print(ball.pos)
        pygame.display.update()
        clock.tick(1000)
    ball.pos[1] = 760
