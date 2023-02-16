import pygame
import pymunk
import pymunk.pygame_util
import math

# Sonido
pygame.mixer.init()
sonido_fondo = pygame.mixer.Sound("sound/fans.mp3")
pygame.mixer.Sound.play(sonido_fondo,-1)


# Initialize the gygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((700,900))

# Title and Icon
pygame.display.set_caption("Table Soccer")
icon = pygame.image.load('Images/copa-mundial.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load("Images/field2.png")

# pymunk space
space = pymunk.Space()
static_body = space.static_body
draw_options = pymunk.pygame_util.DrawOptions(screen)

# clock
clock = pygame.time.Clock()
FPS = 120

# game variables
dia = 52
force = 2000

team1_image = pygame.image.load('Images/argentina52.png')
team1_image2 = pygame.image.load('Images/argentina.png')
team2_image = pygame.image.load('Images/brazil52.png')
team2_image2 = pygame.image.load('Images/brazil.png')

# Teams' players default coordinates
# Player 1
coord_1 = [
    (349,101), (199,227), (349, 202),
    (499,227), (274,352), (424,352)
]

coord_offensive_1 = [
    (349,101), (349,302), (399,227),
    (249,352), (449,352), (299,227)
]

coord_deffensive_1 = [
    (349,101), (199,227), (300,202),
    (499,227), (349,352), (400,202)
]

# Player 2
coord_2 = [
    (349,802), (199, 677), (349,702),
    (499,677), (274,552), (424,552)
]

coord_offensive_2 = [
    (349,802), (299,702), (399,702),
    (449,552), (249,552), (349,601)
]

coord_deffensive_2 = [
    (349,802), (199,677), (300,702),
    (499,677), (400,702), (349,552)
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
    [(73,62), (623,62), (614,69), (81,69)],
    [(73,62), (73,841), (81,834), (81,69)],
    [(81,834), (614,834), (622,841), (73,841)],
    [(614,69), (614,834), (622,841), (622,62)],
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
    
    # calculate shot angle
    mouse_pos = pygame.mouse.get_pos()
    x_dist = team_2[0].body.position[0] - mouse_pos[0]
    y_dist = -(team_2[0].body.position[1] - mouse_pos[1])
    angle = math.degrees(math.atan2(y_dist, x_dist))

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_impulse = math.cos(math.radians(angle))
            y_impulse = math.sin(math.radians(angle))
            team_2[0].body.apply_impulse_at_local_point((force * - x_impulse, force * y_impulse), (0, 0))
        if event.type == pygame.QUIT:
            running = False

    # space.debug_draw(draw_options)

    pygame.display.update()
