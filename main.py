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
    shape.elasticity = 0.8
    # use pivot join to add friction
    pivot = pymunk.PivotJoint(static_body, body, (0,0), (0,0))
    pivot.max_bias = 0 # disable joint correction
    pivot.max_force = 1000 # emulate linear friction

    space.add(body, shape, pivot)
    return shape

new_ball = create_ball(25, (300, 300))
cue_ball = create_ball(25, (310, 700))

# create field cushions
cushions = [
    [(24,60), (572,60), (565,67), (32,67)],
    [(24,60), (24,839), (32,832), (32,67)],
    [(32,832), (565,832), (572,839), (24,839)],
    [(565,67), (565,832), (572,839), (572,60)],
]

# function for creating cushions
def create_cushion(poly_dims):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = ((0,0))
    shape = pymunk.Poly(body, poly_dims)
    shape.elasticity = 0.8
    space.add(body, shape)

for c in cushions:
    create_cushion(c)

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
