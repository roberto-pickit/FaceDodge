#Vision stuff
# import the necessary packages
from EyeTracking.pyimagesearch.eyetracker import EyeTracker
from EyeTracking.pyimagesearch import imutils
import cv2
from gamecomponents.constants import *


# Initialize camera

# construct the eye tracker
et = EyeTracker("EyeTracking/cascades/haarcascade_frontalface_default.xml","EyeTracking/cascades/haarcascade_eye.xml")


def faceTracking(camera):
        (grabbed, frame) = camera.read()
        if not grabbed:
            print("Unable to access camera")
            exit(1)
        frame = imutils.resize(frame, width = 300) 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # detect faces and eyes in the image
        detections = et.track(gray)
        if len(detections)!=0: 
            rectface= detections[0]
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