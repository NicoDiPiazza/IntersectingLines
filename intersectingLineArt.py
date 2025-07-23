import keyboard
import pygame
import math
import random
from PIL import Image
pygame.init()


def pixelColorLookupTableGenerator(filename, screenWidth, screenHeight):
     # this seems potentially unnecessary, so I won't call it unless I really need to do optimizations later. 
     # I'm leaving it just in case though.
     allColors = [[[] for _ in range(screenWidth)] for _ in range(screenHeight)]
     myImage = Image.open(filename)

     for x in range(screenWidth):
          print (x)
          for y in range(screenHeight):
               allColors[x][y] = myImage.load()[x, y]

     return allColors



def newLine(point: list, color: list, angle: float):
    lineLength = 1000000
    passThroughX = point[0]
    passThroughY = point[1]
    startX = passThroughX - (lineLength * math.cos(angle))
    startY = passThroughY - (lineLength * math.sin(angle))
    endX = passThroughX + (lineLength * math.cos(angle))
    endY = passThroughY + (lineLength * math.sin(angle))
    if (angle > math.pi/2 and False):
        color = [255, 0, 0]

    pygame.draw.line(screen, color, (startX, startY), (endX, endY), 1)

def randomColor():
     r = random.random() * 255
     g = random.random() * 255
     b = random.random() * 255
     return [r, g, b]

def randomPoint(screenWidth, screenHeight):
     x = random.random() * screenWidth
     y = random.random() * screenHeight
     return ([x, y])

def findDeviance(pixel: list, color: list, myImage):
     (r, g, b) = myImage.load()[pixel[0], pixel[1]]

     ## to find deviance I'm just gonna take the root mean sum of the differences in each value
     ## this will provide the distance from one color to the other in 3D rgb color space

     ## this means golf scoring. Low score good, high score bad.

     diffRSquared = (r - color[0]) ** 2
     diffGSquared = (g - color[1]) ** 2
     diffBSquared = (b - color[2]) ** 2

     return (diffRSquared + diffGSquared + diffBSquared) ** (1/2)

## ok so what we do is we iterate over the larger range across the screen based on the distance between intercepts
## (edge cases include when the intersect marking lines are perpendicular, we can handle those pretty easily)
## the distance between two should usually approximate to either screenwidth or screenheight, if not, we can randomly choose one
## so we iterate over that range for one of our, then for the other we solve for it using our beautimous line equation!
## now we have a healthy set of points that we are looking at along the line. Not too big, not too small. It works!
## just the right smattering. Of course, a lookup table in the future would still be nice, however, I guess effieciency isn't essential
## and could simply be a nice touch later with a tiny bit of refactoring.
## anyways, that provides a for loop and all the points, into which you can just plug the deviance function and sum
## 
## iterate this same process for all the angles, and keep the best (lowest) score, with its coresponding angle, 
## and you have the best angle!

def sumDeviance(myImage, m: float, b: float, screenWidth: int, screenHeight: int, leftWallY: float, 
                rightWallY: float, topWallX: float, bottomWallX: float, color: list):
     
     leftWallInside = leftWallY > 0 and leftWallY < screenHeight
     rightWallInside = rightWallY > 0 and rightWallY < screenHeight
     topWallInside = topWallX > 0 and topWallX < screenWidth
     bottomWallInside = bottomWallX > 0 and bottomWallX < screenWidth

     topWallX = math.floor(topWallX)
     bottomWallX = math.floor(bottomWallX)

     totalDeviance = 0

     if(leftWallInside and rightWallInside):
          for x in range(screenWidth):
               y = math.floor(m*x + b)
               totalDeviance = totalDeviance + findDeviance([x, y], color, myImage)

     elif(topWallInside and bottomWallInside):
          for y in range(screenHeight):
               x = math.floor((y - b) / m)
               totalDeviance = totalDeviance + findDeviance([x, y], color, myImage)
     elif(leftWallInside):
          if(topWallInside):
               for x in range(math.floor(topWallX)):
                    y = math.floor(m*x + b)
                    totalDeviance = totalDeviance + findDeviance([x, y], color, myImage)
          elif(bottomWallInside):
               for x in range(math.floor(bottomWallX)):
                    y = math.floor(m*x + b)
                    totalDeviance = totalDeviance + findDeviance([x, y], color, myImage)
     elif(rightWallInside):
          if(topWallInside):
               for x in range(math.floor(screenWidth - topWallX)):
                    y = math.floor(m*(x + topWallX + 1) + b)
                    totalDeviance = totalDeviance + findDeviance([x + topWallX, y], color, myImage)
          elif(bottomWallInside):
               for x in range(math.floor(screenWidth - bottomWallX)):
                    y = math.floor(m*(x + bottomWallX + 1) + b)
                    totalDeviance = totalDeviance + findDeviance([x + bottomWallX, y], color, myImage)
     
     return totalDeviance
     



clock = pygame.time.Clock()
stop = False
t = 100
filename = r'C:\Users\ThinkPad\OneDrive - Oregon State University\Desktop\programming\python\crowd_cheering.jpeg'
myImage = Image.open(filename)
[screenWidth, screenHeight] = myImage.size
screen = pygame.display.set_mode((screenWidth, screenHeight))


while ( stop != True):
     if keyboard.is_pressed('q'):
            stop = True

     (mouseX, mouseY) = pygame.mouse.get_pos()
     for event in pygame.event.get():
       if event.type == pygame.MOUSEMOTION:
            (mouseX, mouseY) = pygame.mouse.get_pos()

    ## calculations

     pixel = randomPoint(screenWidth, screenHeight)
     (r, g, b) = myImage.load()[pixel[0], pixel[1]]
     optimalDeviance = 100000000000000

     for theta in range(32):
          angle = 2 * math.pi / (theta + 1)


     ## line is y = mx + b, or, alternatively, b = y - mx, or, (y-b)/m = x
     ## m = tan(theta)
     ## here we will use c because b was taken by r g b

          c = pixel[1] - (math.tan(angle) * pixel[0])
          m = math.tan(angle)

     ## left wall at x = 0
          leftWallIntersectY = c
     ## top wall at y = 0
          topWallIntersectX = -c / m
     ## bottom wall at y = screenHeight
          bottomWallIntersectX = (screenHeight - c)/m
     ## right wall at x = screenWidth
          rightWallIntersectY = m * screenWidth + c

          specificDeviance = sumDeviance(myImage, m, c, screenWidth, screenHeight, leftWallIntersectY, rightWallIntersectY, topWallIntersectX, 
                    bottomWallIntersectX, [r, g, b])
          if specificDeviance <= optimalDeviance:
               optimalDeviance = specificDeviance
               optimalAngle = angle
          


    ## draw calls
     #screen.fill([0, 0, 0])


     newLine(pixel, [r, g, b], optimalAngle)

     # newLine([0, leftWallIntersectY], [0, 255, 0], 0)
     # newLine([0, rightWallIntersectY], [0, 255, 0], 0)
     # newLine([topWallIntersectX, 0], [0, 255, 0], math.pi /2)
     # newLine([bottomWallIntersectX, 0], [0, 255, 0], math.pi /2)
     pygame.display.update()


     t = t+0.01
    
    #number of frames per second
     clock.tick(100)
    #print(clock.get_fps())
    #updates the frame
     