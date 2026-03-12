from src.controller import Controller
import pygame

class Submission(Controller):

    def info(self):
        self.team_name = "Teclado"
        self.look = 1
        self.color = 2

    def behavior(self):
        keys=pygame.key.get_pressed()
        if (keys[pygame.K_a]):
            self.go_left()
        if (keys[pygame.K_d]):
            self.go_right()
        if (keys[pygame.K_SPACE]):
            self.jump()
        if (keys[pygame.K_UP]):
            self.grab()
        if (keys[pygame.K_DOWN]):
            self.throw_down()
        if (keys[pygame.K_RIGHT]):
            self.throw_right()
        if (keys[pygame.K_LEFT]):
            self.throw_left()
