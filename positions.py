#############################
# This file calculates the physical positions of the various graphics, given values
# such as the screenWidth, screeHeight, boardWidth, and boardHeight. It also includes
# calculations of various angular positions when needed to draw objects and determine
# speed/angle of colliding objects. 
#############################

import graphics
import math
import pygame
import ballClass

# Calculate positions of initial colored balls    
def ballStartPositions(width, margin, height):     
    r = ballClass.Ball.radius
    d = 2*r
    distanceX = d*math.cos(math.pi/6)
    distanceY = d*math.sin(math.pi/6)
    
    firstX = (width-2*margin-2*graphics.Border.innerMargin)*0.73 + margin
    firstY1 = (height-margin)/2
    
    secondX = firstX + distanceX
    secondY1 = firstY1 + distanceY
    secondY2 = firstY1 - distanceY
        
    thirdX = secondX + distanceX
    thirdY1 = secondY1 + distanceY
    thirdY2 = secondY1 - distanceY
    thirdY3 = secondY2 - distanceY
        
    fourthX = thirdX + distanceX
    fourthY1 = thirdY1 + distanceY
    fourthY2 = thirdY1 - distanceY
    fourthY3 = thirdY2 - distanceY
    fourthY4 = thirdY3 - distanceY
        
    fifthX = fourthX + distanceX
    fifthY1 = fourthY1 + distanceY
    fifthY2 = fourthY1 - distanceY
    fifthY3 = fourthY2 - distanceY
    fifthY4 = fourthY3 - distanceY
    fifthY5 = fourthY4 - distanceY
        
        
    # Add some distance between balls
    return  [(firstX, firstY1),
            (secondX+4, secondY1+2), (secondX+4, secondY2-2),
            (thirdX+8, thirdY1+4), (thirdX+8, thirdY2), (thirdX+8, thirdY3-4),
            (fourthX+12, fourthY1+6), (fourthX+12, fourthY2+2), \
            (fourthX+12, fourthY3-2),(fourthX+12, fourthY4-6), 
            (fifthX+16, fifthY1+8), (fifthX+16, fifthY2+4), \
            (fifthX+16, fifthY3),(fifthX+16, fifthY4-4), \
            (fifthX+16, fifthY5-8)]
            

            

# Calculate cue stick angle with white ball            
def cueAngle(xCue, yCue, whiteBallX, whiteBallY):
    xDist = xCue - whiteBallX
    yDist = yCue - whiteBallY
        
    if xDist == 0:
        if yDist >= 0:
            angle = math.pi/2
        else:
            angle = math.pi/2*3
    else:    
        absAngle = math.atan(abs(yDist/xDist))
        if yDist >= 0 and xDist <= 0:
            angle = absAngle
        elif yDist >= 0 and xDist >= 0:
            angle = math.pi - absAngle
        elif yDist <= 0 and xDist >= 0:
            angle = math.pi + absAngle
        elif yDist <= 0 and xDist <= 0:
            angle = 2*math.pi - absAngle            
    return angle

# Return list of cue starting and ending positions            
def cuePosition(angle, xCue, yCue, whiteBallX, whiteBallY, \
                distFromWhite, cueLength):
    angle = cueAngle(xCue, yCue, whiteBallX, whiteBallY)
    x1 = whiteBallX + distFromWhite*math.cos(angle)
    y1 = whiteBallY - distFromWhite*math.sin(angle)
    x2 = x1 + cueLength*math.cos(angle)
    y2 = y1 - cueLength*math.sin(angle)
    return (x1, y1, x2, y2)

 
# Return xStart and yStart of guide lines
def guideLinePosition(angle, xCue, yCue, whiteBallX, whiteBallY, distFromWhite):
    angle = cueAngle(xCue, yCue, whiteBallX, whiteBallY)
    xStart = whiteBallX - 2*distFromWhite*math.cos(angle)
    yStart = whiteBallY + 2*distFromWhite*math.sin(angle)
    return (xStart, yStart)


# Calculate hole positions    
def holePositions(outerMargin, innerMargin, boardWidth, boardHeight):
    xFirstCol = outerMargin + innerMargin - graphics.Hole.radius
    xSecondCol = boardWidth/2 + outerMargin
    xThirdCol = boardWidth + outerMargin - (innerMargin - graphics.Hole.radius)
    yFirstRow = outerMargin + innerMargin - graphics.Hole.radius
    ySecondRow = boardHeight + outerMargin - innerMargin + graphics.Hole.radius
        
    listPos = [(xFirstCol, yFirstRow), (xSecondCol, yFirstRow), \
               (xThirdCol, yFirstRow), (xFirstCol, ySecondRow), \
               (xSecondCol, ySecondRow), (xThirdCol, ySecondRow)]
               
    return listPos
    
# Return True if white ball is within bounds of the board
def boundsForWhite(margin, boardWidth, boardHeight):
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]
    upBound = margin + graphics.Border.innerMargin + ballClass.Ball.radius
    lowBound = boardHeight + margin - \
               graphics.Border.innerMargin - ballClass.Ball.radius
    leftBound = margin + graphics.Border.innerMargin + ballClass.Ball.radius
    rightBound = boardWidth + margin - \
                graphics.Border.innerMargin - ballClass.Ball.radius
    if x < rightBound and x > leftBound and y > upBound and y < lowBound:
        return True
    else:
        return False
        