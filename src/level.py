# The level class that reads and draws the level
class Level:
    def __init__(self, file_path):
        self.level = None
        self.size = None
        self.a_starting_pos = None
        self.b_starting_pos = None
        self.fishes_starting_pos = None
        self.tile_image_indexes = None
        self.read_level(file_path)
        self.set_tile_images()

    # Makes the level a rectangle
    def make_level_rectangle(self, double_list):
        max_size = 0
        for i in double_list:
            if (len(i) > max_size):
                max_size = len(i)
        for i in double_list:
            while(len(i) < max_size):
                i.append('_')
            i.insert(0, 'o') # Left vertical border
            i.append('o') # Right vertical border
        max_size += 2
        double_list.insert(0, ['o']*max_size) # Upper horizontal border
        double_list.append(['o']*max_size) # Lower horizontal border
        self.level = double_list
        self.size = (max_size, len(self.level))

    # Locates a unique tile
    def locate_tile(self, character):
        for i, line in enumerate(self.level):
            for j, elem in enumerate(line):
                if (character == elem):
                    return (j * 32, i *32)
    
    # Locates all tiles of a given character
    def locate_multiple_tiles(self, character):
        pos_list = []
        for i, line in enumerate(self.level):
            for j, elem in enumerate(line):
                if (character == elem):
                    pos_list.append([j * 32, i *32])
        return pos_list

    # Read the text file of the level
    def read_level(self, file_path):
        with open(file_path, 'r') as file:
            # Read each line, strip the newline, and convert to a list of characters
            self.make_level_rectangle([list(line.strip('\n')) for line in file])
            self.a_starting_pos = self.locate_tile('A')
            self.b_starting_pos = self.locate_tile('B')
            self.fishes_starting_pos = self.locate_multiple_tiles('F')

    # Saves what tiles should be drawn on each 
    # Essentially, it's an autotiling algorithm
    def set_tile_images(self):
        self.tile_image_indexes = [[0] * self.size[0] for _ in range(self.size[1])]
        # Upper and lower row
        # Edges always 8
        for i in range(0, self.size[0]):
            # Upper row
            if (self.level[1][i] != 'o'):
                self.tile_image_indexes[0][i] = 14
            else:
                self.tile_image_indexes[0][i] = 8
            # Lower row
            if (self.level[self.size[1] - 2][i] != 'o'):
                self.tile_image_indexes[self.size[1] - 1][i] = 2
            else:
                self.tile_image_indexes[self.size[1] - 1][i] = 8
        # Left and right borders
        for i in range(1, self.size[1] - 1):
            # Left
            if (self.level[i][1] != 'o'):
                self.tile_image_indexes[i][0] = 9
            else:
                self.tile_image_indexes[i][0] = 8
            # Right
            if (self.level[i][self.size[0] - 2] != 'o'):
                self.tile_image_indexes[i][self.size[0] - 1] = 7
            else:
                self.tile_image_indexes[i][self.size[0] - 1] = 8
        # Evil middle tiles incoming!
        # Ugly af
        for i in range(1, self.size[1] - 1):
            for j in range(1, self.size[0] - 1):
                if (self.level[i][j] == 'o'):
                    if (self.level[i-1][j] == 'o'):
                        if (self.level[i+1][j] == 'o'):
                            if (self.level[i][j+1] == 'o'):
                                if (self.level[i][j-1] == 'o'):
                                    self.tile_image_indexes[i][j] = 8
                                else:
                                    self.tile_image_indexes[i][j] = 7
                            else:
                                if (self.level[i][j-1] == 'o'):
                                    self.tile_image_indexes[i][j] = 9
                                else: 
                                    self.tile_image_indexes[i][j] = 10
                        else:
                            if (self.level[i][j+1] == 'o'):
                                if (self.level[i][j-1] == 'o'):
                                    self.tile_image_indexes[i][j] = 14
                                else:
                                    self.tile_image_indexes[i][j] = 13
                            else:
                                if (self.level[i][j-1] == 'o'):
                                    self.tile_image_indexes[i][j] = 15
                                else: 
                                    self.tile_image_indexes[i][j] = 16
                    else:
                        if (self.level[i+1][j] == 'o'):
                            if (self.level[i][j+1] == 'o'):
                                if (self.level[i][j-1] == 'o'):
                                    self.tile_image_indexes[i][j] = 2
                                else:
                                    self.tile_image_indexes[i][j] = 1
                            else:
                                if (self.level[i][j-1] == 'o'):
                                    self.tile_image_indexes[i][j] = 3
                                else: 
                                    self.tile_image_indexes[i][j] = 4
                        else:
                            if (self.level[i][j+1] == 'o'):
                                if (self.level[i][j-1] == 'o'):
                                    self.tile_image_indexes[i][j] = 11
                                else:
                                    self.tile_image_indexes[i][j] = 5
                            else:
                                if (self.level[i][j-1] == 'o'):
                                    self.tile_image_indexes[i][j] = 17
                                else: 
                                    self.tile_image_indexes[i][j] = 6

    # Draws the whole level
    def draw(self, tileset, surface, scale, x_origin, y_origin):
        for y, line in enumerate(self.tile_image_indexes):
            for x, tile in enumerate(line):
                # Pygame method to draw on a screen
                surface.blit(tileset[tile], (x * 32 * scale + x_origin, y * 32 * scale + y_origin))
    
    def draw_background(self, background, surface, scale, x_origin, y_origin):
        # Upper tiles
        for x in range(1, self.size[0] - 1):
            surface.blit(background[0], (x * 32 * scale + x_origin, 32 * scale + y_origin))
        for x in range(1, self.size[0] - 1):
            surface.blit(background[2], (x * 32 * scale + x_origin, (self.size[1] - 2) * 32 * scale + y_origin))
        # Middle tiles
        for y in range(2, self.size[1] - 2):
            for x in range(1, self.size[0] - 1):
                surface.blit(background[1], (x * 32 * scale + x_origin, y * 32 * scale + y_origin))

    # Get the height for screen
    def get_height(self):
        return len(self.level)
    
    # Get the length for screen
    def get_width(self):
        return len(self.level[0])
    
    def get_a_starting_pos(self):
        return self.a_starting_pos
    
    def get_b_starting_pos(self):
        return self.b_starting_pos
    
    def get_fishes_starting_pos(self):
        return self.fishes_starting_pos
    
    def get_matrix(self):
        return self.level