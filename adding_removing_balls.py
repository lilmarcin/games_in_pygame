import pygame
import sys
import random
import math
import numpy as np

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Adding/Removing balls")

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
    (0, 0, 128),  # granat
    (128, 128, 255)  # purple
]

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color, direction, speed):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.color = color
        self.speed = speed

def generate_ball():
    radius = 10
    x = random.randint(radius, width - radius)
    y = random.randint(radius, height - radius)
    color = random.choice(colors)
    direction = [random.choice([-1, 1]), random.choice([-1, 1])]
    speed = 3
    return Ball(x, y, radius, color, direction, speed)

balls = [generate_ball()]  # 1 kulka na start

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Aktualizacja położenia kulki
    for ball in balls:
        ball.rect.x += ball.speed * ball.direction[0]
        ball.rect.y += ball.speed * ball.direction[1]

        # Ball reflection
        if ball.rect.left - ball.radius // 2 < 0 or ball.rect.right - ball.radius // 2  > width:
            ball.direction[0] *= -1
            # Remove ball with 25% probability
            if random.random() < 0.25:
                balls.remove(ball)
            # Add ball with 25% probability
            elif random.random() > 0.75:
                balls.append(generate_ball())

        if ball.rect.top - ball.radius // 2 < 0 or ball.rect.bottom - ball.radius // 2 > height:
            ball.direction[1] *= -1
            if random.random() < 0.25:
                balls.remove(ball)
            elif random.random() > 0.75:
                balls.append(generate_ball())


    screen.fill(black)

    # Drawing balls
    for ball in balls:
        pygame.draw.circle(screen, ball.color, (int(ball.rect.x), int(ball.rect.y)), ball.radius)


    pygame.display.flip()

    clock.tick(300)
