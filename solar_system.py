import pygame
import math
import sys
import random

# ---COLOR PALETTE (RGB)---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# --- WINDOW SIZE ---
WIDTH = 1900
HEIGHT = 900

# --- PHYSICS SIMULATION CONSTANTS ---
G = 6.674e-11  # Gravitational constant
TIME = 24 * 3600  # 1 day in seconds
AU = 149.6e6 * 1000  # Astronomical Unit (meters)
SCALE = 200 / AU  # 1AU = 100px


# --- STARS BACKGROUND ---

stars_bg = list()


def stary_sky(width, height):
    for i in range(0, 900):
        for j in range(0, 500):
            n = random.randint(0, 1900)
            pygame.draw.circle(surface=screen, color=WHITE, center=(n, i), radius=1)
            stars_bg.append(n, i)


# --- ASTRONOMICAL BODIES SIMULATED ---
bodies = list()


class Bodies:
    def __init__(self, color, position, mass, radius, speed, orbit_trail):
        self.color = color  # tuple RGB
        self.position = position  # list [x, y]
        self.mass = mass  # kg
        self.radius = radius  # px
        self.speed = speed  # m/s
        self.orbit_trail = orbit_trail  # list of positions [[x1, y1], [x2, y2],...]

        bodies.append(self)

    def get_xy(self):
        x = self.position[0] * SCALE + WIDTH / 2
        y = self.position[1] * SCALE + HEIGHT / 2
        return (x, y)

    def draw_orbit(self):
        x, y = self.get_xy()
        # Drawing orbit lines
        self.orbit_trail.append((x, y))
        prev_orbit = self.orbit_trail[0]

        for orbit in self.orbit_trail:
            pygame.draw.line(
                surface=screen,
                color=WHITE,
                start_pos=prev_orbit,
                end_pos=orbit,
                width=1,
            )
            prev_orbit = orbit

    def draw_body(self):
        x, y = self.get_xy()
        # Drawing bodies
        pygame.draw.circle(
            surface=screen, color=self.color, center=[x, y], radius=self.radius
        )

    def attraction(self, bodies):
        for other in bodies:
            if self != other:
                x_distance = other.position[0] - self.position[0]
                y_distance = other.position[1] - self.position[1]

                r = math.sqrt(x_distance**2 + y_distance**2)
                F = G * self.mass * other.mass / r**2

                angle = math.atan2(y_distance, x_distance)
                Fx = F * math.cos(angle)
                Fy = F * math.sin(angle)

                past_speed = self.speed
                self.speed[0] = (Fx * TIME) / self.mass + past_speed[0]
                self.speed[1] = (Fy * TIME) / self.mass + past_speed[1]

    def update_position(self):
        self.attraction(bodies)
        self.position[0] = self.position[0] + TIME * self.speed[0]
        self.position[1] = self.position[1] + TIME * self.speed[1]


def main_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        for body in bodies:
            body.update_position()
            body.draw_orbit()
            body.draw_body()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    # Initializing bodies
    sun = Bodies(
        color=YELLOW,
        position=[0, 0],
        mass=1.988e30,
        radius=50,
        speed=[0, 0],
        orbit_trail=[],
    )

    earth = Bodies(
        color=BLUE,
        position=[1 * AU, 0],
        mass=5.972e24,
        radius=12,
        # speed=[0, -40000],
        speed=[0, -29.783 * 1000],
        orbit_trail=[],
    )

    mars = Bodies(
        color=RED,
        position=[1.524 * AU, 0],
        mass=6.39e23,
        radius=10,
        speed=[0, -24.077 * 1000],
        orbit_trail=[],
    )

    mercury = Bodies(
        color=GREEN,
        position=[0.387 * AU, 0],
        mass=3.30e23,
        radius=8,
        speed=[0, -47.4 * 1000],
        orbit_trail=[],
    )

    """sun2 = Bodies(
        color=WHITE,
        position=[6 * AU, 3 * AU],
        mass=1.988e30,
        radius=50,
        speed=[-47.4 * 1000, -47.4 * 1000],
        orbit_trail=[],
    )"""

    # Pygame initializations
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    main_loop()
