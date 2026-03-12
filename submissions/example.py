from src.controller import Controller

class Submission(Controller):
    def info(self):
        self.team_name = "Nombre de ejemplo"
        self.look = 5 # Pon un número del 1 al 5
        self.color = 2 # Pon un número del 0 al 3

    def behavior(self):
        self.go_left()
        self.jump()