import math
import random
import sys
import pygame

# UAV SWARM simulation.
# a swarm of drones flies together using "boids" rules (separation, alignment,
# cohesion) plus collision avoidance

W, H = 960, 640
pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("UAV swarm - decentralized formation flight")
font = pygame.font.SysFont("consolas", 18)
clock = pygame.time.Clock()

NUM = 40
MAX_SPEED = 4.0
NEIGHBOR = 70      #basically  how far a drone can see its neighbors
SEP_DIST = 28      # this is like personal space get this close and push apart


class Drone:
    def __init__(self):
        self.x = random.uniform(0, W)
        self.y = random.uniform(0, H)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)


swarm = [Drone() for _ in range(NUM)]
target = [W / 2, H / 2]


def limit(vx, vy, m):
    # cap a vector to max length m
    speed = math.hypot(vx, vy)
    if speed > m:
        vx, vy = vx / speed * m, vy / speed * m
    return vx, vy


def step():
    for d in swarm:
        sep_x = sep_y = 0
        ali_x = ali_y = 0
        coh_x = coh_y = 0
        count = 0

        # look at every nearby drone
        for other in swarm:
            if other is d:
                continue
            dist = math.hypot(other.x - d.x, other.y - d.y)
            if dist < NEIGHBOR:
                count += 1
                # alignment: match neighbors velocity
                ali_x += other.vx
                ali_y += other.vy
                # cohesion: move toward neighbors center
                coh_x += other.x
                coh_y += other.y
                # separation: avoid crashing into close ones
                if dist < SEP_DIST and dist > 0:
                    sep_x -= (other.x - d.x) / dist
                    sep_y -= (other.y - d.y) / dist

        if count:
            ali_x, ali_y = ali_x / count, ali_y / count
            coh_x = (coh_x / count - d.x) * 0.01
            coh_y = (coh_y / count - d.y) * 0.01

        # steer toward the shared target
        tx = (target[0] - d.x) * 0.004
        ty = (target[1] - d.y) * 0.004

        # add all the urges together with weights
        d.vx += sep_x * 1.5 + ali_x * 0.05 + coh_x + tx
        d.vy += sep_y * 1.5 + ali_y * 0.05 + coh_y + ty
        d.vx, d.vy = limit(d.vx, d.vy, MAX_SPEED)

    for d in swarm:
        d.x += d.vx
        d.y += d.vy
        # wrap around the edges
        d.x %= W
        d.y %= H


running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            target[0], target[1] = e.pos

    step()

    screen.fill((12, 14, 22))

    # draw the target
    pygame.draw.circle(screen, (255, 170, 60), (int(target[0]), int(target[1])), 8, 2)

    # draw all  drone as a little arrow pointing where it flies
    for d in swarm:
        ang = math.atan2(d.vy, d.vx)
        tip = (d.x + 10 * math.cos(ang), d.y + 10 * math.sin(ang))
        l = (d.x + 6 * math.cos(ang + 2.5), d.y + 6 * math.sin(ang + 2.5))
        r = (d.x + 6 * math.cos(ang - 2.5), d.y + 6 * math.sin(ang - 2.5))
        pygame.draw.polygon(screen, (120, 200, 255), [tip, l, r])

    screen.blit(font.render(f"{NUM} drones | click to move the target", True, (180, 190, 210)), (14, 14))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
