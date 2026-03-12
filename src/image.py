import pygame

# Function to chop the image into individual frames
def chop_into_frames(image, tile_width, tile_height):
    image_width, image_height = image.get_size()
    tiles = []

    for y in range(0, image_height, tile_height):
        for x in range(0, image_width, tile_width):
            # Create a new surface for each tile
            tile = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)
            # Copy the portion of the original image onto the new surface
            tile.blit(image, (0, 0), pygame.Rect(x, y, tile_width, tile_height))
            tiles.append(tile)

    return tiles

# Change three colors of an image
def recolor_three_colors(surface, original_color_a, new_color_a, original_color_b, new_color_b, original_color_c, new_color_c):
    # Lock the surface to directly access pixel data (improves performance)
    surface.lock()
    width, height = surface.get_size()

    for x in range(width):
        for y in range(height):
            # Get the color of the current pixel
            current_color = surface.get_at((x, y))
            # Replace if it matches the original colors
            if current_color[:3] == original_color_a:  # Ignore the alpha channel
                surface.set_at((x, y), new_color_a + (current_color.a,))
            elif current_color[:3] == original_color_b:  # Ignore the alpha channel
                surface.set_at((x, y), new_color_b + (current_color.a,))
            elif current_color[:3] == original_color_c:  # Ignore the alpha channel
                surface.set_at((x, y), new_color_c + (current_color.a,))
    
    # Unlock the surface after modifying pixels
    surface.unlock()

# Given an index recolors the sprites
def fixed_recolor(surface, color_index):
    if (color_index == 1):
        recolor_three_colors(surface, (164, 211, 242), (199, 222, 151), (106, 155, 232), (113, 193, 66), (113, 193, 66), (219, 138, 228))
    elif (color_index == 2):
        recolor_three_colors(surface, (164, 211, 242), (221, 198, 229), (106, 155, 232), (219, 138, 228), (113, 193, 66), (193, 206, 86))
    elif (color_index == 3):
        recolor_three_colors(surface, (164, 211, 242), (221, 219, 182), (106, 155, 232), (193, 206, 86), (113, 193, 66), (106, 155, 232))

# Master function that returns the recolored and chopped sprite sheet of both players 
def get_player_sprites(char_index, color_index):
    image_a = pygame.image.load("./assets/P{}_Walk-Sheet.png".format(char_index)).convert_alpha()
    fixed_recolor(image_a, color_index)
    sprites_a = chop_into_frames(image_a, 32, 32)
    return sprites_a