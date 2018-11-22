import math

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
    if ball1.rect.x < ball2.rect.x and ball1.rect.y > ball2.rect.y:
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
            ball1.xSpeed = ballV*math.sin(hitAngle)*1/5
            
        
            
    # When striking ball is in upper right posision    
    if ball1.rect.x > ball2.rect.x and ball1.rect.y > ball2.rect.y:
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
            ball1V = ball1.ySpeed*sinAngle - ball1.xSpeed*cosAngle
            ball2V = -ball1.xSpeed*sinAngle - ball1.ySpeed*cosAngle
            ball1.xSpeed = -ball1V*cosAngle
            ball1.ySpeed = ball1V*sinAngle
            ball2.xSpeed = -ball2V*sinAngle
            ball2.ySpeed = -ball2V*cosAngle
            
        if hitAngle == strikeAngle:
            ball2.xSpeed = -ballV*math.cos(hitAngle)
            ball2.ySpeed = -ballV*math.sin(hitAngle)
            ball1.xSpeed = -ballV*math.cos(hitAngle)*1/5
            ball1.xSpeed = -ballV*math.sin(hitAngle)*1/5

    
    
    
    # When striking ball is in lower right position    
    if ball1.rect.x > ball2.rect.x and ball1.rect.y < ball2.rect.y:
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
            ball1.xSpeed = 0
            ball1.ySpeed = 0
    
            #ball1.xSpeed = -ballV*math.cos(hitAngle)*1/5
            #ball1.ySpeed = ballV*math.sin(hitAngle)*1/5
    
    
    # If two colliding balls are in same x or y level        
    if ball1.rect.x == ball2.rect.x or ball1.rect.y == ball2.rect.y:
        ballV = (ball1.xSpeed**2 + ball1.ySpeed**2)**0.5
        ball1.ySpeed, ball2.xSpeed = ball1.ySpeed, ball1.xSpeed
        ball1.xSpeed, ball2.ySpeed = 0, 0
        

# Change speed and direction when ball touches borders        
def collideBorder(ballGroup, margin, boardHeight, boardWidth):
    for ball in ballGroup:
        if ball.rect.y <= margin or \
        ball.rect.y >= boardHeight+margin:
            ball.ySpeed = -ball.ySpeed
        elif ball.rect.x <= margin or \
        ball.rect.x >= boardWidth+margin:
            ball.xSpeed = -ball.xSpeed
             