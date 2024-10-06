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

MERCURY = (122, 111, 43)
VENUS = (156, 96, 36)
EARTH = (43, 44, 122)
MARS = (156, 60, 36)
JUPITER = (217, 140, 95)
SATURN = (227, 191, 125)
URANUS = (112, 212, 210)
NEPTUNE = (182, 227, 226)

# --- WINDOW SIZE ---
WIDTH = 800
HEIGHT = 600

# --- PHYSICS SIMULATION CONSTANTS ---
G = 6.674e-11  # Gravitational constant
TIME = 24 * 3600  # 1 day in seconds
AU = 149.6e6 * 1000  # Astronomical Unit (meters)
SCALE = 100 / AU  # 1AU = 100px


# --- STARS BACKGROUND ---

stars_bg = list()

# --- CAMERA OFFSET ---
cameraOffset = [0, 0]
origin = (WIDTH / 2, HEIGHT / 2)
center = [origin[0], origin[1]]


def stary_sky(width, height):
    if len(stars_bg) == 0:
        for i in range(0, 900, 1):
            for j in range(0, 1):
                n = random.randint(0, 1900)
                stars_bg.append((n, i))

    for star_pos in stars_bg:
        pygame.draw.circle(surface=screen, color=WHITE, center=star_pos, radius=1)


# --- ASTRONOMICAL BODIES SIMULATED ---
bodies = list()


def lineLength(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    # length = sqrt((x2 - x1)^2 + (y2 - y1)^2)
    x_sqrd = (x2 - x1) * (x2 - x1)
    y_sqrd = (y2 - y1) * (y2 - y1)
    length = math.sqrt(x_sqrd + y_sqrd)
    return length


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
                color=self.color,
                start_pos=prev_orbit,
                end_pos=orbit,
                width=1,
            )
            prev_orbit = orbit

        if len(self.orbit_trail) > 10000:
            self.orbit_trail.pop(0)

    def draw_body(self):
        x, y = self.get_xy()

        scale_radius = self.radius * SCALE * 10e8
        # Drawing bodies
        pygame.draw.circle(
            surface=screen, color=self.color, center=[x, y], radius=scale_radius
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
        global cameraOffset
        self.attraction(bodies)
        self.position[0] = (self.position[0] + TIME * self.speed[0]) + cameraOffset[0]
        self.position[1] = self.position[1] + TIME * self.speed[1]

        # print(cameraOffset[0])  # ---------------------

    def write_speed_txt(self):
        x, y = self.get_xy()
        font = pygame.font.SysFont("consolas", 14)
        speed = math.sqrt(self.speed[0] ** 2 + self.speed[1] ** 2)
        speed = speed / 1000
        speed_txt = font.render(f"{round(speed, 2)} km/s", 1, WHITE)
        screen.blit(
            speed_txt,
            (
                x - speed_txt.get_width() / 2,
                (y - speed_txt.get_height() / 2) - self.radius - 10,
            ),
        )


def main_loop():
    global SCALE
    global cameraOffset

    origin = (0, 0)

    while True:
        for event in pygame.event.get():
            mousexy = pygame.mouse.get_pos()
            mousebttn = pygame.mouse.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ZOOM
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    SCALE += 10 / AU
                elif event.y < 0:
                    SCALE -= 10 / AU

                if SCALE < 0:
                    SCALE = 0

            # CAMERA
            if mousebttn[0] == True:
                cameraOffset[0] += 10e5 * (mousexy[0] - 400)
                # print(cameraOffset[0])
                print(mousexy[0])
            if mousebttn[0] == False:
                cameraOffset[0] = 0
                # print(cameraOffset[0])
                print(mousexy[0])

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    cameraOffset[0] = 0
                    # print(cameraOffset[0])

            # --- Stop planet - Method call (Testing) ---
            # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Call the on_mouse_button_down() function

        # Background
        screen.fill(BLACK)
        stary_sky(WIDTH, HEIGHT)  # stars (random)

        for body in bodies:
            body.update_position()
            # body.draw_orbit()
            body.draw_body()
            body.write_speed_txt()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    # Initializing bodies
    sun = Bodies(
        color=YELLOW,
        position=[0, 0],
        mass=1.988e30,
        radius=30,
        speed=[0, 0],
        orbit_trail=[],
    )

    mercury = Bodies(
        color=MERCURY,
        position=[0.387 * AU, 0],
        mass=3.30e23,
        radius=5,
        speed=[0, -47.4 * 1000],
        orbit_trail=[],
    )

    venus = Bodies(
        color=VENUS,
        position=[0.72 * AU, 0],
        mass=4.867e24,
        radius=10,
        speed=[0, -35.02 * 1000],
        orbit_trail=[],
    )

    earth = Bodies(
        color=EARTH,
        position=[1 * AU, 0],
        mass=5.972e24,
        radius=12,
        # speed=[0, -40000],
        speed=[0, -29.783 * 1000],
        orbit_trail=[],
    )

    mars = Bodies(
        color=MARS,
        position=[1.524 * AU, 0],
        mass=6.39e23,
        radius=7,
        speed=[0, -24.077 * 1000],
        orbit_trail=[],
    )

    jupiter = Bodies(
        color=JUPITER,
        position=[5.2 * AU, 0],
        mass=1.89813e27,
        radius=20,
        speed=[0, -13.06 * 1000],
        orbit_trail=[],
    )

    saturn = Bodies(
        color=SATURN,
        position=[9.538 * AU, 0],
        mass=5.6832e26,
        radius=18,
        speed=[0, -9.67 * 1000],
        orbit_trail=[],
    )

    uranus = Bodies(
        color=URANUS,
        position=[19.165 * AU, 0],
        mass=86.811e24,
        radius=17,
        speed=[0, -7.13 * 1000],
        orbit_trail=[],
    )

    neptune = Bodies(
        color=NEPTUNE,
        position=[30.1806 * AU, 0],
        mass=102.409e24,
        radius=16,
        speed=[0, -5.45 * 1000],
        orbit_trail=[],
    )

    # TEST BODIES
    """sun2 = Bodies(
        color=WHITE,
        position=[6 * AU, 3 * AU],
        mass=1.988e30,
        radius=50,
        speed=[-47.4 * 1000, -47.4 * 1000],
        orbit_trail=[],
    )"""

    """
    moon = Bodies(
        color=WHITE,
        position=[0.2569555e-3 * AU + earth.position[0], 0],
        mass=0.07346e24,
        # mass=0.000001,
        radius=3,
        speed=[0, earth.speed[1]],
        orbit_trail=[],
    )
    """

    # Pygame initializations
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    main_loop()
