import numpy as np
import pandas as pd
from math import ceil, floor, sqrt, cos, sin, radians
import random

path = r'car.csv'

size_of_pixel = .5
unitsPerPixel = 1 / size_of_pixel

initX = 207.5
initY = 13.5
initHeading = 1.5708

carCircleHitboxRadius = 11
matrixCarCircleHitboxRadius = int(carCircleHitboxRadius * unitsPerPixel)


stepForwardSize = 8

stepSideSize = 7
angleSide = 0.0558505
stepSideY = 2.09673
stepSideX = 0.11723

class SafetyData(): # TODO ROMAN I GOT A JOB FOR YOU
    #TODO run the maping and updating of current location
    def __init__(self):
        #cars x and y location given as double as mid of car
        self.carX = initX
        self.carY = initY
        #which is in cms and since the matrix has 0.5cm resolution, the carX and carY should be multiplied by 2 to get the correct index of the matrix.
        self.matrixCarX = int(self.carX * unitsPerPixel)
        self.matrixCarY = int(self.carY * unitsPerPixel)
        
        self.heading = initHeading
        
        #import 0s and 1s from the csv file into a matrix that is 446 in y and QD by x
        self.A = np.loadtxt(path, delimiter=",", dtype=int)
        
        self.recovery = 0
        self.last_step = None
        self.last_heading = 0


    def update(self, move): # move = tuple of (angle, throttle)
        angle, throttle = move
        
        deltaX = cos(self.heading)
        deltaY = sin(self.heading)
        
        if angle == 0:
            self.carX += deltaX * throttle * stepForwardSize
            self.carY += deltaY * throttle * stepForwardSize
        elif angle != 0:
            if self.heading > 1.5708*3.5:
                self.carX += deltaX * throttle * stepSideSize 
                self.carY += deltaY * throttle * stepSideSize * 1.3
            elif self.heading > 1.5708*2.5:
                self.carX += deltaX * throttle * stepSideSize * 1.3
                self.carY += deltaY * throttle * stepSideSize 
            elif self.heading > 1.5708*1.5:
                self.carX += deltaX * throttle * stepSideSize 
                self.carY += deltaY * throttle * stepSideSize * 1.3
            elif self.heading > 1.5708*0.5:
                self.carX += deltaX * throttle * stepSideSize * 1.3
                self.carY += deltaY * throttle * stepSideSize
            else:
                self.carX += deltaX * throttle * stepSideSize 
                self.carY += deltaY * throttle * stepSideSize * 1.3
        
        self.matrixX = int(self.carX * unitsPerPixel)
        self.matrixY = int(self.carY * unitsPerPixel)
            
        self.heading -= angle * angleSide
        
        if self.heading < 0:
            self.heading += 6.28319
        elif self.heading >= 6.28319:
            self.heading -= 6.28319
        
    def is_crashed(self) -> bool:
        return self.check_collisions(self.carX, self.carY, carCircleHitboxRadius)
    def recover(self, move):
        angle, throttle = move
        throttle = throttle
        self.update((-angle, -throttle))
        
        #angle = random.choice([-1, 0, 1])
        angle = 0
        self.update((angle, -throttle))
        return (angle, -throttle)
    
    
    def check_collisions(self, x: float, y: float, r: float) -> bool:
        start_x = max(0, floor((x - r) / size_of_pixel))
        end_x = min(self.A.shape[0]-1, ceil((x + r) / size_of_pixel))
        start_y = max(0, floor((y - r) / size_of_pixel))
        end_y = min(self.A.shape[1]-1, ceil((y + r) / size_of_pixel))

        pixel_radius = size_of_pixel / sqrt(2)

        for x_i in range(start_x, end_x + 1):
            for y_i in range(start_y, end_y + 1):
                if self.A[x_i, y_i] == 1 and \
                    (x - x_i * size_of_pixel) ** 2 + (y - y_i * size_of_pixel) ** 2 <= (r + pixel_radius) ** 2:
                    return True
        return False