import pygame
#Vision stuff
# import the necessary packages
from EyeTracking.pyimagesearch.eyetracker import EyeTracker
import cv2

import random
from gamecomponents.gamecomp import Obstacle, Benefit, Square, Score
from gamecomponents.visioncomp import faceTracking
from gamecomponents.constants import *


# Initialize Pygame
pygame.init()
pygame.font.init()



# Set up the game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
square = Square(WIDTH // 2, HEIGHT - SQUARE_SIZE - 10, SQUARE_SIZE)
obstacles = []
benefits = []
lives= 3
score= Score(lives,0)
clock = pygame.time.Clock()
dx=0
obst_move=0
camera = cv2.VideoCapture(0)

while True:
    (dx, obst_move)=faceTracking(camera)
        
         
    screen.fill(WHITE)
    square.move(dx)
    square.draw(screen)
    score.checkRecord()
    score.draw(screen)
    if random.randint(0, 50) < 3 & obst_move>0 :  # 2% chance to create a new obstacle every frame
        obstacles.append(Obstacle(random.randint(0, WIDTH - OBSTACLE_WIDTH), -OBSTACLE_HEIGHT, 
                                  OBSTACLE_WIDTH*random.randint(10,500)/100, OBSTACLE_HEIGHT,random.randint(1,3)))
    if random.randint(0, 500) < 2 & obst_move>0 :  # 2% chance to create a new obstacle every frame
        benefits.append(Benefit(random.randint(0, WIDTH - OBSTACLE_WIDTH), -OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
    
    for benefit in benefits:
        benefit.move(obst_move)
        benefit.draw(screen)
        if benefit.off_screen():
            benefits.remove(benefit)
        if benefit.hits(square):
            score.updateScore(0,1)
            benefits.remove(benefit)


    for obstacle in obstacles:
        obstacle.move(obst_move)
        obstacle.draw(screen)
        if obstacle.off_screen():
            obstacles.remove(obstacle)
            score.updateScore(1)
        if obstacle.hits(square):  # game over if an obstacle hits the square
            #obstacles = []
            obstacles.remove(obstacle)
            score.updateScore(0,-1)
            square = Square(WIDTH // 2, HEIGHT - SQUARE_SIZE - 10, SQUARE_SIZE)

    pygame.display.flip()
    clock.tick(120)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if score.num_lives<1:
        pygame.QUIT
        pygame.quit()

        print ("GAME OVER")
    for event in pygame.event.get():
        if event.type == pygame.QUIT or score.num_lives<1:
            pygame.quit()
            print ("GAME OVER")

            camera.release()
            cv2.destroyAllWindows()
        
        
        
camera.release()
cv2.destroyAllWindows()
        
    
    #elif keys[pygame.K_LEFT]:
    #    dx = -SPEED
    #elif keys[pygame.K_RIGHT]:
    #    dx = SPEED
    #else:
    #    dx=0
  