import pygame
import math
import sys

colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
}

TIMESTEP = 24 * 3600


bodies = list()


class Bodies:
    def __init__(self, color, pos, mass, radius, speed, orbit_trail):
        self.color = color
        self.pos = pos
        self.mass = mass * solar_mass
        self.radius = radius

        self.speed = speed

        self.orbit_trail = orbit_trail

        bodies.append(self)

    def draw_body(self):
        x = self.pos[0] + width / 2
        y = self.pos[1] + height / 2
        pygame.draw.circle(
            surface=screen, color=self.color, center=[x, y], radius=self.radius
        )

    def draw_orbit(self):
        for body in bodies[1:]:
            x = body.pos[0] + width / 2
            y = body.pos[1] + height / 2
            body.orbit_trail.append([x, y])
            prev_orbit = body.orbit_trail[0]

            for orbit in body.orbit_trail:
                pygame.draw.line(
                    surface=screen,
                    color="white",
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

            print("Fx", Fx)
            print("Fy", Fy)

            past_speed = self.speed

            time = pygame.time.get_ticks()
            self.speed[0] = (Fx * time * time) / self.mass + past_speed[0]

            self.speed[1] = (Fy * time * time) / self.mass + past_speed[1]

    def update_pos(self):
        time = pygame.time.get_ticks()
        self.pos[0] = self.pos[0] + time * self.speed[0] / 1e26
        self.pos[1] = self.pos[1] + time * self.speed[1] / 1e26


def main_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(colors["black"])

        for body in bodies:
            body.attraction(bodies[0])
            body.update_pos()
            body.draw_orbit()
            body.draw_body()
            print(body.color)
            print(body.pos)
            print(body.speed)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    width = 800
    height = 800

    G = 6.674e-11
    solar_mass = 1.988e30

    sun = Bodies(
        color=colors["yellow"],
        pos=[0, 0],
        mass=1,
        radius=50,
        speed=[0, 0],
        orbit_trail=[],
    )

    earth = Bodies(
        color=colors["white"],
        pos=[0, 400],
        mass=3.0e-6,
        radius=10,
        speed=[2.2e23, -0.1e21],
        orbit_trail=[],
    )

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    main_loop()
