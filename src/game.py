import pygame
import sys
from src.level import Level
from src.screen import draw_game
from src.image import chop_into_frames
from src.player import Player
from src.fish import Fish
from src.sudden_death import SuddenDeath

pygame.init()

SCALE_FACTOR = 1  # Scale factor to enlarge the window
window = pygame.display.set_mode((600, 400), pygame.RESIZABLE) 
pygame.display.set_caption("TPC3")
base_resolution = None
center = None
# Create a counter for the points of each team
team_points = [0, 0]
# Create a list to check if a team has died
death = [False, False]
# Get team names
team_names = ["Pablo's cool long team name", "Dani"]
# Create the text font that counts each teams points
font = pygame.font.Font(None, 28)
# Create a fixed-resolution surface
base_surface = None

# Load images
tileset = chop_into_frames(pygame.image.load("./assets/tileset.png").convert_alpha(), 32 , 32)
background = chop_into_frames(pygame.image.load("./assets/background.png").convert_alpha(), 32 , 32)
fish_sprites = chop_into_frames(pygame.image.load("./assets/Pufferfish.png").convert_alpha(), 32, 32)
sudden_death_sprites = chop_into_frames(pygame.image.load("./assets/SuddenDeath.png").convert_alpha(), 32, 32)
# Create Level
current_level = None

# Create Sudden Death
sudden_death = None

# Create sharks
player_a = None
player_b = None

# Create fish
fish = None

# Create Controllers
controller_1 = None
controller_2 = None

a_holding = False
b_holding = False

# Assign starting frame rate
frame_rate = 60


def set_up(map_file, player1, player2):
    global base_resolution, center, window, base_surface, player_a, player_b, fish, current_level, controller_1, controller_2, a_holding, b_holding, death, sudden_death

    # Read map
    current_level = Level(map_file)

    # Set up screen
    base_resolution = (current_level.get_width() * 32, current_level.get_height() * 32)
    center = (base_resolution[0] / 2, base_resolution[1] / 2)
    # window = pygame.display.set_mode((base_resolution[0] * SCALE_FACTOR, base_resolution[1] * SCALE_FACTOR), pygame.RESIZABLE) 
    # window = pygame.display.set_mode((800, 600), pygame.RESIZABLE) 
    base_surface = pygame.Surface(base_resolution)
    window.fill((0, 0, 0))
    pygame.display.flip()

    controller_1 = player1
    controller_2 = player2
    controller_1.info()
    controller_2.info()
    controller_1.set_is_first_controller(True)
    controller_2.set_is_first_controller(False)
    controller_1.set_level(current_level.get_matrix())
    controller_2.set_level(current_level.get_matrix())
    controller_1.make_first_time_pixel_map()
    controller_2.make_first_time_pixel_map()
    team_names[0] = controller_1.get_team_name()
    team_names[1] = controller_2.get_team_name()

    a_pos = current_level.get_a_starting_pos()
    b_pos = current_level.get_b_starting_pos()
    player_a = Player(a_pos[0], a_pos[1], controller_1.get_look(), controller_1.get_color(), current_level.get_matrix())
    player_b = Player(b_pos[0], b_pos[1], controller_2.get_look(), controller_2.get_color(), current_level.get_matrix())

    fish = []
    for pos in current_level.get_fishes_starting_pos():
        fish.append(Fish(pos, current_level.get_matrix()))

    sudden_death = SuddenDeath(current_level.get_width(), current_level.get_height())


    a_holding = False
    b_holding = False

    death[0] = False
    death[1] = False


def loop():
    global current_level, a_holding, b_holding, death, sudden_death, frame_rate

    photo_finish_time = 0
    game_time = 0

    # Main loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # <~~~~Change Frame Rate~~~~>
        keys=pygame.key.get_pressed()
        if (keys[pygame.K_1]): # Normal speed
            frame_rate = 60
        elif (keys[pygame.K_2]): # x2 speed
            frame_rate = 120
        elif (keys[pygame.K_3]): # x4 speed
            frame_rate = 240

        # <~~~~Logic Block~~~~>
        if (not death[0] and not death[1]):
            fish_pos = []
            fish_state = []
            for current in fish:
                fish_pos.append(current.get_pos())
                fish_state.append(current.get_state())
            
            controller_1.clear()
            controller_2.clear()
            controller_1.update(fish_pos, fish_state, player_a.get_pos(), player_b.get_pos(), game_time, player_a.get_y_speed())
            controller_2.update(fish_pos, fish_state, player_b.get_pos(), player_a.get_pos(), game_time, player_b.get_y_speed())
            controller_1.behavior()
            controller_2.behavior()

            player_a.control(controller_1.get_go_left(), controller_1.get_go_right(), controller_1.get_jump())
            player_b.control(controller_2.get_go_left(), controller_2.get_go_right(), controller_2.get_jump())

            # Throws
            if (controller_1.get_throw_down() and a_holding):
                player_a.fish_jump()
                a_holding = False
            if (controller_2.get_throw_down() and b_holding):
                player_b.fish_jump()
                b_holding = False
            if ((controller_1.get_throw_right() or controller_1.get_throw_left()) and a_holding):
                a_holding = False
            if ((controller_2.get_throw_right() or controller_2.get_throw_left()) and b_holding):
                b_holding = False

            for current in fish:
                if (current.behave(player_a.get_pos(), player_b.get_pos(), player_a.get_facing(), player_b.get_facing(),
                                    controller_1.get_grab() and not a_holding, controller_2.get_grab() and not b_holding,
                                    controller_1.get_throw_down(), controller_1.get_throw_right(), controller_1.get_throw_left(),
                                    controller_2.get_throw_down(), controller_2.get_throw_right(), controller_2.get_throw_left())):
                    death[0] = True
                    death[1] = True
                    team_points[0] += 1
                    team_points[1] += 1

                if (current.is_grabbed_by_a()):
                    a_holding = True
                if (current.is_grabbed_by_b()):
                    b_holding = True
                
                if (current.is_hit(player_a.get_pos())):
                    death[0] = True
                    team_points[1] += 1
                if (current.is_hit(player_b.get_pos())):
                    death[1] = True
                    team_points[0] += 1
            if (sudden_death.check_death(game_time, player_a.get_pos())):
                death[0] = True
                team_points[1] += 1
            if (sudden_death.check_death(game_time, player_b.get_pos())):
                death[1] = True
                team_points[0] += 1
            game_time += 1
        else:
            photo_finish_time += 1
            if (photo_finish_time == 60):
                break

        # <~~~~Draw Block~~~~>
        # Draw background
        current_level.draw_background(background, base_surface, 1, 0, 0)
        # Draw map
        current_level.draw(tileset, base_surface, 1, 0, 0)
        # Draw Fishes
        # This part of the code is horrible I know. I just have to finish this project on time and refactoring would take a while
        for current in fish:
            current.draw(base_surface, fish_sprites, player_a.get_facing(), player_b.get_facing())

        # Draw players
        player_a.draw(base_surface)
        player_b.draw(base_surface)

        # Draw Sudden Death
        sudden_death.draw_spikes(base_surface, sudden_death_sprites, game_time)

        # Draw logos
        # base_surface.blit(logos, (base_resolution[0]-270, 20))

        # Draw text of points
        text_of_points = font.render(team_names[0] + ": " + str(team_points[0]) + " - " + team_names[1] + ": " + str(team_points[1]), True, (255, 255, 255))
        base_surface.blit(text_of_points, (4, 2))

        draw_game(window, base_surface, current_level)

        # Limit to frame_rate FPS
        pygame.time.Clock().tick(frame_rate)