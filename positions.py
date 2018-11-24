import graphics
import math

# Calculate positions of initial colored balls    
def ballStartPositions(width, margin, height):     
    r = 15
    d = 2*r
    distanceX = d*math.cos(math.pi/6)
    distanceY = d*math.sin(math.pi/6)
    
    firstX = (width-2*margin)/3*2 + margin
    firstY1 = height/2
    
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
    return [(firstX, firstY1),
            (secondX+4, secondY1+4), (secondX+4, secondY2-4),
            (thirdX+8, thirdY1+8), (thirdX+8, thirdY2), (thirdX+8, thirdY3-8),
            (fourthX+12, fourthY1+12), (fourthX+12, fourthY2+8), \
            (fourthX+12, fourthY3-8),(fourthX+12, fourthY4-12), 
            (fifthX+16, fifthY1+16), (fifthX+16, fifthY2+8), \
            (fifthX+16, fifthY3),(fifthX+16, fifthY4-8), \
            (fifthX+16, fifthY5-16)]
            

            

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
    
    
    
    
    
    
    

    
    
    
