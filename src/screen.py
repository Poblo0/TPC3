import pygame

def calculate_scaling_and_position(window_width, window_height, level_width, level_height):
    window_ratio = window_width / window_height
    level_ratio = level_width / level_height
    if window_ratio > level_ratio:
        scale = window_height / level_height
        scaled_width = int(level_width * scale)
        scaled_height = window_height
        x_offset = (window_width - scaled_width) // 2
        y_offset = 0
    else:
        scale = window_width / level_width
        scaled_width = window_width
        scaled_height = int(level_height * scale)
        x_offset = 0
        y_offset = (window_height - scaled_height) // 2
    return scaled_width, scaled_height, x_offset, y_offset

def draw_game(window, game_surface, level):
    scaled_width, scaled_height, x_offset, y_offset = calculate_scaling_and_position(
        *window.get_size(), level.get_width(), level.get_height()
    )
    scaled_surface = pygame.transform.scale(game_surface, (scaled_width, scaled_height))
    window.blit(scaled_surface, (x_offset, y_offset))
    pygame.display.flip()