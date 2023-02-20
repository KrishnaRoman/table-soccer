import pygame, sys
from button import Button

import pymunk
import pymunk.pygame_util
import math


pygame.init()

SCREEN = pygame.display.set_mode((1000, 720))
pygame.display.set_caption("Table Soccer")

BG = pygame.image.load("assets/HD1.jpg")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():
    
    # Create the screen
    PLAY_MOUSE_POS = pygame.mouse.get_pos()
    SCREEN = pygame.display.set_mode((950,900))
    # Background
    BG = pygame.image.load("Images/field.png")
    scoreboard = pygame.image.load("Images/scoreboard.png")
    landscape = pygame.image.load("Images/landscape.jpeg")
    #Arrow
    arrow_image = pygame.image.load("Images/right-arrow.png")

    # pymunk space
    space = pymunk.Space()
    static_body = space.static_body
    draw_options = pymunk.pygame_util.DrawOptions(SCREEN)

    # clock
    clock = pygame.time.Clock()
    FPS = 16

    # game variables
    dia = 52
    force = 0
    max_force = 2000
    force_direction = 1
    powering_up = False
    scored_1 = False
    scored_2 = False
    team1_score = 0
    team2_score = 0
    game_running = True
    turn_player2 = False

    # colours
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)

    # fonts
    font = pygame.font.SysFont("Lato", 60)
    #font = pygame.transform.rotate(original_font, 90)
    large_font = pygame.font.SysFont("Lato", 90)

    name1 = 'argentina'
    name2 = 'brazil'


    team1_image = pygame.image.load(f'Images/{name1}52.png')
    team1_image2 = pygame.image.load(f'Images/{name1}.png')
    team2_image = pygame.image.load(f'Images/{name2}52.png')
    team2_image2 = pygame.image.load(f'Images/{name2}.png')
    ball_image = pygame.image.load('Images/ball.png')

    rotated_1 = pygame.transform.rotate(team1_image, 90)
    rotated_2 = pygame.transform.rotate(team2_image, 90)

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
    # function for outputting text onto the screen
    def draw_text(text, font, text_col, x, y, rotated=True):
        img = font.render(text, True, text_col)
        if rotated:
            img = pygame.transform.rotate(img, 270)
        SCREEN.blit(img, (x, y))

    # funcion for creating balls
    def create_ball(radious, pos, mass = 5, elasticity = 0.8, friction = 300): # elasticity = 0.8, mass = 5
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Circle(body, radious)
        shape.mass = mass
        shape.elasticity = elasticity
        # use pivot join to add friction
        pivot = pymunk.PivotJoint(static_body, body, (0,0), (0,0))
        pivot.max_bias = 0 # disable joint correction
        pivot.max_force = friction # emulate linear friction

        space.add(body, shape, pivot)
        return shape

    ball = create_ball(16, (350,450), 2, 0.8, 150)

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

    # create lines of goal
    goals = [62, 842]

    # create field cushions
    cushions = [
        [(73,62), (243,62), (251,70), (81,70)],
        [(243,13), (243,62), (251,70), (251,21)],
        [(452,13), (243,13), (251,21), (444,21)],
        [(452,13), (452,62), (444,70), (444,21)],
        [(452,62), (622,62), (614,70), (444,70)],
        [(73,62), (73,842), (81,834), (81,70)],
        [(73,842), (243,842), (251,834), (81,834)],
        [(243,891), (243,842), (251,834), (251,883)],
        [(452,891), (243,891), (251,883), (444,883)],
        [(452,891), (452,842), (444,834), (444,883)],
        [(452,842), (622,842), (614,834), (444,834)],
        [(614,70), (614,834), (622,842), (622,62)],
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

    class Arrow():
        def __init__(self, pos):
            self.original_image = arrow_image
            self.angle = 0
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect()
            self.rect.center = pos

        def update(self, angle):
            self.angle = angle

        def draw(self, surface):
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            surface.blit(self.image,
                (self.rect.centerx - self.image.get_width()/2,
                self.rect.centery - self.image.get_height()/2)
            )

    selected = None
    
    # Create power bars to show how hard the player will hit
    power_bar = pygame.Surface((10,20))
    power_bar.fill(RED)

    running=True
    while running:
                
        # Game Loop

        clock.tick(FPS)
        space.step(1/FPS)

        # Background Image
        SCREEN.blit(BG, (0,0))

        # Landscape
        SCREEN.blit(landscape, (700,0))

        # Scoreboard
        SCREEN.blit(scoreboard, (700,322))



        # Check if any team scored
        if ball.body.position[1] < goals[0] - ball.radius:
            scored_2 = True
        elif ball.body.position[1] > goals[1] + ball.radius:
            scored_1 = True

        # Players images (goalkepper is bigger)
        # Team 1
        SCREEN.blit(team1_image2, (team_1[0].body.position[0] - team_1[0].radius,
                                    team_1[0].body.position[1] - team_1[0].radius))

        for player in team_1[1:]:
            SCREEN.blit(team1_image, (player.body.position[0] - player.radius,
                                        player.body.position[1] - player.radius))

        # Team 2
        SCREEN.blit(team2_image2, (team_2[0].body.position[0] - team_2[0].radius,
                                    team_2[0].body.position[1] - team_2[0].radius))

        for player in team_2[1:]:
            SCREEN.blit(team2_image, (player.body.position[0] - player.radius,
                                        player.body.position[1] - player.radius))

        # ball
        SCREEN.blit(ball_image, (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))

        # check if all the objects have stopped moving
        taking_shot = True
        for player in team_1+team_2+[ball]:
            if int(player.body.velocity[0]) != 0 or int(player.body.velocity[1]) != 0:
                taking_shot = False
                selected = None

        # calculate shot angle
        if taking_shot and game_running:
            if scored_1 or scored_2:
                # reposition players
                coord = coord_1+coord_2
                for i, player in enumerate(team_1+team_2):
                    player.body.position = coord[i]
                ball.body.position = (350, 450)
                team1_score += scored_1
                team2_score += scored_2
                scored_1 = False
                scored_2 = False
            if selected:
                arrow = Arrow(selected.body.position)
                PLAY_MOUSE_POS = pygame.mouse.get_pos()
                arrow.rect.center = selected.body.position
                x_dist = -(selected.body.position[0] - PLAY_MOUSE_POS[0])
                y_dist = selected.body.position[1] - PLAY_MOUSE_POS[1]
                angle = math.degrees(math.atan2(y_dist, x_dist))
                arrow.update(angle)

                # Draw arrow
                arrow.draw(SCREEN)

        # powering up seelected player
        if selected and powering_up and game_running:
            force += 100 * force_direction
            if force >= max_force or force <= 0:
                force_direction *= -1
            # draw power bars
            for b in range(math.ceil(force / 400)):
                SCREEN.blit(power_bar,
                (selected.body.position[0] -30 + (b*15),
                selected.body.position[1] + 30 ))
        elif selected and not powering_up and taking_shot:
            x_impulse = math.cos(math.radians(angle))
            y_impulse = math.sin(math.radians(angle))
            selected.body.apply_impulse_at_local_point((force * - x_impulse, force * y_impulse), (0, 0))
            force = 0
            force_direction = 1

        # draw panel
        draw_text(str(team1_score), large_font, WHITE, 785, 375)
        draw_text(str(team2_score), large_font, WHITE, 785, 490)

        SCREEN.blit(rotated_1, (860, 365))
        SCREEN.blit(rotated_2, (860, 480))

        if turn_player2:
            draw_text("Team " + str(turn_player2 + 1) + " turn", font, WHITE, 10, 850, False)
        else:
            draw_text("Team " + str(turn_player2 + 1) + " turn", font, WHITE, 10, 10, False)

        if team1_score >= 3:
            draw_text("TEAM 1 WINS", font, WHITE, 200, 275, False)
            game_running = False
        elif team2_score >= 3:
            draw_text("TEAM 2 WINS", font, WHITE, 200, 600, False)
            game_running = False

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and taking_shot:
                # Check if a player is clicked
                if turn_player2:
                    team = team_2
                else:
                    team = team_1
                PLAY_MOUSE_POS = pygame.mouse.get_pos()
                for player in team:
                    player_x_dist = abs(player.body.position[0] - PLAY_MOUSE_POS[0])
                    player_y_dist = abs(player.body.position[1] - PLAY_MOUSE_POS[1])
                    player_dist = math.sqrt((player_x_dist ** 2) + (player_y_dist ** 2))
                    if player_dist <= player.radius:
                        selected = player
                powering_up = True
            if event.type == pygame.MOUSEBUTTONUP and taking_shot and selected:
                powering_up = False
                turn_player2 = not turn_player2
            if event.type == pygame.QUIT:
                running = False

        # space.debug_draw(draw_options)

        pygame.display.update()




        PLAY_BACK = Button(image=None, pos=(900, 300), 
                            text_input="BACK", font=get_font(25), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(30).render("OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(500, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(500, 460), 
                            text_input="BACK", font=get_font(25), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN = pygame.display.set_mode((1000, 720))
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(70).render("TABLE SOCCER", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(500, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(500, 250), 
                            text_input="PLAY", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(500, 400), 
                            text_input="OPTIONS", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(500, 550), 
                            text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()