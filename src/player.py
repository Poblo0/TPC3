import pygame
from src.image import get_player_sprites

class Player:
    def __init__(self, x, y, char_index, color_index, level):
        self.x = x
        self.y = y
        self.walk_speed = 2
        self.jump_speed = -7
        self.max_fall_speed = 7
        self.y_speed = 0
        self.sub_speed = 0
        self.alive = True
        self.in_ground = False
        self.facing = True
        self.holding_puf = False
        self.level = level
        self.walked = False
        self.animation = 0
        self.current_frame = 0
        self.sprites = get_player_sprites(char_index, color_index)

    def control(self, left, right, jump):
        self.walked = False
        if (right):
            self.walked = True
            self.x += self.walk_speed
            self.facing = False
        if (left):
            self.walked = True
            self.x -= self.walk_speed
            self.facing = True
        if (jump and self.in_ground):
            self.y_speed = self.jump_speed
        if (self.y_speed < self.max_fall_speed):
            if (self.sub_speed == 3 or self.in_ground): # How many frames it takes to decrease y_speed
                self.y_speed += 1
                self.sub_speed = 0
            else:
                self.sub_speed += 1
        self.in_ground = False
        self.x_collision()
        self.y_collision()

    def fish_jump(self):
        self.y_speed = self.jump_speed

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def get_pos(self):
        return (self.x, self.y)
    
    def get_facing(self):
        return self.facing
    
    def get_tile(self, x, y):
        if self.level[y // 32][x // 32] == 'o':
            return True
        return False
    
    def get_y_speed(self):
        return self.y_speed

    def y_collision(self):
        if (self.y_speed >= 0 and (self.get_tile(self.x, self.y + 32 + self.y_speed) or self.get_tile(self.x + 31, self.y + 32 + self.y_speed))):
            tile_y = ((self.y + 32 + self.y_speed) // 32) * 32
            self.y = tile_y - 32  # Place character just above the tile
            self.y_speed = 0
            self.in_ground = True
        elif (self.y_speed <= 0 and (self.get_tile(self.x, self.y + self.y_speed)
                                     or self.get_tile(self.x + 31, self.y + self.y_speed))):
            tile_y = ((self.y + self.y_speed) // 32) * 32
            self.y = tile_y + 32
            self.y_speed = 0
        self.y += self.y_speed

    def draw(self, surface):
        if (not self.in_ground):
            if (self.y_speed < 0):
                self.current_frame = 1
                self.animation = 0
            else:
                self.current_frame = 2
                self.animation = 0
        elif (self.walked):
            self.current_frame = (self.animation // 6) % (len(self.sprites) - 1) + 1 
            self.animation = (self.animation + 1) % ((len(self.sprites) - 1) * 6)
        else:
            self.animation = 0
            self.current_frame = 0
        if (self.facing):
            flipped_img = pygame.transform.flip(self.sprites[self.current_frame], True, False)
            surface.blit(flipped_img, (self.x, self.y))
        else: surface.blit(self.sprites[self.current_frame], (self.x, self.y))

    def x_collision(self):
        if (((self.y_speed <= 0 and self.get_tile(self.x + 32, self.y)) or (self.y_speed >= 0 and self.get_tile(self.x + 32, self.y + 31)))):
            self.x = self.x - self.x % 32
        elif (((self.y_speed <= 0 and self.get_tile(self.x, self.y)) or (self.y_speed >= 0 and self.get_tile(self.x, self.y + 31)))):
            self.x = self.x + 32 - (self.x) % 32