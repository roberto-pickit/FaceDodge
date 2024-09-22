import pygame
from gamecomponents.constants import *

# Square class
class Square:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def draw(self, surface):
        pygame.draw.rect(surface, RED, pygame.Rect(self.x, self.y, self.size, self.size))

    def move(self, dx):
        self.x += dx
        if self.x <= 0:
            self.x = 0
        elif self.x >= WIDTH - SQUARE_SIZE:
            self.x = WIDTH - SQUARE_SIZE

# Obstacle class
class Obstacle:
    def __init__(self, x, y, width, height,speedmult):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speedmult= speedmult

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, pygame.Rect(self.x, self.y, self.width, self.height))

    def move(self, speed):
        self.y += speed*self.speedmult

    def off_screen(self):
        return self.y > HEIGHT

    def hits(self, square):
        return (square.x < self.x + self.width and square.x + square.size > self.x and
                square.y < self.y + self.height and square.y + square.size > self.y)

# Coin benefit class
class Benefit(Obstacle):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height,1)
    def draw(self, surface):
        pygame.draw.circle(surface, GOLD, (self.x, self.y), self.height/2)


# Score class
class Score:
    def __init__(self,num_lives=3,num_obst_survived=0):
        self.num_lives = num_lives
        self.num_obst_survived= num_obst_survived
        self.myfont = pygame.font.SysFont(None, 30)
        try:
            with open(HIGHSCORE_PATH, 'r') as f:
                high_score = int(f.read())
        except FileNotFoundError:
            high_score = 0  # If the file doesn't exist yet, start with a high score of 0.
        self.highestscore= high_score


    def draw(self, screen):
        textsurface = self.myfont.render('Score: ' + str(self.num_obst_survived)+' Lives: ' + str(self.num_lives) + 
                                         '                                   Record: ' +str(self.highestscore),
                                         False, (0, 0, 0))
        screen.blit(textsurface, (50, 50))  # adjust coordinates as needed
        
    def updateScore(self, obst, death=0):
        self.num_obst_survived+=obst
        self.num_lives+=death
        if obst<0:
            self.num_obst_survived=0

    def checkRecord(self):
        try:
            with open(HIGHSCORE_PATH, 'r') as f:
                high_score = int(f.read())
        except FileNotFoundError:
            high_score = 0  # If the file doesn't exist yet, start with a high score of 0.
        if high_score<self.num_obst_survived:
            self.highestscore=self.num_obst_survived
            with open(HIGHSCORE_PATH, 'w') as f:
                f.write(str(self.num_obst_survived))
