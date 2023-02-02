import pygame
import pymunk
import pymunk.pygame_util

# Initialize the gygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((600,900))

# Title and Icon
pygame.display.set_caption("Table Soccer")
icon = pygame.image.load('copa-mundial.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load("field.jpg")

# pymunk space
space = pymunk.Space()
static_body = space.static_body
draw_options = pymunk.pygame_util.DrawOptions(screen)

# clock
clock = pygame.time.Clock()
FPS = 120

# funcion for creating balls
def create_ball(radious, pos):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radious)
    shape.mass = 5
    # use pivot join to add friction
    pivot = pymunk.PivotJoint(static_body, body, (0,0), (0,0))
    pivot.max_bias = 0 # disable joint correction
    pivot.max_force = 1000 # emulate linear friction

    space.add(body, shape, pivot)
    return shape

new_ball = create_ball(25, (300, 300))
cue_ball = create_ball(25, (310, 700))

# Game Loop
running = True
while running:

    clock.tick(FPS)
    space.step(1/FPS)

    # RGB background color
    screen.fill((0,0,0))
    screen.blit(background, (0,0))

    #Background Image
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            cue_ball.body.apply_impulse_at_local_point((0, -1500), (0, 0))
        if event.type == pygame.QUIT:
            running = False

    space.debug_draw(draw_options)

    pygame.display.update()
