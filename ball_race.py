import pygame
import sys
import random
import math
import numpy as np

pygame.init()

# Window settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ball race")

# Colors
white = (255, 255, 255)
grey = (128, 128, 128)
black = (0, 0, 0)
colors = [
    (255, 0, 0),  # red
    (0, 255, 0),  # green
    (0, 0, 255),  # blue
    (0, 255, 255),  # cyan
    (255, 255, 0),  # yellow
    (255, 0, 255),  # magenta
    (128, 0, 128),  # violet
    (255, 128, 0),  # orange
    (0, 0, 128),  # navy
    (128, 128, 255)  # purple
]

# Initial parameters
radius = 5
speed = 3


# Class representing ball
class Ball(pygame.sprite.Sprite):
    def __init__(self, position,direction, radius, color, obstacles_group, winning_area):
        super().__init__()
        self.pos = pygame.math.Vector2(position)
        self.dir = pygame.math.Vector2(direction)
        self.radius = radius
        self.color = color
        self.obstacles_group = obstacles_group
        self.name = self.get_color_name(color)
        self.speed = 3
        self.is_winner = False
        self.winning_area = winning_area
        self.rect = pygame.Rect(round(self.pos.x - radius), round(self.pos.y - radius), radius*2, radius*2)
        self.image = pygame.Surface((radius*2, radius*2))
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)

    def collision_with_obstacles(self):
        collision_list = pygame.sprite.spritecollide(self, self.obstacles_group, False, collided = pygame.sprite.collide_circle)
        for obstacle in collision_list:
                #print("KOLIZJA")
                dx = obstacle.rect.x - self.pos.x + self.radius // 2
                dy = obstacle.rect.y - self.pos.y + self.radius // 2
                angle = math.atan2(dy, dx)
                self.dir.x = -math.cos(angle)
                self.dir.y = -math.sin(angle)
                collision_list.remove(obstacle)

    def get_color_name(self, color):
        color_names = {
            (255, 0, 0): "Czerwonka",
            (0, 255, 0): "Zielonka",
            (0, 0, 255): "Niebieska",
            (0, 255, 255): "Cyjanka",
            (255, 255, 0): "Żółtko",
            (255, 0, 255): "Magentka",
            (128, 0, 128): "Fioletka",
            (255, 128, 0): "Pomarańczka",
            (0, 0, 128): "Granatka",
            (128, 128, 255): "Purpurka"
        }
        return color_names.get(color, "Nieznany")


    def check_winning_condition(self):
        collision_list = pygame.sprite.spritecollide(self, self.winning_area, False)
        #print(collision_list)
        if collision_list:
            #print(f"Kulka {self.name} wygrywa!")
            self.is_winner = True


    def update_position(self):
        self.pos.x += self.speed * self.dir.x
        self.pos.y += self.speed * self.dir.y
        #print(self.direction[0])
        #print(self.direction[1])
        if  (self.pos.x - self.radius < 0 and self.dir.x < 0) or \
            (self.pos.x + self.radius > width and self.dir.x > 0):
                self.dir.x *= -1 *1.1

        if  (self.pos.y - self.radius < 0 and self.dir.y < 0) or \
            (self.pos.y + self.radius > height and self.dir.y > 0):
                self.dir.y *= -1 *1.1

        self.rect = self.image.get_rect(center = (round(self.pos.x), round(self.pos.y)))


# Classes representing obstacles
class ObstacleRectangle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, width, height))
        self.rect = self.image.get_rect(center=(x, y))

class ObstacleTriangle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, angle):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, color, [(0, 0), (width, 0), (0, height)], angle)
        self.rect = self.image.get_rect(center=(x, y))
        self.image = pygame.transform.rotate(self.image, angle)
        #self.rect = self.image.get_rect(center=self.rect.center)

class ObstacleCircle(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))

class WinningArea(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (0, 255, 0), (0, 0, 40, 40))
        self.rect = self.image.get_rect(center=(x, y))

class NearWinningArea(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (200, 255, 200), (0, 0, 40, 40))
        self.rect = self.image.get_rect(center=(x, y))
    
# Generate ball function (i - number of balls)
def generate_ball(i, obstacles_group, winning_area):
    x = 30
    y = 150 + 15 * i
    radius = 5
    color = colors[i % len(colors)]
    direction = pygame.math.Vector2(1, 0).rotate(random.randrange(360))
    return Ball((x, y), direction, radius, color, obstacles_group, winning_area)


# Initialize map
def initialize():
    # Create gropu of sprites
    obstacles_group = pygame.sprite.Group()
    winning_area = pygame.sprite.Group()
    nwa = pygame.sprite.Group()
    balls = [generate_ball(i, obstacles_group, winning_area) for i in range(10)]
    balls_group = pygame.sprite.Group()

    # Obstacles (0 - empty area, 1 - wall, 2,3,4,5- triangle, 6-circle wall)
    obstacles = [
        [6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 6],
        [0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0],
        [0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 6, 0, 0, 0, 1, 1, 1, 0, 0, 6, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 6, 0, 0, 0, 1, 2, 1, 0, 0, 6, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 6, 0, 0, 0, 1, 1, 1, 0, 0, 6, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 6],
    ]

    # Adding ball to balls_gruop
    for ball in balls:
        balls_group.add(ball)

    # Adding obstacles to obstacles_gruop
    for y, row in enumerate(obstacles):
        for x, cell in enumerate(row):
            if cell == 1:
                # #
                # #
                obstacle = NearWinningArea(x * 40, y * 40)
                nwa.add(obstacle)
            elif cell == 2:
                #
                # #
                # # # 
                # # # #                
                obstacle = WinningArea(x * 40, y * 40)
                winning_area.add(obstacle)

            elif cell == 3:
                      #
                    # #
                  # # #
                # # # #
                obstacle = ObstacleTriangle(x*40, y*40, 50, 50, white, 30)
                obstacles_group.add(obstacle)
            elif cell == 4:
                # # # #
                  # # #
                    # #
                      #
                obstacle = ObstacleTriangle(x*40, y*40, 50, 50, white, 30)
                obstacles_group.add(obstacle)
            elif cell == 5:
                # # # #
                # # # #
                # #
                #
                obstacle = ObstacleTriangle(x*40, y*40, 50, 50, white, 0)
                obstacles_group.add(obstacle)
            elif cell == 6:
                  # # 
                # # # #
                  # #
                obstacle = ObstacleCircle(x*42, y*42, 25, white)
                obstacles_group.add(obstacle)

    return balls_group, obstacles_group, winning_area, nwa


# Main loop
def main():
    simulation_started = False
    clock = pygame.time.Clock()

    balls_group, obstacles_group, winning_area, nearwinningarea = initialize()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                simulation_started = True

        if simulation_started:
            # Update position
            for ball in balls_group:
                if not ball.is_winner:
                    ball.update_position()
                    collision_list = pygame.sprite.spritecollide(ball, balls_group, False, collided = pygame.sprite.collide_circle)
                    for obstacle in collision_list:
                        distance_vec = ball.pos - obstacle.pos
                        if 0 < distance_vec.length_squared() < (ball.radius + obstacle.radius) ** 2:
                            ball.dir.reflect_ip(distance_vec)
                            obstacle.dir.reflect_ip(distance_vec)
                            break
                    ball.collision_with_obstacles()
                    ball.check_winning_condition()
                else:
                    font = pygame.font.Font(None, 80)
                    text = font.render(f"Ball {ball.name} won!", True, (ball.color))
                    text_rect = text.get_rect(center=(width // 2, height // 2))
                    pygame.draw.rect(screen, (200, 200, 200), (text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20))
                    screen.blit(text, text_rect)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    break


        screen.fill(black)

        # Drawing sprites
        nearwinningarea.draw(screen)
        obstacles_group.draw(screen)
        winning_area.draw(screen)
        balls_group.draw(screen)

        pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    main()