
import numpy as np
import pandas as pd

path = r'mycar\foo.csv'

precisionPerCm = 2

initX = 30
initY = 30
initHeading = 0

carCircleHitboxRadius = 12.5
matrixCarCircleHitboxRadius = int(carCircleHitboxRadius * precisionPerCm)


stepForwardSize = 2.5

stepSideSize = 2.1
angleSide = 3.2
stepSideY = 2.09673
stepSideX = 0.11723


class SafetyData(): # TODO ROMAN I GOT A JOB FOR YOU
    #TODO run the maping and updating of current location
    def __init__(self):
        #cars x and y location given as double as the origin point of it from bottom left:
        self.carX = initX
        self.carY = initY
        #which is in cms and since the matrix has 0.5cm resolution, the carX and carY should be multiplied by 2 to get the correct index of the matrix.
        self.matrixCarX = int(self.carX * precisionPerCm)
        self.matrixCarY = int(self.carY * precisionPerCm)
        
        self.heading = initHeading
        
        #import 0s and 1s from the csv file into a matrix that is 446 in y and QD by x
        hitboxMarix = pd.read_csv(path, header=None).values
        #flip the y axis
        hitboxMarix = np.flip(hitboxMarix, 0)
        print(hitboxMarix[136][2])#top left of the controller hitbox at the left side.

        #make 0s False and 1s True
        hitboxMarix = hitboxMarix.astype(bool)


    def update(self, move): # move = tuple of (angle, throttle)
        angle, throttle = move
        
        self.heading += angle * angleSide
        if self.heading < 0:
            self.heading += 360
        elif self.heading >= 360:
            self.heading -= 360
            
        self.carX
        
        
        self.matrixX = int(self.carX * precisionPerCm)
        self.matrixY = int(self.carY * precisionPerCm)
    def is_crashed(self) -> bool:
        # TODO: check if we crashed
        pass
    def recover(self):
        # TODO: recover from crash
        pass