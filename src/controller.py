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
    
    def get_list_dangerous_fish(self):
        fish = [False] * len(self.fish_state)
        for i, current in enumerate(self.fish_state):
            if (current == 1 or current == 2 or current == 3):
                fish[i] = True
        return fish
    
    def get_list_grabbable_fish(self):
        fish = [False] * len(self.fish_state)
        for i, current in enumerate(self.fish_state):
            if (current == 0):
                fish[i] = True
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
        if (x < 0 or y < 0 or x // 32 > len(self.level[0]) or y // 32 > len(self.level)):
            return True
        return self.level[y // 32][x // 32] == 'o'
    
    def get_level_x_pixel_size(self):
        return len(self.level[0]) * 32
    
    def get_level_y_pixel_size(self):
        return len(self.level) * 32

    def get_level_matrix(self):
        return self.level
    
    def get_left_sudden_death(self):
        return self.game_time - 105 + 31 - 8

    def get_right_sudden_death(self):
        return self.get_level_x_pixel_size() - self.game_time + 105 + 8 - 31
    
    def get_y_speed(self):
        return self.my_y_speed
    
    def is_sudden_death_active(self):
        if (self.game_time - 105 + 31 > 0):
            return True
        return False