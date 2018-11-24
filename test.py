        
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

# Return list of two bool values to check if ball is in board xrange and yrange        
def borderCheck(ball, margin, boardHeight, boardWidth):
    innnerMarign = graphics.Border.innerMargin
    distCorner = graphics.Border.distToCornerSide
    extend = graphics.Border.extend
    holeR = graphics.Hole.radius
    
    if type(ball) != pygame.sprite.Group:
        listRange = [True, True]
        if ball.rect.centerx >= boardWidth/2 + margin + holeR or ball.rect.centerx <= boardWidth/2 + margin - holeR:
            if ball.rect.y <= margin +  or ball.rect.y >= boardHeight+margin-2*ball.radius:
                listRange[1] = False
            elif ball.rect.x <= margin or \
            ball.rect.x >= boardWidth+margin-2*ball.radius:
                listRange[0] = False
        return listRange
    

# Function to ensure ball doesn't go out of bounds right after collision call    
def adjustBorderCollision(ball, oldX, oldY, margin, boardHeight, boardWidth):
    listRange = borderCheck(ball, margin, boardHeight, boardWidth)
    if listRange[0] == False:
        if ball.rect.x <= margin:
           ball.rect.x += margin - ball.rect.x
        elif ball.rect.x >= boardWidth+margin-2*ball.radius:
            ball.rect.x -= ball.rect.x + 2*ball.radius - boardWidth - margin
    if listRange[1] == False:
        if ball.rect.y <= margin:
            ball.rect.y += margin - ball.rect.y
        elif ball.rect.y >= boardHeight+margin-2*ball.radius:
            ball.rect.y -= ball.rect.y + 2*ball.radius - boardHeight - margin
    



# Function to ensure two balls don't overlap right after collision call            
def adjustCollision(ball1, ball2, oldX, oldY):
    dist = distance(ball1.rect.x, ball1.rect.y, ball2.rect.x, ball2.rect.y)
    triSide = abs(ball2.rect.x - ball1.rect.x)
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