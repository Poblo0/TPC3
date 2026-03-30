import pygame

class SuddenDeath:
    def __init__(self, level_with, level_height):
        self.level_with = level_with * 32
        self.level_height = level_height * 32
    
    def draw_spikes(self, surface, sprites, time):
        flipped_img = pygame.transform.flip(sprites[1], True, False)
        for y in range(0, self.level_height, 32):
            surface.blit(sprites[1], (time - 420, y))
            surface.blit(flipped_img, (self.level_with - time + 420 - 32, y))
            place = time - 420 -32
            while(place > -32):
                surface.blit(sprites[0], (place, y))
                place -= 32
            place = self.level_with - time + 420
            while(place < self.level_with):
                surface.blit(sprites[0], (place, y))
                place += 32

    def check_death(self, time, pos):
        if (time - 420 + 31 - 8 > pos[0]):
            return True
        elif (self.level_with - time + 420 - 32 + 8 < pos[0] + 31):
            return True
        else:
            return False