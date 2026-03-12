from src.controller import Controller

class Submission(Controller):
    def info(self):
        self.team_name = "Explica Getters"
        self.look = 4 # Pon un número del 1 al 5
        self.color = 2 # Pon un número del 0 al 3

    def behavior(self):
        # Getter checks
        print("-------------------------------------------------------------")
        print("My pos", self.get_x(), self.get_y())
        print("Enemy pos", self.get_enemy_x(), self.get_enemy_y())
        print("Get all fish pos", self.get_list_fish_pos())
        print("Get if fish is dangerous", self.get_list_dangerous_fish())
        print("Get if fish is grabbable", self.get_list_grabbable_fish())
        print("Am I grabbing fish", self.is_grabbing_fish())
        print("Is the enemy grabbing fish", self.is_enemy_grabbing_fish())
        print("Am I unable to go left", self.is_pixel_ground(self.get_x() - 2, self.get_y()))
        print("Am I unable to go right", self.is_pixel_ground(self.get_x() + 34, self.get_y()))
        print("What's the pixel width of the level", self.get_level_x_pixel_size())
        print("What's the pixel height of the level", self.get_level_y_pixel_size())
        print("Level matrix?", self.get_level_matrix())
        print("Where are the left spikes of sudden death?", self.get_left_sudden_death())
        print("Where are the right spikes of sudden death?", self.get_right_sudden_death())
        print("What is on y my pixel per frame speed?", self.get_y_speed())
        print("Is sudden death active?", self.is_sudden_death_active())