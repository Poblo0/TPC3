class Controller:
    def __init__(self):
        self.team_name = "Nombre por defecto"
        self.fgo_right = False
        self.fgo_left = False
        self.fjump = False
        self.fgrab = False
        self.fthrow_right = False
        self.fthrow_left = False
        self.fthrow_down = False
        self.level = None
        self.pixeled_level = None
        self.fish_pos = None
        self.fish_state = None
        self.my_pos = None
        self.other_player_pos = None
        self.look = 1
        self.color = 1
        self.is_first_controller = True
        self.game_time = 0
        self.my_y_speed = 0
    
    def clear(self):
        self.fgo_right = False
        self.fgo_left = False
        self.fjump = False
        self.fgrab = False
        self.fthrow_right = False
        self.fthrow_left = False
        self.fthrow_down = False

    def update(self, fish_pos, fish_state, my_pos, other_player_pos, time, my_y_speed):
        self.fish_pos = fish_pos.copy()
        self.fish_state = fish_state.copy()
        self.my_pos = my_pos
        self.other_player_pos = other_player_pos
        self.game_time = time
        self.my_y_speed = my_y_speed

    def set_level(self, level):
        self.level = [sublist[:] for sublist in level] # this way competitors can't modify the real level
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                if self.level[i][j] != 'o':
                    self.level[i][j] = ' '

    def make_first_time_pixel_map(self):
        # Initial map matrix
        x_pixels = len(self.level[0]) * 32
        y_pixels = len(self.level) * 32
        self.pixeled_level = [[' '] * x_pixels for _ in range(y_pixels)]
        
        # Add terrain pixel position
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                if (self.level[i][j] == 'o'):
                    for x in range(32):
                        for y in range(32):
                            self.pixeled_level[i * 32 + y][j * 32 + x] = 'o'


    def set_is_first_controller(self, is_first_controller):
        self.is_first_controller = is_first_controller

    # Butons
    def go_right(self):
        self.fgo_right = True

    def go_left(self):
        self.fgo_left = True

    def jump(self):
        self.fjump = True

    def grab(self):
        self.fgrab = True

    def throw_right(self):
        self.fthrow_right = True

    def throw_left(self):
        self.fthrow_left = True

    def throw_down(self):
        self.fthrow_down = True


    # Getters for the game
    def get_go_right(self):
        return self.fgo_right
    
    def get_go_left(self):
        return self.fgo_left
    
    def get_jump(self):
        return self.fjump
    
    def get_grab(self):
        return self.fgrab
    
    def get_throw_right(self):
        return self.fthrow_right
    
    def get_throw_left(self):
        return self.fthrow_left
    
    def get_throw_down(self):
        return self.fthrow_down
    
    def get_look(self):
        return self.look

    def get_color(self):
        return self.color
    
    def get_team_name(self):
        return self.team_name

    #<~~~~<~~~~<~~~~<~~~~<~~~~
    # Getters for players
    #<~~~~<~~~~<~~~~<~~~~<~~~~

    def get_x(self):
        return self.my_pos[0]
    
    def get_y(self):
        return self.my_pos[1]
    
    def get_enemy_x(self):
        return self.other_player_pos[0]
    
    def get_enemy_y(self):
        return self.other_player_pos[1]
    
    # first [] is what fish and second [] is on 0 the x coord and on 1 y
    def get_list_fish_pos(self):
        return self.fish_pos
    
    def get_list_fish_state(self):
        fish = [-1] * len(self.fish_state)
        for i, current in enumerate(self.fish_state):
            if (current == 0 or current == 1 or current == 2 or current == 3):
                fish[i] = current
        return fish
    
    def is_grabbing_fish(self):
        for current in self.fish_state:
            if (self.is_first_controller):
                if (current == 4):
                    return True
            else:
                if (current == 5):
                    return True
        return False
    
    def is_enemy_grabbing_fish(self):
        for current in self.fish_state:
            if (self.is_first_controller):
                if (current == 5):
                    return True
            else:
                if (current == 4):
                    return True
        return False
    
    def is_pixel_ground(self, x, y):
        if (x < 0 or y < 0 or x // 32 > len(self.level[0]) - 1 or y // 32 > len(self.level) - 1):
            return True
        return self.level[y // 32][x // 32] == 'o'
    
    def get_level_x_pixel_size(self):
        return len(self.level[0]) * 32
    
    def get_level_y_pixel_size(self):
        return len(self.level) * 32

    def get_tile_level_matrix(self):
        # Make a clean copy of self.level
        lv_map = [row[:] for row in self.level]

        # First we center the coordinates of the characters and get the approx tile position
        my_tile_x = (self.my_pos[0] + 16) // 32
        my_tile_y = (self.my_pos[1] + 16) // 32
        other_tile_x = (self.other_player_pos[0] + 16) // 32
        other_tile_y = (self.other_player_pos[1] + 16) // 32
        # Add characters position (Your position is 'A' enemy position 'B')
        # When both are in the same position, only 'B' is shown
        lv_map[my_tile_y][my_tile_x] = 'A'
        lv_map[other_tile_y][other_tile_x] = 'B'

        # First we center the coordinates of the fishes and get the approx tile position
        fish_tile_pos = []
        for fish in self.fish_pos:
            fish_tile_pos.append([(fish[0] + 16) // 32, (fish[1] + 16) // 32])
        # Add fish position, represented by its state
        # If grabed it will not be shown
        for fish, state in zip(fish_tile_pos, self.fish_state):
            if(state == 0):
                lv_map[fish[1]][fish[0]] = '0'
            elif(state == 1 or state == 2 or state == 3):
                lv_map[fish[1]][fish[0]] = str(state)

        return lv_map
    
    def get_pixel_level_matrix(self):
        # Make a clean copy of self.pixeled_level
        lv_map = [row[:] for row in self.pixeled_level]

        # Add characters position (Your position is 'A' enemy position 'B')
        # When both are in the same position, only 'B' is shown
        for x in range(32):
            for y in range(32):
                lv_map[y + self.my_pos[1]][x + self.my_pos[0]] = 'A'
                lv_map[y + self.other_player_pos[1]][x + self.other_player_pos[0]] = 'B'

        # Add fish position, represented by its state
        # If grabed it will not be shown
        for fish, state in zip(self.fish_pos, self.fish_state):
            x_fish = fish[0]
            y_fish = fish[1]
            if(state == 0):
                for x in range(8,24):
                    for y in range(32):
                        lv_map[y + y_fish][x + x_fish] = '0'
            elif(state == 1 or state == 2 or state == 3):
                for x in range(2,31):
                    for y in range(3,28):
                        lv_map[y + y_fish][x + x_fish] = str(state)
                                        
        return lv_map
    
    def get_left_sudden_death(self):
        return self.game_time - 420 + 31 - 8

    def get_right_sudden_death(self):
        return self.get_level_x_pixel_size() - self.game_time + 420 + 8 - 31
    
    def get_y_speed(self):
        return self.my_y_speed
    
    def is_sudden_death_active(self):
        if (self.game_time - 420 + 31 > 0):
            return True
        return False