import math
import ballClass
import pygame
import graphics

# Calculate distance beteween two points
def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5


# Change ball speed and direction when collided    
def collide(ball1, ball2):

    dist = distance(ball1.rect.centerx, ball1.rect.centery, \
    ball2.rect.centerx, ball2.rect.centery)


    # Diagonal speed of ball    
    ballV = (ball1.xSpeed**2+ball1.ySpeed**2)**0.5
    
    
    # When striking ball is in upper left position
    if ball1.rect.x < ball2.rect.x and ball1.rect.y < ball2.rect.y :
        triSide = ball2.rect.y - ball1.rect.y
        angle = math.acos(triSide/dist)
        strikeAngle = math.acos(ball1.xSpeed/ballV)        
        hitAngle = math.acos((ball2.rect.x - ball1.rect.x)/dist)
        
        # Compare striking angle with collision angle to 
        # determine bouncing direction
        if hitAngle > strikeAngle:
            cosAngle = math.cos(angle)
            sinAngle = math.sin(angle)
            ball1V = ball1.xSpeed*cosAngle - ball1.ySpeed*sinAngle
            ball2V = ball1.xSpeed*sinAngle + ball1.ySpeed*cosAngle
            ball1.xSpeed = ball1V*cosAngle
            ball1.ySpeed = -ball1V*sinAngle
            ball2.xSpeed = ball2V*sinAngle
            ball2.ySpeed = ball2V*cosAngle
            
        if hitAngle < strikeAngle:
            cosAngle = math.cos(angle)
            sinAngle = math.sin(angle)
            ball1V = ball1.ySpeed*sinAngle - ball1.xSpeed*cosAngle
            ball2V = ball1.xSpeed*sinAngle + ball1.ySpeed*cosAngle
            ball1.xSpeed = -ball1V*cosAngle
            ball1.ySpeed = ball1V*sinAngle
            ball2.xSpeed = ball2V*sinAngle
            ball2.ySpeed = ball2V*cosAngle
        
        # If two balls collide head on, add some speed to first ball so 
        # ball doesn't completely stop
        if hitAngle == strikeAngle:
            ball2.xSpeed = ballV*math.cos(hitAngle)
            ball2.ySpeed = ballV*math.sin(hitAngle)
            ball1.xSpeed = ballV*math.cos(hitAngle)*1/5
            ball1.xSpeed = ballV*math.sin(hitAngle)*1/5
            
            
        
    # When striking ball is in lower left position
    elif ball1.rect.x < ball2.rect.x and ball1.rect.y > ball2.rect.y:
        triSide = ball1.rect.y - ball2.rect.y
        angle = math.acos(triSide/dist)
        ballV = (ball1.xSpeed**2 + ball1.ySpeed**2)**0.5
        strikeAngle = math.acos(ball1.xSpeed/ballV)
        hitAngle = math.acos((ball2.rect.x - ball1.rect.x)/dist) 
        
        if hitAngle > strikeAngle:
            cosAngle = math.cos(angle)
            sinAngle = math.sin(angle)
            ball1V = ball1.ySpeed*cosAngle + ball1.xSpeed*sinAngle
            ball2V = ball1.xSpeed*cosAngle - ball1.ySpeed*sinAngle
            ball1.xSpeed = ball1V*sinAngle
            ball1.ySpeed = ball1V*cosAngle
            ball2.xSpeed = ball2V*cosAngle
            ball2.ySpeed = -ball2V*sinAngle
            
        if hitAngle < strikeAngle:
            cosAngle = math.cos(angle)
            sinAngle = math.sin(angle)
            ball1V = -ball1.ySpeed*cosAngle - ball1.xSpeed*sinAngle
            ball2V = ball1.xSpeed*cosAngle - ball1.ySpeed*sinAngle
            ball1.xSpeed = -ball1V*sinAngle
            ball1.ySpeed = -ball1V*cosAngle
            ball2.xSpeed = ball2V*cosAngle
            ball2.ySpeed = -ball2V*sinAngle
            
        if hitAngle == strikeAngle:
            ball2.xSpeed = ballV*math.cos(hitAngle)
            ball2.ySpeed = -ballV*math.sin(hitAngle)
            ball1.xSpeed = ballV*math.cos(hitAngle)*1/5
            ball1.xSpeed = -ballV*math.sin(hitAngle)*1/5
            
        
            
    # When striking ball is in lower right position    
    elif ball1.rect.x > ball2.rect.x and ball1.rect.y > ball2.rect.y:
        triSide = ball1.rect.y - ball2.rect.y
        angle = math.acos(triSide/dist)
        ballV = (ball1.xSpeed**2 + ball1.ySpeed**2)**0.5
        strikeAngle = math.acos(-ball1.xSpeed/ballV)
        hitAngle = math.acos((ball2.rect.x - ball1.rect.x)/dist)
        
        if hitAngle < strikeAngle:
            cosAngle = math.cos(angle)
            sinAngle = math.sin(angle)
            ball1V = ball1.ySpeed*sinAngle - ball1.xSpeed*cosAngle
            ball2V = -ball1.xSpeed*sinAngle - ball1.ySpeed*cosAngle
            ball1.xSpeed = -ball1V*cosAngle
            ball1.ySpeed = ball1V*sinAngle
            ball2.xSpeed = -ball2V*sinAngle
            ball2.ySpeed = -ball2V*cosAngle
            
        if hitAngle > strikeAngle:
            cosAngle = math.cos(angle)
            sinAngle = math.sin(angle)
            ball1V = ball1.xSpeed*sinAngle - ball1.ySpeed*cosAngle
            ball2V = -ball1.xSpeed*cosAngle - ball1.ySpeed*sinAngle
            ball1.xSpeed = -ball1V*cosAngle
            ball1.ySpeed = ball1V*sinAngle
            ball2.xSpeed = -ball2V*sinAngle
            ball2.ySpeed = -ball2V*cosAngle
            
        if hitAngle == strikeAngle:
            ball2.xSpeed = -ballV*math.cos(hitAngle)
            ball2.ySpeed = -ballV*math.sin(hitAngle)
            ball1.xSpeed = -ballV*math.cos(hitAngle)*1/5
            ball1.ySpeed = -ballV*math.sin(hitAngle)*1/5

    
   
    # When striking ball is in upper right position    
    elif ball1.rect.x > ball2.rect.x and ball1.rect.y < ball2.rect.y:
        triSide = ball2.rect.y - ball1.rect.y
        angle = math.acos(triSide/dist)
        ballV = (ball1.xSpeed**2 + ball1.ySpeed**2)**0.5
        strikeAngle = math.acos(-ball1.xSpeed/ballV)
        hitAngle = math.acos((ball2.rect.x - ball1.rect.x)/dist)
        
        if hitAngle < strikeAngle:
            cosAngle = math.cos(angle)
            sinAngle = math.sin(angle)
            ball1V = -ball1.ySpeed*sinAngle - ball1.xSpeed*cosAngle
            ball2V = ball1.xSpeed*sinAngle - ball1.ySpeed*cosAngle
            ball1.xSpeed = -ball1V*cosAngle
            ball1.ySpeed = -ball1V*sinAngle
            ball2.xSpeed = -ball2V*sinAngle
            ball2.ySpeed = ball2V*cosAngle
            
            
        if hitAngle > strikeAngle:
            cosAngle = math.cos(angle)
            sinAngle = math.sin(angle)
            ball1V = -ball1.ySpeed*sinAngle - ball1.xSpeed*cosAngle
            ball2V = ball1.ySpeed*cosAngle - ball1.xSpeed*sinAngle
            ball1.xSpeed = -ball1V*cosAngle
            ball1.ySpeed = -ball1V*sinAngle
            ball2.xSpeed = -ball2V*sinAngle
            ball2.ySpeed = ball2V*cosAngle
            
        if hitAngle == strikeAngle:
            ball2.xSpeed = -ballV*math.cos(hitAngle)
            ball2.ySpeed = ballV*math.sin(hitAngle)
            ball1.xSpeed = -ballV*math.cos(hitAngle)*1/5
            ball1.ySpeed = ballV*math.sin(hitAngle)*1/5
    
    
    
    # If two colliding balls are in same x or y level        
    elif ball1.rect.x == ball2.rect.x or ball1.rect.y == ball2.rect.y:
        ballV = (ball1.xSpeed**2 + ball1.ySpeed**2)**0.5
        ball1.ySpeed, ball2.xSpeed = ball1.ySpeed, ball1.xSpeed
        ball1.xSpeed, ball2.ySpeed = 0, 0
        

# Change speed and direction when ball touches borders        
def collideBorder(ball, margin, boardHeight, boardWidth):
    if type(ball) != pygame.sprite.Group:
        listRange = borderCheck(ball, margin, boardHeight, boardWidth)
        if listRange[1] == False:
            ball.ySpeed = -ball.ySpeed
        if listRange[0] == False:
            ball.xSpeed = -ball.xSpeed
        elif False in listRange[2:]:
            collideAngle(ball)
            
# Change ball speed and angle when it collides with 45 degree borders
def collideAngle(ball):       
    if ball.xSpeed * ball.ySpeed > 0:
        ball.xSpeed, ball.ySpeed = ball.ySpeed, ball.xSpeed
    else:
        ball.xSpeed, ball.ySpeed = -ball.ySpeed, -ball.xSpeed
        

# Calculate the perpendicular distance of the ball radius to a line function
def distPointLine(a, b, c, x, y):
    return abs((a*x + b*y + c)) / (math.sqrt(a**2 + b**2)) 

# Equation of upper left 45 degree sloped border ax + by + c = 0
def checkDistance1(margin, distCorner, inMargin):
    a = 1
    b = -1
    c = inMargin - distCorner
    return [a, b, c]

# Equation of upper left 45 degree sloped border ax + by + c = 0    
def checkDistance2(margin, distCorner, inMargin):
    a = 1
    b = -1
    c = distCorner - inMargin
    return [a, b, c]

# Equation of upper middle 45 degree sloped border ax + by + c = 0     
def checkDistance3(margin, inMargin, holeR, boardWidth):
    a = -1
    b = -1
    c = 2*margin + boardWidth/2 - holeR + inMargin
    return [a, b, c]
     
# Equation of upper middle 45 degree sloped border ax + by + c = 0  
def checkDistance4(margin, inMargin, holeR, boardWidth):
    a = 1
    b = -1
    c = inMargin - boardWidth/2 - holeR
    return [a, b, c]

# Equation of upper right 45 degree sloped border ax + by + c = 0      
def checkDistance5(margin, inMargin, boardWidth, distCorner):
    a = -1
    b = -1
    c = 2*margin + inMargin + boardWidth - distCorner
    return [a, b, c]

# Equation of upper right 45 degree sloped border ax + by + c = 0      
def checkDistance6(margin, inMargin, boardWidth, distCorner):
    a = -1
    b = -1
    c = 2*margin + distCorner - inMargin + boardWidth
    return [a, b, c]
 
# Equation of lower right 45 degree sloped border ax + by + c = 0     
def checkDistance7(margin, boardHeight, boardWidth, inMargin, distCorner):
    a = -1
    b = -1
    c = boardHeight - boardWidth + inMargin - distCorner
    return [a, b, c]
    
# Equation of lower right 45 degree sloped border ax + by + c = 0 
def checkDistance8(margin, boardHeight, boardWidth, inMargin, distCorner):
    a = -1
    b = -1
    c = boardHeight - boardWidth - inMargin + distCorner
    return [a, b, c]

# Equation of lower middle 45 degree sloped border ax + by + c = 0 
def checkDistance9(margin, boardHeight, boardWidth, inMargin, holeR):
    a = -1
    b = -1
    c = boardHeight + 2*margin - inMargin + holeR + boardWidth/2
    return [a, b, c]

# Equation of lower middle 45 degree sloped border ax + by + c = 0   
def checkDistance10(margin, boardHeight, boardWidth, inMargin, holeR):
    a = 1
    b = -1
    c = boardHeight - inMargin + holeR - boardWidth/2
    return [a, b, c]
 
# Equation of lower left 45 degree sloped border ax + by + c = 0     
def checkDistance11(margin, boardHeight, inMargin, distCorner):
    a = -1
    b = -1
    c = boardHeight + 2*margin - inMargin + distCorner
    return [a, b, c]

# Equation of lower 45 degree sloped border ax + by + c = 0    
def checkDistance12(margin, boardHeight, inMargin, distCorner):
    a = 1
    b = -1
    c = boardHeight + 2*margin + inMargin - distCorner
    return [a, b, c]
    
    
# Check (x, y) of ball to see if it will bounce off a nomral or sloped border
def regBorderCheck(ball, margin, boardHeight, boardWidth):
    # import values from other files and classes
    innnerMarign = graphics.Border.innerMargin
    distCorner = graphics.Border.distToCornerSide
    extend = graphics.Border.extend
    extendX = graphics.Border.extend*math.cos(math.pi/4)
    holeR = graphics.Hole.radius
    x = ball.rect.centerx
    y = ball.rect.centery
    
    # radius bounds for normal collision with table
    if (x >= boardWidth/2 + margin + holeR and \
    x <= boardWidth + margin - distCorner) \
    or (x <= boardWidth/2 + margin - holeR and x >= margin + distCorner) or \
    (x <= margin + distCorner and y <= boardHeight + margin - distCorner and \
    y >= margin + distCorner) or \
    (x >= boardWidth + margin - distCorner and\
    y <= boardHeight + margin - distCorner and y >= margin + distCorner):
        return True    
    else:
        return False


# Return list of bool values to check which border side the ball collides to      
def borderCheck(ball, margin, boardHeight, boardWidth):
    # import values from other files and classes
    innerMargin = graphics.Border.innerMargin
    distCorner = graphics.Border.distToCornerSide
    extend = graphics.Border.extend
    extendX = graphics.Border.extend*math.cos(math.pi/4)
    holeR = graphics.Hole.radius
    x = ball.rect.centerx
    y = ball.rect.centery
    
    # Make sure ball is not sprite type
    if type(ball) != pygame.sprite.Group:
        
        # List to determine which side the border side collides to
        listRange = [True] * 14
        
        # If True, then the ball collides into the normal borders of the board
        if regBorderCheck(ball, margin, boardHeight, boardWidth):
            if ball.rect.y <= margin + innerMargin or ball.rect.y >= \
            boardHeight - innerMargin + margin - 2*ball.radius:                 
                listRange[1] = False    # Collides to up/bottom border
            elif ball.rect.x <= margin + innerMargin or \
            ball.rect.x >= boardWidth+margin-innerMargin-2*ball.radius:
                listRange[0] = False    # Collides to left/right border

        # Ball colides to a sloped border
        else:
            # Upper left sloped borders
            if x < margin + distCorner and y < margin + distCorner:
                # Check the distance of the ball center to the border line
                pos = checkDistance1(margin, distCorner, innerMargin)
                pos2 = checkDistance2(margin, distCorner, innerMargin)
                # Collides
                if distPointLine(pos[0], pos[1], pos[2], x, y) <= ball.radius:
                    listRange[2] = False
                elif distPointLine(pos2[0], pos2[1],pos2[2], x, y) \
                <= ball.radius:
                    listRange[3] = False
             
            # Upper middle sloped borders
            elif x < boardWidth/2 + margin + holeR and \
                 x > boardWidth/2 + margin - holeR and y < boardHeight/2:
                pos = checkDistance3(margin, innerMargin, holeR, boardWidth)
                pos2 = checkDistance4(margin, innerMargin, holeR, boardWidth)
                if distPointLine(pos[0], pos[1], pos[2], x, y) <= ball.radius:
                    listRange[4] = False
                elif distPointLine(pos2[0], pos2[1],pos2[2], x, y) \
                    <= ball.radius:
                    listRange[5] = False
            
            # Upper right sloped borders        
            elif x > boardWidth + margin - distCorner and \
                 y < margin + distCorner:
                pos = checkDistance5(margin, innerMargin, \
                                     boardWidth, distCorner)
                pos2 = checkDistance6(margin, innerMargin, \
                                      boardWidth, distCorner)
                if distPointLine(pos[0], pos[1], pos[2], x, y) <= ball.radius:
                    listRange[6] = False
                elif distPointLine(pos2[0], pos2[1],pos2[2], x, y) \
                    <= ball.radius:
                    listRange[7] = False
            
            # Lower left sloped borders        
            elif x > margin + distCorner and \
            y > boardHeight + margin - distCorner:
                pos = checkDistance7(margin, boardHeight,\
                boardWidth, innerMargin, distCorner)
                pos2 = checkDistance8(margin, boardHeight,\
                boardWidth, innerMargin, distCorner)
                if distPointLine(pos[0], pos[1], pos[2], x, y) \
                    <= ball.radius:
                    listRange[8] = False
                elif distPointLine(pos2[0], pos2[1],pos2[2], x, y) \
                    <= ball.radius:
                    listRange[9] = False
             
            # Lower middle sloped borders
            elif x < boardWidth/2 + margin + holeR and \
                 x > boardWidth/2 + margin - holeR and y > boardHeight/2:
                pos = checkDistance9(margin, boardHeight,\
                boardWidth, innerMargin, holeR)
                pos2 = checkDistance10(margin, boardHeight,\
                boardWidth, innerMargin, holeR)
                if distPointLine(pos[0], pos[1], pos[2], x, y) \
                    <= ball.radius:
                    listRange[8] = False
                elif distPointLine(pos2[0], pos2[1],pos2[2], x, y) \
                    <= ball.radius:
                    listRange[9] = False
             
            # Lower left sloped borders
            elif x < margin + distCorner and \
            y > boardHeight + margin - distCorner:
                pos = checkDistance11(margin, boardHeight,\
                innerMargin, distCorner)
                pos2 = checkDistance12(margin, boardHeight,\
                innerMargin, distCorner)
                if distPointLine(pos[0], pos[1], pos[2], x, y)\
                    <= ball.radius:
                    listRange[12] = False
                elif distPointLine(pos2[0], pos2[1],pos2[2], x, y) \
                    <= ball.radius:
                    listRange[13] = False

        # Return list of bool values to determine whether collision has occured
        # And if so, which side
        return listRange
                
    

# Function to ensure ball doesn't go out of bounds right after collision call    
def adjustBorderCollision(ball, oldX, oldY, margin, boardHeight, boardWidth):
    # Values from other files and classes
    innerMargin = graphics.Border.innerMargin
    distCorner = graphics.Border.distToCornerSide
    holeR = graphics.Hole.radius
    x = ball.rect.centerx
    y = ball.rect.centery
    
    # List containing collision state information
    listRange = borderCheck(ball, margin, boardHeight, boardWidth)
    
    # Collides with top/bottom normal borders
    if listRange[0] == False:
        if ball.rect.x <= margin + innerMargin:
           ball.rect.x = margin + innerMargin
        elif ball.rect.x >= boardWidth+margin-innerMargin-2*ball.radius:
            ball.rect.x = boardWidth+margin-innerMargin-2*ball.radius
    
    # Collides with left/right normal borders        
    elif listRange[1] == False:
        if ball.rect.y <= margin + innerMargin:
            ball.rect.y = margin + innerMargin
        elif ball.rect.y >= boardHeight+margin-innerMargin-2*ball.radius:
            ball.rect.y = boardHeight+margin-innerMargin-2*ball.radius
    
    # Collides with upper left sloped borders        
    elif listRange[2] == False:
        pos = checkDistance1(margin, distCorner, innerMargin)
        dist = distPointLine(pos[0], pos[1], pos[2], x, y)
        if dist <= ball.radius:
            ball.rect.x -= (ball.radius - dist)*math.cos(math.pi/4)
            ball.rect.y += (ball.radius - dist)* math.cos(math.pi/4)
   
    
    elif listRange[3] == False:
        pos = checkDistance2(margin, distCorner, innerMargin)
        dist = distPointLine(pos[0], pos[1], pos[2], x, y)
        if dist <= ball.radius:
            ball.rect.x += (ball.radius - dist)*math.cos(math.pi/4)
            ball.rect.y -= (ball.radius - dist)* math.cos(math.pi/4)
    
    # Collides with upper middle sloped borders
    elif listRange[4] == False:
        pos = checkDistance3(margin, innerMargin, holeR, boardWidth)
        dist = distPointLine(pos[0], pos[1], pos[2], x, y)
        if dist <= ball.radius:
            ball.rect.x += (ball.radius - dist)*math.cos(math.pi/4)
            ball.rect.y += (ball.radius - dist)* math.cos(math.pi/4)
    
           
    elif listRange[5] == False:
        pos = checkDistance4(margin, innerMargin, holeR, boardWidth)
        dist = distPointLine(pos[0], pos[1], pos[2], x, y)
        if dist <= ball.radius:
            ball.rect.x -= (ball.radius - dist)*math.cos(math.pi/4)
            ball.rect.y += (ball.radius - dist)* math.cos(math.pi/4)
    
   # Collides with upper right sloped borders
    elif listRange[6] == False:
        pos = checkDistance5(margin, innerMargin, boardWidth, distCorner)
        dist = distPointLine(pos[0], pos[1], pos[2], x, y)
        if dist <= ball.radius:
            ball.rect.x += (ball.radius - dist)*math.cos(math.pi/4)
            ball.rect.y += (ball.radius - dist)* math.cos(math.pi/4)
    
    elif listRange[7] == False:
        pos = checkDistance6(margin, innerMargin, boardWidth, distCorner)
        dist = distPointLine(pos[0], pos[1], pos[2], x, y)
        if dist <= ball.radius:
            ball.rect.x -= (ball.radius - dist)*math.cos(math.pi/4)
            ball.rect.y -= (ball.radius - dist)* math.cos(math.pi/4)
    
     # Collides with lower right sloped borders                
    elif listRange[8] == False:
        pos = checkDistance7(margin, boardHeight,\
              boardWidth, innerMargin, distCorner)
        dist = distPointLine(pos[0], pos[1], pos[2], x, y)
        if dist <= ball.radius:
            ball.rect.x -= (ball.radius - dist)*math.cos(math.pi/4)
            ball.rect.y += (ball.radius - dist)* math.cos(math.pi/4)
            
    elif listRange[9] == False:
        pos = checkDistance8(margin, boardHeight,\
              boardWidth, innerMargin, distCorner)
        dist = distPointLine(pos[0], pos[1], pos[2], x, y)
        if dist <= ball.radius:
            ball.rect.x += (ball.radius - dist)*math.cos(math.pi/4)
            ball.rect.y -= (ball.radius - dist)* math.cos(math.pi/4)
    
    # Collides with lower middle sloped borders
    elif listRange[10] == False:
        pos = checkDistance9(margin, boardHeight,\
              boardWidth, innerMargin, holeR)
        dist = distPointLine(pos[0], pos[1], pos[2], x, y)
        if dist <= ball.radius:
            ball.rect.x -= (ball.radius - dist)*math.cos(math.pi/4)
            ball.rect.y -= (ball.radius - dist)* math.cos(math.pi/4)
            
    elif listRange[11] == False:
        pos = checkDistance10(margin, boardHeight,\
              boardWidth, innerMargin, holeR)
        dist = distPointLine(pos[0], pos[1], pos[2], x, y)
        if dist <= ball.radius:
            ball.rect.x += (ball.radius - dist)*math.cos(math.pi/4)
            ball.rect.y -= (ball.radius - dist)* math.cos(math.pi/4)
    
    # Collides with lower left sloped borders          
    elif listRange[12] == False:
        pos = checkDistance11(margin, boardHeight, innerMargin, distCorner)
        dist = distPointLine(pos[0], pos[1], pos[2], x, y)
        if dist <= ball.radius:
            ball.rect.x -= (ball.radius - dist)*math.cos(math.pi/4)
            ball.rect.y -= (ball.radius - dist)* math.cos(math.pi/4)
            
    elif listRange[13] == False:
        pos = checkDistance12(margin, boardHeight, innerMargin, distCorner)
        dist = distPointLine(pos[0], pos[1], pos[2], x, y)
        if dist <= ball.radius:
            ball.rect.x += (ball.radius - dist)*math.cos(math.pi/4)
            ball.rect.y -= (ball.radius - dist)* math.cos(math.pi/4)

        



# Function to ensure two balls don't overlap right after collision call            
def adjustCollision(ball1, ball2, oldX, oldY):
    innerMargin = graphics.Border.innerMargin
    distCorner = graphics.Border.distToCornerSide
    
    dist = distance(ball1.rect.x, ball1.rect.y, ball2.rect.x, ball2.rect.y)
    triSide = abs(ball2.rect.x - ball1.rect.x)
    if dist != 0:
        angle = math.acos(triSide/dist)
        xDiff = abs(ball1.radius*2*math.cos(angle) - dist*math.cos(angle))
        yDiff = abs(ball1.radius*2*math.sin(angle) - dist*math.cos(angle))
        
        if oldX <= ball2.rect.x and oldY <= ball2.rect.y:
            ball1.rect.x -= xDiff
            ball1.rect.y -= yDiff
            
        elif oldX <= ball2.rect.x and oldY >= ball2.rect.y:
            ball1.rect.x -= xDiff
            ball1.rect.y += yDiff
            
        elif oldX >= ball2.rect.x and oldY >= ball2.rect.y:
            ball1.rect.x += xDiff
            ball1.rect.y += yDiff
            
        elif oldX >= ball2.rect.x and oldY <= ball2.rect.y:
            ball1.rect.x += xDiff
            ball1.rect.y -= yDiff
        
        
    
             