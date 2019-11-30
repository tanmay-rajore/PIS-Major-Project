import numpy as np
import cv2
from collections import deque
import serial
from tkinter import Tk
root = Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
ser=serial.Serial('/dev/cu.usbmodem14201', baudrate=9600, timeout=0.1)
# Define the upper and lower boundaries for a color to be considered "Blue"
blueLower = np.array([100, 60, 60])
blueUpper = np.array([140, 255, 255])

# Define a 5x5 kernel for erosion and dilation
kernel = np.ones((5, 5), np.uint8)

# Setup deques to store separate colors in separate arrays

colors = [(0,0,0),(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255),(255,0,255),(255,255,0),(255,255,255)]
colorIndex = 0

# Setup the Paint interface
paintWindow = np.zeros((500,800,3))
cv2.namedWindow("Paint", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Paint",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
# Load the video
camera = cv2.VideoCapture(0)
camera.set(3,1024)
camera.set(4,512)
# Keep looping
previous=(600,300)
ser.flush()
while 1:
    ser.flush()
    try:
        arduino=ser.readline()[0:-1].decode('utf-8')
    except:
        pass
    print(arduino)

    # Grab the current paintWindow
    (grabbed, frame) = camera.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Check to see if we have reached the end of the video
    if not grabbed:
        break

    # Determine which pixels fall within the blue boundaries and then blur the binary image
    blueMask = cv2.inRange(hsv, blueLower, blueUpper)
    blueMask = cv2.erode(blueMask, kernel, iterations=2)
    blueMask = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel)
    blueMask = cv2.dilate(blueMask, kernel, iterations=1)

    # Find contours in the image
    (cnts,_) = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    center = (0,0)
        # Check to see if any contours were found
    if len(cnts) > 0:
        # Sort the contours and find the largest one -- we
        # will assume this contour correspondes to the area of the bottle cap
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        if(cv2.contourArea(cnt)>1200 and cv2.contourArea(cnt)<20000):
            # Get the radius of the enclosing circle around the found contour
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)
            # Draw the circle around the contour
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            # Get the moments to calculate the center of the contour (in this case Circle)
            M = cv2.moments(cnt)
            center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
            if(arduino[1]=="1"):
                #clear all
                paintWindow[:,:,:] = 0
            elif(arduino[2:5]=="000"):
                colorIndex = 0
            elif(arduino[2:5]=="100"):
                colorIndex = 1 
            elif(arduino[2:5]=="010"):
                colorIndex = 2
            elif(arduino[2:5]=="001"):
                colorIndex = 3 
            elif(arduino[2:5]=="011"):
                colorIndex = 4
            elif(arduino[2:5]=="101"):
                colorIndex = 5 
            elif(arduino[2:5]=="110"):
                colorIndex = 6 
            elif(arduino[2:5]=="111"):
                colorIndex = 7
            print(colorIndex)
            if(colorIndex==0):
                cv2.line(paintWindow, previous, center, colors[colorIndex], 50)
                cv2.circle(paintWindow, center, 25, colors[colorIndex], -1)
            else:
                cv2.line(paintWindow, previous, center, colors[colorIndex], 4)
                cv2.circle(paintWindow, center, 2, colors[colorIndex], -1)
            previous=center
            #Draw on the board with the current color index
    else:
        continue
    # Show the frame and the paintWindow image
    #cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWindow)

    # If the 'q' key is pressed, stop the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
