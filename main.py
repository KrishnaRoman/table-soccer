import pygame
import pymunk
import pymunk.pygame_util

# Initialize the gygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((600,900))

# Title and Icon
pygame.display.set_caption("Table Soccer")
icon = pygame.image.load('Images/copa-mundial.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load("Images/field.jpg")

# pymunk space
space = pymunk.Space()
static_body = space.static_body
draw_options = pymunk.pygame_util.DrawOptions(screen)

# clock
clock = pygame.time.Clock()
FPS = 120

# game variables
dia = 52
team1_image = pygame.image.load('Images/argentina52.png')
team1_image2 = pygame.image.load('Images/argentina.png')
team2_image = pygame.image.load('Images/brazil52.png')
team2_image2 = pygame.image.load('Images/brazil.png')

# Teams' players coordinates
coord_1 = [
    (300,99), (150,225), (300, 200),
    (450,225), (225,350), (375,350)
]

coord_2 = [
    (300,800), (150, 675), (300,700),
    (450,675), (225,550), (375,550)
]

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

# setup game players team_1
team_1 = [create_ball(32, coord_1[0])]
for i in range(1,6):
    new_player = create_ball(dia/2, coord_1[i])
    team_1.append(new_player)

# setup game players team_2
team_2 = [create_ball(32, coord_2[0])]
for i in range(1,6):
    new_player = create_ball(dia/2, coord_2[i])
    team_2.append(new_player)

# create field cushions
cushions = [
    [(24,60), (573,60), (565,67), (32,67)],
    [(24,60), (24,839), (32,832), (32,67)],
    [(32,832), (565,832), (573,839), (24,839)],
    [(565,67), (565,832), (573,839), (573,60)],
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

    # Background Image
    screen.blit(background, (0,0))

    # Players images (goalkepper is bigger)
    # Team 1
    screen.blit(team1_image2, (team_1[0].body.position[0] - team_1[0].radius,
                                team_1[0].body.position[1] - team_1[0].radius))

    for player in team_1[1:]:
        screen.blit(team1_image, (player.body.position[0] - player.radius,
                                    player.body.position[1] - player.radius))

    # Team 2
    screen.blit(team2_image2, (team_2[0].body.position[0] - team_2[0].radius,
                                team_2[0].body.position[1] - team_2[0].radius))

    for player in team_2[1:]:
        screen.blit(team2_image, (player.body.position[0] - player.radius,
                                    player.body.position[1] - player.radius))

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            team_2[0].body.apply_impulse_at_local_point((150, -1500), (0, 0))
        if event.type == pygame.QUIT:
            running = False

    # space.debug_draw(draw_options)

    pygame.display.update()
