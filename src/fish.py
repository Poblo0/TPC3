import pygame

class Fish:
    def __init__(self, pos, level):
        self.x = pos[0]
        self.y = pos[1]
        self.y_speed = 0
        self.level = level
        self.size = 32
        self.state = 0 # 0 rest, 1 right, 2 left, 3 falling, 4 player A, 5 player B
        self.animation = 0
        self.walk_speed = 4
    
    def go_right(self):
        self.x += self.walk_speed
        self.animation = (self.animation - 1) % 40 # 40 stay on animation loop and 10 not on first sprite
        self.x_collision()

    def go_left(self):
        self.x -= self.walk_speed
        self.animation = (self.animation + 1) % 40
        self.x_collision()

    def get_tile(self, x, y):
        if self.level[y // 32][x // 32] == 'o':
            return True
        return False

    def y_collision(self):
        self.y_speed += 1
        if (self.y_speed >= 0 and (self.get_tile(self.x, self.y + 32 + self.y_speed) or self.get_tile(self.x + 31, self.y + 32 + self.y_speed))):
            tile_y = ((self.y + 32 + self.y_speed) // 32) * 32
            self.y = tile_y - 32  # Place character just above the tile
            self.y_speed = 0
            if (self.state == 3):
                self.state = 0
        self.y += self.y_speed

    def x_collision(self):
        if (((self.y_speed <= 0 and self.get_tile(self.x + 32, self.y)) or (self.y_speed >= 0 and self.get_tile(self.x + 32, self.y + 31)))):
            self.x = self.x - self.x % 32
            self.state = 2
        elif (((self.y_speed <= 0 and self.get_tile(self.x, self.y)) or (self.y_speed >= 0 and self.get_tile(self.x, self.y + 31)))):
            self.x = self.x + 32 - (self.x) % 32
            self.state = 1

    def small_col(self, pos):
        if ((((self.x + 8 <= pos[0] + 32) and (self.x + 8 >= pos[0])) or ((self.x + 23 <= pos[0] + 32) and (self.x + 24 >= pos[0])))
            and (((self.y + 9 <= pos[1] + 32) and (self.y + 9 >= pos[1])) or ((self.y + 23 <= pos[1] + 32) and (self.y + 23 >= pos[1])))):
            return True
        else:
            return False
        
    def is_hit(self, pos):
        if (self.state == 0 or self.state == 4  or self.state == 5):
            return False
        if ((((self.x + 2 <= pos[0] + 32) and (self.x + 2 >= pos[0])) or ((self.x + 29 <= pos[0] + 32) and (self.x + 30 >= pos[0])))
            and (((self.y + 3 <= pos[1] + 32) and (self.y + 3 >= pos[1])) or ((self.y + 23 <= pos[1] + 32) and (self.y + 23 >= pos[1])))):
            return True
        else:
            return False
        
    def kick(self, pos, facing):
        if (facing):
            if(not self.get_tile(pos[0] - 32, self.y)):
                self.x = pos[0] - 32
            self.state = 2
        else:
            if(not self.get_tile(pos[0] + 32, self.y)):
                self.x = pos[0] + 32
            self.state = 1

    def is_grabbed_by_a(self):
        return self.state == 4
    
    def is_grabbed_by_b(self):
        return self.state == 5
    
    def behave(self, a_pos, b_pos, a_facing, b_facing, a_grab, b_grab, a_down, a_right, a_left, b_down, b_right, b_left):
        # A method that does two things isn't ideal but for this small project it gives more clarity than splitting everything
        # I'm not using a match because some versions of python3 don't have it
        if (self.state == 0):
            if (self.small_col(a_pos) and self.small_col(b_pos)):
                return True
            if (self.small_col(a_pos)):
                if (a_grab):
                    self.state = 4
                else: 
                    self.kick(a_pos, a_facing)
            elif (self.small_col(b_pos)):
                if (b_grab):
                    self.state = 5
                else:
                    self.kick(b_pos, b_facing)
        elif (self.state == 1):
            self.go_right()
            self.y_collision()
        elif (self.state == 2):
            self.go_left()
            self.y_collision()
        elif (self.state == 3):
            self.y_collision()
        elif (self.state == 4):
            if (a_down):
                if (not self.get_tile(a_pos[0], self.y + 32)):
                    self.x = a_pos[0]
                    self.y = a_pos[1] + 32
                    self.state = 3
                else:
                    self.x = a_pos[0]
                    self.y = a_pos[1]
                    self.state = 3
            elif (a_right):
                self.kick(a_pos, False)
            elif (a_left):
                self.kick(a_pos, True)
            else:
                if (a_facing):
                    self.y = a_pos[1]
                    self.x = a_pos[0] - 20
                else:
                    self.x = a_pos[0] + 20
                    self.y = a_pos[1]
        elif (self.state == 5):
            if (b_down):
                if (not self.get_tile(a_pos[0], self.y + 32)):
                    self.x = b_pos[0]
                    self.y = b_pos[1] + 32
                    self.state = 3
                else:
                    self.x = b_pos[0]
                    self.y = b_pos[1]
                    self.state = 3
            elif (b_right):
                self.kick(b_pos, False)
            elif (b_left):
                self.kick(b_pos, True)
            else:
                if (b_facing):
                    self.y = b_pos[1]
                    self.x = b_pos[0] - 20
                else:
                    self.x = b_pos[0] + 20
                    self.y = b_pos[1]
        return False

    def draw(self, surface, sprites, a_facing, b_facing):
        # A method that does two things isn't ideal but for this small project it gives more clarity than splitting everything
        # I'm not using a match because some versions of python3 don't have it
        if (self.state == 0):
            surface.blit(sprites[0], (self.x, self.y))
        elif (self.state == 1):
            surface.blit(sprites[self.animation // 10 + 1],(self.x, self.y))
        elif (self.state == 2):
            surface.blit(sprites[self.animation // 10 + 1], (self.x, self.y))
        elif (self.state == 3):
            surface.blit(sprites[5], (self.x, self.y))
        elif (self.state == 4):
            if (a_facing):
                flipped_img = pygame.transform.flip(sprites[0], True, False)
                surface.blit(flipped_img, (self.x, self.y))
            else:
                surface.blit(sprites[0], (self.x, self.y))
        elif (self.state == 5):
            if (b_facing):
                flipped_img = pygame.transform.flip(sprites[0], True, False)
                surface.blit(flipped_img, (self.x, self.y))
            else:
                surface.blit(sprites[0], (self.x, self.y))

    def get_pos(self):
        return (self.x, self.y)
    
    def get_state(self):
        return self.state