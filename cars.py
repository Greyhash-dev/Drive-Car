# This File was written by Greyhash-dev (https://github.com/Greyhash-dev)
# This Program and every Files within it stand under the GNU Affero General Public License v3.0
import pygame
from gascalculator import gas, steering
from rotate import blitRotate
import math


def findIntersect(Ax1, Ay1, Ax2, Ay2, Bx1, By1, Bx2, By2):
    d = (By2 - By1) * (Ax2 - Ax1) - (Bx2 - Bx1) * (Ay2 - Ay1)

    if d:
        uA = ((Bx2 - Bx1) * (Ay1 - By1) - (By2 - By1) * (Ax1 - Bx1)) / d
        uB = ((Ax2 - Ax1) * (Ay1 - By1) - (Ay2 - Ay1) * (Ax1 - Bx1)) / d
    else:
        return
    if not (0 <= uA <= 1 and 0 <= uB <= 1):
        return
    x = Ax1 + uA * (Ax2 - Ax1)
    y = Ay1 + uA * (Ay2 - Ay1)

    return math.sqrt(((Ax1-x)**2)+((Ay1-y)**2))


class car:
    def __init__(self, carid, boarders, showlines):
        self.boarders = boarders    # All the boarders of the game
        self.id = carid  # Every Car has his own ID, can be useful later
        self.car = pygame.image.load("./graphics/car.png")  # Load in the Car graphics
        self.car.set_colorkey((0, 255, 0))  # Everything green gets cut out
        self.position = [350, 500]  # Position Array [x, y]
        self.rotation = 90  # Rotation Variable
        self.gasClass = gas()  # This will be used to calculate the acceleration
        self.origin = [350, 500]  # Position Array after giving it to the rotation Algorithm
        self.rotatedCar = pygame.image.load("./graphics/car.png")  # Car Object after the rotation Algorithm had it.
        self.steerClass = steering(self.rotation)  # Class to calculate the steering
        self.acceleration = 0  # Acceleration of the Car
        self.points = 0
        self.intersections = []     # Intersections of the Lasers as distance
        self.checkpointcolor = 201
        self.gashistory = []
        self.showlines = showlines

    def update(self, gas, steer, fps):
        self.acceleration = self.gasClass.call(gas, self.position[0], fps)  # Calculate the Acceleration
        self.rotation = self.steerClass.call(steer, fps)  # Calculate the Angle of the Car
        self.position[0] -= self.acceleration * math.sin((2 * math.pi * self.rotation) / 360)
        self.position[1] -= self.acceleration * math.cos((2 * math.pi * self.rotation) / 360)
        w, h = self.car.get_size()  # Get Car width and height
        self.rotatedCar, self.origin = blitRotate(self.car, self.position, (w // 2, h // 2),
                                                  self.rotation)  # Rotate Car at center
        self.gashistory.append(self.acceleration)
        if len(self.gashistory) > 60:
            self.gashistory.pop(0)


    def drawlines(self, pos, angle, screen):
        xpos, ypos = pos
        lr = [
            (xpos - 100 * math.sin((2 * math.pi * angle) / 360),
             ypos - 100 * math.cos((2 * math.pi * angle) / 360)),
            (xpos - 100 * math.sin((2 * math.pi * (angle + 45)) / 360),
             ypos - 100 * math.cos((2 * math.pi * (angle + 45)) / 360)),
            (xpos - 100 * math.sin((2 * math.pi * (angle - 45)) / 360),
             ypos - 100 * math.cos((2 * math.pi * (angle - 45)) / 360)),
            (xpos - 100 * math.sin((2 * math.pi * (angle + 90)) / 360),
             ypos - 100 * math.cos((2 * math.pi * (angle + 90)) / 360)),
            (xpos - 100 * math.sin((2 * math.pi * (angle - 90)) / 360),
             ypos - 100 * math.cos((2 * math.pi * (angle - 90)) / 360))
        ]
        if self.showlines:
            pygame.draw.line(screen, (200, 0, 0), (xpos, ypos), lr[0])
            pygame.draw.line(screen, (200, 0, 0), (xpos, ypos), lr[1])
            pygame.draw.line(screen, (200, 0, 0), (xpos, ypos), lr[2])
            pygame.draw.line(screen, (200, 0, 0), (xpos, ypos), lr[3])
            pygame.draw.line(screen, (200, 0, 0), (xpos, ypos), lr[4])
        self.intersections = []
        for _ in lr:
            boardercounter = 0
            x = []
            for boarder in self.boarders:
                y = (findIntersect(xpos, ypos, _[0], _[1], boarder[0][0], boarder[0][1], boarder[1][0],
                                                   boarder[1][1]))
                if y is not None:
                    x.append(y)
                    boardercounter += 1
            if boardercounter == 1:
                self.intersections.append(x[0])
            elif boardercounter == 0:
                self.intersections.append(200)
            else:
                self.intersections.append(min(x))


    def getObject(self):
        return self.rotatedCar

    def getPosition(self):
        return self.position

    def getRotation(self):
        return self.rotation

    def getOrigin(self):
        return self.origin

    def getSize(self):
        return self.car.get_size()

    def respawn(self):
        self.position = [350, 500]
        self.origin = [350, 500]
        self.steerClass.reset()
        self.checkpointcolor = 201
        self.points = 0

    def setpoints(self, points):
        self.points = points

    def getpoints(self):
        return self.points

    def getintersections(self):
        return self.intersections

    def checkpoint(self):
        self.checkpointcolor += 1
        if self.checkpointcolor == 211:
            self.checkpointcolor = 201

    def getcheckpoint(self):
        return self.checkpointcolor

    def getid(self):
        return self.id

    def getgashistory(self):
        return self.gashistory
