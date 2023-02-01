import pygame

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

# Game Loop
running = True
while running:

    # RGB background color
    screen.fill((255,255,255))
    screen.blit(background, (0,0))

    #Background Image
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
