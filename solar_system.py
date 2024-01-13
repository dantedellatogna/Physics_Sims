import pygame
import math
import sys


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

width = 1900
height = 900

G = 6.674e-11
solar_mass = 1.988e30
TIMESTEP = 24 * 3600  # 1 day
AU = 149.6e6 * 1000
SCALE = 200 / AU  # 1AU = 100px


bodies = list()


class Bodies:
    def __init__(self, color, pos, mass, radius, speed, orbit_trail):
        self.color = color
        self.pos = pos
        self.mass = mass
        self.radius = radius

        self.speed = speed

        self.orbit_trail = orbit_trail

        bodies.append(self)

    def draw_body(self):
        x = self.pos[0] * SCALE + width / 2
        y = self.pos[1] * SCALE + height / 2
        print("x, y: ", [x, y])
        pygame.draw.circle(
            surface=screen, color=self.color, center=[x, y], radius=self.radius
        )

    def draw_orbit(self):
        for body in bodies[1:]:
            x = body.pos[0] * SCALE + width / 2
            y = body.pos[1] * SCALE + height / 2
            body.orbit_trail.append([x, y])
            prev_orbit = body.orbit_trail[0]

            for orbit in body.orbit_trail:
                pygame.draw.line(
                    surface=screen,
                    color=body.color,
                    start_pos=prev_orbit,
                    end_pos=orbit,
                )
                prev_orbit = orbit

    def attraction(self, other):
        if self != bodies[0]:
            x_distance = other.pos[0] - self.pos[0]
            y_distance = other.pos[1] - self.pos[1]

            r = math.sqrt(x_distance**2 + y_distance**2)

            F = G * self.mass * other.mass / r**2

            angle = math.atan2(y_distance, x_distance)

            Fx = F * math.cos(angle)
            Fy = F * math.sin(angle)

            # print("Fx", Fx)
            # print("Fy", Fy)

            past_speed = self.speed

            time = TIMESTEP
            # time = pygame.time.get_ticks()
            self.speed[0] = (Fx * time) / self.mass + past_speed[0]

            self.speed[1] = (Fy * time) / self.mass + past_speed[1]

    def update_pos(self):
        time = TIMESTEP
        # time = pygame.time.get_ticks()
        self.pos[0] = self.pos[0] + time * self.speed[0]
        self.pos[1] = self.pos[1] + time * self.speed[1]


def main_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        for body in bodies:
            body.attraction(bodies[0])
            body.update_pos()
            body.draw_orbit()
            body.draw_body()
            print("Color: ", body.color)
            print("Position: ", body.pos)
            print("Speed: ", body.speed)

        pygame.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    sun = Bodies(
        color=YELLOW,
        pos=[0, 0],
        mass=1.988e30,
        radius=50,
        speed=[0, 0],
        orbit_trail=[],
    )

    earth = Bodies(
        color=BLUE,
        # pos=[0, 400],
        pos=[1 * AU, 0],
        mass=5.972e24,
        radius=12,
        # speed=[0, -40000],
        speed=[0, -29.783 * 1000],
        orbit_trail=[],
    )

    mars = Bodies(
        color=RED,
        pos=[1.524 * AU, 0],
        mass=6.39e23,
        radius=10,
        speed=[0, -24.077 * 1000],
        orbit_trail=[],
    )

    mercury = Bodies(
        color=GREEN,
        pos=[0.387 * AU, 0],
        mass=3.30e23,
        radius=8,
        speed=[0, -47.4 * 1000],
        orbit_trail=[],
    )

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    main_loop()
