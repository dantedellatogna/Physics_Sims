import pygame
import sys

colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
}

bodies = list()


class Body:
    def __init__(self, color, mass, pos, speed, past_speed, gravity):
        self.color = color
        self.mass = mass
        self.pos = pos
        self.speed = speed
        self.past_speed = past_speed
        self.gravity = gravity

        bodies.append(self)


class Ball(Body):
    def __init__(self, color, mass, pos, speed, past_speed, gravity, radius):
        super().__init__(color, mass, pos, speed, past_speed, gravity)
        self.radius = radius


def main_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # gravity
        time = pygame.time.get_ticks()
        for body in bodies:
            if body.gravity == True:
                body.speed[1] = g * time + body.past_speed[1]
                body.past_speed[1] = body.speed[1]

                # pygame.time.delay()

                print(body.speed[1])
                print(body.pos)

                body.pos[1] = body.pos[1] + time * body.speed[1]

        screen.fill("black")

        for body in bodies:
            pygame.draw.circle(
                surface=screen,
                color=body.color,
                center=body.pos,
                radius=body.radius,
            )

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    width = 800
    height = 800

    g = 0.00000981

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    spawn = [100, 100]
    ball1 = Ball(
        color=colors["white"],
        mass=1,
        pos=spawn,
        speed=[0, 0],
        past_speed=[0, 0],
        gravity=True,
        radius=40,
    )

    ball2 = Ball(
        color=colors["red"],
        mass=2,
        pos=[600, 300],
        speed=[0, 0],
        past_speed=[0, 0],
        gravity=True,
        radius=80,
    )

    main_loop()
