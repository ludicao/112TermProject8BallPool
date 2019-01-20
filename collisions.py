#############################
# This file handles all of the physics functions of the game, including border
# collision on both straight and sloper sides, ball collisions, cue and white
# ball collision, friction between gameboard and balls, as wel as calculating 
# angles, detecting, and drawing guide lines connecting balls to holes. I 
# noticed that the internal pygame.sprite.collision functions in the pygame 
# library aren't really efficient. There's sometimes a lag between when the 
# actually collide and pygame.sprite.collision detecting a collision. Therefore,
# without further adjustments, the balls would very much likely overlap with
# each other, especially when multiple balls are moving and colliding at 
# the same time. Therefore, I added various additional functions to prevent 
# overlapping of sprite ball groups.
#############################


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
        strikeAngle = math.acos(abs(ball1.xSpeed)/ballV)
        hitAngle = math.acos((ball2.rect.x - ball1.rect.x)/dist)
        
        if ball1.xSpeed > 0 and ball1.ySpeed < 0:
            cosAngle = math.cos(angle)
            sinAngle = math.sin(angle)
            ball2V = -ball1.xSpeed*sinAngle - ball1.ySpeed*cosAngle
            ball1V = ball1.xSpeed*cosAngle - ball1.ySpeed*sinAngle
            ball1.xSpeed = ball1V*cosAngle
            ball1.ySpeed = -ball1V*sinAngle
            ball2.xSpeed = -ball2V*sinAngle
            ball2.ySpeed = -ball2V*cosAngle 
        
        else:
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
                if ball1.xSpeed > 0 and ball1.ySpeed < 0:
                    cosAngle = math.cos(angle)
                    sinAngle = math.sin(angle)
                    ball1V = ball1.xSpeed*sinAngle - ball1.ySpeed*cosAngle
                    ball2V = -ball1.xSpeed*cosAngle - ball1.ySpeed*sinAngle
                    ball1.xSpeed = -ball1V*cosAngle
                    ball1.ySpeed = ball1V*sinAngle
                    ball2.xSpeed = -ball2V*sinAngle
                    ball2.ySpeed = -ball2V*cosAngle
                elif ball1.xSpeed < 0 and ball1.ySpeed > 0:
                    cosAngle = math.cos(angle)
                    sinAngle = math.sin(angle)
                    ball1V = ball1.ySpeed*sinAngle - ball1.xSpeed*cosAngle
                    ball2V = -ball1.ySpeed*cosAngle - ball1.xSpeed*sinAngle
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
        
        if ball1.xSpeed > 0 and ball1.ySpeed > 0:
            cosAngle = math.cos(angle)
            sinAngle = math.sin(angle)
            ball1V = ball1.ySpeed*sinAngle + ball1.xSpeed*cosAngle
            ball2V = ball1.ySpeed*cosAngle - ball1.xSpeed*sinAngle
            ball1.xSpeed = ball1V*cosAngle
            ball1.ySpeed = ball1V*sinAngle
            ball2.xSpeed = -ball2V*sinAngle
            ball2.ySpeed = ball2V*cosAngle
            
        else:
            
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
        if False in listRange[2:]:
            collideAngle(ball, listRange)
        elif listRange[1] == False:
            ball.ySpeed = -ball.ySpeed
        elif listRange[0] == False:
            ball.xSpeed = -ball.xSpeed
            
# Change ball speed and angle when it collides with 45 degree borders
def collideAngle(ball, listRange):   
    if ball.xSpeed * ball.ySpeed > 0:
        # These are borders which slope toward the upper right direction
        if listRange[4] == False or listRange[10] == False or \
        listRange[6] == False or listRange[7] == False or \
        listRange[12] == False or listRange[13] == False:
            ball.xSpeed, ball.ySpeed = -ball.ySpeed, -ball.xSpeed
        # Borders that slope toward the upper left direction
        else:
            ball.xSpeed, ball.ySpeed = ball.ySpeed, ball.xSpeed
    else:
        xOriginal = ball.xSpeed
        if ball.xSpeed > 0:
            ball.xSpeed = -abs(ball.ySpeed)
        else:
            ball.xSpeed = abs(ball.ySpeed)
        if ball.ySpeed > 0:
            ball.ySpeed = -abs(xOriginal)
        else:
            ball.ySpeed = abs(xOriginal)

        

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
    c = 2*margin + boardWidth/2 - 2*holeR + inMargin
    return [a, b, c]
     
# Equation of upper middle 45 degree sloped border ax + by + c = 0  
def checkDistance4(margin, inMargin, holeR, boardWidth):
    a = 1
    b = -1
    c = inMargin - boardWidth/2 - 2*holeR
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
    a = 1
    b = -1
    c = boardHeight - boardWidth + inMargin - distCorner
    return [a, b, c]
    
# Equation of lower right 45 degree sloped border ax + by + c = 0 
def checkDistance8(margin, boardHeight, boardWidth, inMargin, distCorner):
    a = 1
    b = -1
    c = boardHeight - boardWidth - inMargin + distCorner
    return [a, b, c]

# Equation of lower middle 45 degree sloped border ax + by + c = 0 
def checkDistance9(margin, boardHeight, boardWidth, inMargin, holeR):
    a = -1
    b = -1
    c = boardHeight + 2*margin - inMargin + 2*holeR + boardWidth/2
    return [a, b, c]

# Equation of lower middle 45 degree sloped border ax + by + c = 0   
def checkDistance10(margin, boardHeight, boardWidth, inMargin, holeR):
    a = 1
    b = -1
    c = boardHeight - inMargin + 2*holeR - boardWidth/2
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
    if (x >= boardWidth/2 + margin + holeR + extendX and \
    x <= boardWidth + margin - distCorner) \
    or (x <= boardWidth/2 + margin - holeR - extendX and x >= \
    margin + distCorner) or (x <= margin + distCorner and \
    y <= boardHeight + margin - distCorner and y >= margin + distCorner) or \
    (x >= boardWidth + margin - distCorner and \
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
            elif x < boardWidth/2 + margin + holeR + extendX and \
                 x > boardWidth/2 + margin - holeR - extendX and \
                 y < boardHeight/2:
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
            
            # Lower right sloped borders        
            elif x > margin + boardWidth - distCorner and \
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
            elif x < boardWidth/2 + margin + holeR + extendX and \
                 x > boardWidth/2 + margin - holeR - extendX \
                 and y > boardHeight/2:
                pos = checkDistance9(margin, boardHeight,\
                boardWidth, innerMargin, holeR)
                pos2 = checkDistance10(margin, boardHeight,\
                boardWidth, innerMargin, holeR)
                if distPointLine(pos[0], pos[1], pos[2], x, y) \
                    <= ball.radius:
                    listRange[10] = False
                elif distPointLine(pos2[0], pos2[1],pos2[2], x, y) \
                    <= ball.radius:
                    listRange[11] = False
             
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
    extendX = graphics.Border.extend*math.cos(math.pi/4)
    
    # List containing collision state information
    listRange = borderCheck(ball, margin, boardHeight, boardWidth)
    
    # Collides with left/right normal borders
    if listRange[0] == False:
        if ball.rect.x <= margin + innerMargin:
           ball.rect.x = margin + innerMargin
        elif ball.rect.x >= boardWidth+margin-innerMargin-2*ball.radius:
            ball.rect.x = boardWidth+margin-innerMargin-2*ball.radius
    
    # Collides with top/bottom normal borders        
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
    
    dist = distance(ball1.rect.centerx, ball1.rect.centery, \
    ball2.rect.centerx, ball2.rect.centery)
    triSide = abs(ball2.rect.centerx - ball1.rect.centerx)
    if dist != 0:
        angle = math.acos(triSide/dist)
        xDiff = abs(ball1.radius*2*math.cos(angle) - dist*math.cos(angle))
        yDiff = abs(ball1.radius*2*math.sin(angle) - dist*math.cos(angle))
        
        # Striking ball previously in upper left position
        if oldX <= ball2.rect.centerx and oldY <= ball2.rect.centery:
            
            ball2.rect.centerx += xDiff
            ball2.rect.centery += yDiff 
            if abs(ball1.xSpeed) >= 0.001 or abs(ball1.ySpeed) >= 0.001:
                collide(ball1, ball2)
        
        # Striking ball previously in lower left position           
        elif oldX <= ball2.rect.centerx and oldY >= ball2.rect.centery:
            ball2.rect.centerx += xDiff
            ball2.rect.centery -= yDiff        
            if abs(ball1.xSpeed) >= 0.001 or abs(ball1.ySpeed) >= 0.001:
                collide(ball1, ball2)
                ball2.hasCollided = True
        
        # Striking ball previously in upper right position        
        elif oldX >= ball2.rect.centerx and oldY >= ball2.rect.centery:
            ball2.rect.centerx -= xDiff
            ball2.rect.centery -= yDiff 
            if abs(ball1.xSpeed) >= 0.001 or abs(ball1.ySpeed) >= 0.001:
                collide(ball1, ball2)
                ball2.hasCollided = True
        
        # Strking ball previously in lower right position    
        elif oldX >= ball2.rect.centerx and oldY <= ball2.rect.centery:
            ball2.rect.centerx -= xDiff 
            ball2.rect.centery += yDiff 
            if abs(ball1.xSpeed) >= 0.001 or abs(ball1.ySpeed) >= 0.001:
                collide(ball1, ball2)
                ball2.hasCollided = True

# Check whether two balls have collided when speed is too fast to be detected
# by pygame.sprite.collide
def detectFast(ball1, ball2, oldX, oldY):
    yUp = ball2.rect.y - ball2.radius
    yDown = ball2.rect.y + 3*ball2.radius
    xLeft = ball2.rect.x
    xRight = ball2.rect.x + 2*ball2.radius   
    
    if oldX < ball2.rect.centerx and ball1.rect.centerx > ball2.rect.centerx \
    and oldY < yDown and oldY > yUp:
        return True
        
    if oldX > ball2.rect.centerx and ball1.rect.centerx < ball2.rect.centerx \
    and oldY < yDown and oldY > yUp:
        return True
        
    if oldY < ball2.rect.centery and ball1.rect.centery > ball2.rect.centery \
    and oldX < xRight and oldX > xLeft:
        return True
        
    if oldY > ball2.rect.centery and ball1.rect.centery < ball2.rect.centery \
    and oldX < xRight and oldX > xLeft:
        return True
        
    
        
# Return a, b, c values of line connecting two balls
def ballLine(x1, y1, x2, y2):
    if x2-x1 != 0:
        a = (y2-y1)/(x2-x1)
        c = y1 - a*x1
        b = -1
        return ([a, b, c])

# Return connecting points of white ball, colliding ball, and goal hole   
def whiteAndBall(xWhite, yWhite, ballGroup, holeGroup, xBall, yBall, \
bw, margin, bh):
    listValid = connectPoint(holeGroup, xBall, yBall, ballGroup, bw, \
    margin, bh)
    listPoints = []
    
    # Check whether white ball would collide into other balls when heading 
    # toward collision point
    for i in range(len(listValid)):
        ballIntersect = False
        if ballLine(xWhite, yWhite, listValid[i][0], listValid[i][1]) == None:
            ballIntersect = True
        else:
            a = ballLine(xWhite, yWhite, listValid[i][0], listValid[i][1])[0]
            b = ballLine(xWhite, yWhite, listValid[i][0], listValid[i][1])[1]
            c = ballLine(xWhite, yWhite, listValid[i][0], listValid[i][1])[2]
            for ball in ballGroup:
                x = ball.rect.centerx
                y = ball.rect.centery
                # Make sure balls don't iterate through themselves
                if x != xBall and y != yBall and ball.color != (255, 255, 255):
                    # Only check distance for line segments
                    if (x > min(xWhite, xBall) and x < max(xWhite, xBall)) or \
                    (y > min(yWhite, yBall) and y < max(yWhite, yBall)):
                        if distPointLine(a, b, c, x, y) < 2*ball.radius:
                            ballIntersect = True
        
        # Make sure white ball doesn't collide with ball before hitting the
        # colliding point                
        if (xBall < max(xWhite, listValid[i][0]) and xBall > min(xWhite, \
        listValid[i][0])) or (yBall < max(yWhite, listValid[i][1]) and yBall > \
        min(listValid[i][1], yWhite)):
            if (distPointLine(a, b, c, xBall, yBall)) >= \
            2*ballClass.Ball.radius and not ballIntersect:
                listPoints += [[xWhite, yWhite, listValid[i][0], \
                listValid[i][1], listValid[i][2], listValid[i][3]]]
        elif not ballIntersect:
            listPoints += [[xWhite, yWhite, listValid[i][0], \
            listValid[i][1], listValid[i][2], listValid[i][3]]]
             
    return listPoints

# Return coordinate points of center of white ball when it collides with ball        
def connectPoint(holeGroup, xBall, yBall, ballGroup, bw, margin, bh):
    r = ballClass.Ball.radius
    listValid = ballAndHole(holeGroup, xBall, yBall, ballGroup, bw, margin)
    innerMargin = graphics.Border.innerMargin
    validPoints = []
    for i in range(len(listValid)):
        xDist = abs(listValid[i][0] - xBall)
        yDist = abs(listValid[i][1] - yBall)
        if xDist != 0:
            angle = math.atan(yDist/xDist)
        else:
            continue
        if xBall > listValid[i][0]:
            xpoint = xBall + 2*r*math.cos(angle)
        else:
            xpoint = xBall - 2*r*math.cos(angle)
            
        if yBall > listValid[i][1]:
            ypoint = yBall + 2*r*math.sin(angle)
        else:
            ypoint = yBall - 2*r*math.sin(angle)
        
        # Make sure colliding point is not out of game board bounds    
        if xpoint > margin + innerMargin + r and xpoint +r < margin + bw - \
        innerMargin and ypoint > margin + innerMargin + r and ypoint  + r \
        < margin + bh - innerMargin:
            validPoints += [[xpoint, ypoint, listValid[i][0], listValid[i][1]]]

    return validPoints
            
    
        

# Return list of hole coordinates that connect ball without intersecting with
# other balls        
def ballAndHole(holeGroup, xBall, yBall, ballGroup, bw, margin):
    # import values from other files and classes
    innerMargin = graphics.Border.innerMargin
    dist = graphics.Border.distToCornerSide
    extend = graphics.Border.extend
    extendX = graphics.Border.extend*math.cos(math.pi/4)
    holeR = graphics.Hole.radius
    r = ballClass.Ball.radius
    
    # Slop ranges of lines that connect to corner holes  
    slope1 = abs((extendX - r)/(innerMargin - dist + extendX + \
    r*math.cos(math.pi/4)))
    slope2 = 1/slope1
    
    slope3 = abs((r*math.cos(math.pi/4) + holeR) / \
    (r*math.cos(math.pi/4) - 2*holeR))
    #slope4 = 1/slope3
    
    
    listValid = []
    for hole in holeGroup:
        ballIntersect = False
        if ballLine(hole.rect.centerx, hole.rect.centery, xBall, yBall) != None:
            a = ballLine(hole.rect.centerx, hole.rect.centery, xBall, yBall)[0]
            b = ballLine(hole.rect.centerx, hole.rect.centery, xBall, yBall)[1]
            c = ballLine(hole.rect.centerx, hole.rect.centery, xBall, yBall)[2]
            # Check distance with every ball and line to determine if 
            # colliding ball would intersect with other balls when moving 
            # in this direction
            for ball in ballGroup:
                if ball.rect.centerx != xBall and ball.rect.centery != yBall:
                    x = ball.rect.centerx
                    y = ball.rect.centery  
                    if (x <= max(hole.rect.centerx, xBall) and \
                    x >= min(hole.rect.centerx, xBall))\
                    or(y <= max(hole.rect.centery, yBall) and \
                    y >= min(hole.rect.centery, yBall)):
                        if distPointLine(a, b, c, x, y) \
                        <=  2*ball.radius:
                            ballIntersect = True
        
        # Check whether colliding ball would collide with borders        
        if not ballIntersect:
            if hole.rect.centerx == bw/2 + margin:
                if abs(a) > slope3:
                    listValid.append((hole.rect.centerx, hole.rect.centery))
            else:
                if abs(a) < max(slope1, slope2) and abs(a) > \
                min(slope2, slope1):
                    listValid.append([hole.rect.centerx, hole.rect.centery])
    
    return listValid
    

# Return the centerx and centery of the clicked ball    
def ballPos(ballGroup, xCur, yCur, typePlay):
    for ball in ballGroup:
        if (type(ball) == ballClass.Ball and typePlay == 'solid') or \
         (type(ball) == ballClass.stripedBalls and typePlay == 'striped'):
            if distance(ball.rect.centerx, ball.rect.centery, xCur, yCur) <= \
            ball.radius:
                return (ball.rect.centerx, ball.rect.centery)
                
                
# Return all hint lines of a ball
def allLines(ballGroup, player1, player2, display1, wx, wy, holeGroup, \
bw, margin, bh):
    hintPoints = []
    for ball in ballGroup:
        if ball.color != (255 , 255, 255):           
            x = ball.rect.centerx
            y = ball.rect.centery
            if player1 != None:
                if display1:
                    if (player1.type == 'solid' and \
                    type(ball) == ballClass.Ball) \
                    or (player1.type == 'striped' \
                    and type(ball) == ballClass.stripedBalls):
                        hintOne = whiteAndBall(wx, wy, ballGroup, \
                        holeGroup, x, y, bw, margin, bh)
                        if hintOne != None:
                            hintPoints.append(hintOne)
                else:
                    if (player2.type == 'solid' \
                    and type(ball) == ballClass.Ball) \
                    or (player2.type == 'striped' \
                    and type(ball) == ballClass.stripedBalls):
                        hintOne = whiteAndBall(wx, wy, ballGroup, holeGroup, \
                        x, y, bw, margin, bh)
                        if hintOne != None:
                            hintPoints.append(hintOne)
                            
            else:
                hintOne = whiteAndBall(wx, wy, ballGroup, holeGroup, x, y, \
                        bw, margin, bh)
                if hintOne != None:
                    hintPoints.append(hintOne)
                        
    return hintPoints
    
 
# Return hint lines of all balls
def drawAllLines(screen, ballGroup, player1, player2, display1, wx, wy, \
holeGroup, bw, margin, bh):
    allPoints = allLines(ballGroup, player1, player2, display1, wx, wy, \
    holeGroup, bw, margin, bh)
    if allPoints != []:
        for points in allPoints:
            for i in range(len(points)):
                x1 = points[i][0]
                y1 = points[i][1]
                x2 = points[i][2]
                y2 = points[i][3]            
                x3 = points[i][4]
                y3 = points[i][5]
                pygame.draw.lines(screen, (220,20,60), False, \
                [(x1, y1), (x2, y2), (x3, y3)], 2)
                pygame.draw.circle(screen, (255, 255, 255), (int(x2), int(y2)),\
                ballClass.Ball.radius,2)
                        
                        
                        
                        
                        