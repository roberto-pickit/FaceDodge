import pygame
from Game.gamecomponents.constants import *
#Vision stuff
# import the necessary packages
from EyeTracking.pyimagesearch.eyetracker import EyeTracker
from EyeTracking.pyimagesearch import imutils
import cv2


# Initialize camera

# construct the eye tracker
et = EyeTracker("EyeTracking/cascades/haarcascade_frontalface_default.xml","EyeTracking/cascades/haarcascade_eye.xml")


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


    def draw(self, screen):
        textsurface = self.myfont.render('Score: ' + str(self.num_obst_survived)+' Lives: ' + str(self.num_lives), False, (0, 0, 0))
        screen.blit(textsurface, (50, 50))  # adjust coordinates as needed
        
    def updateScore(self, obst, death=0):
        self.num_obst_survived+=obst
        self.num_lives+=death
        if obst<0:
            self.num_obst_survived=0


def faceTracking(camera):
        (grabbed, frame) = camera.read()
        if not grabbed:
            print("Unable to access camera")
            exit(1)
        frame = imutils.resize(frame, width = 300) 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # detect faces and eyes in the image
        detections = et.track(gray)
        rectface= detections[0]
        if len(rectface)!=0: 
            obst_move=OBST_SPEED
            cv2.rectangle(frame, (rectface[0], rectface[1]), (rectface[2], rectface[3]), (0, 255, 0), 2)
            if (rectface[0]+rectface[2]/2>270):
                dx = -SPEED*2
            elif(rectface[0]+rectface[2]/2>220):
                dx = -SPEED
            elif(rectface[0]+rectface[2]/2<130):
                dx = SPEED*2
            elif (rectface[0]+rectface[2]/2<180):
                dx = SPEED
            else:
                dx= 0
        else:
            obst_move= 0
            dx=0
        frame = cv2.flip(frame, 1)
        cv2.imshow("Video streaming", frame)
        return dx, obst_move