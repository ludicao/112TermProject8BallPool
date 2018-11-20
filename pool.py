import math
import pygame

# Calculate distance beteween two points
def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

# Change ball speed and direction when collided    
def collide(ball1, ball2):

    dist = distance(ball1.rect.centerx, ball1.rect.centery, \
    ball2.rect.centerx, ball2.rect.centery)
    
    # Add small speed to prevent zero division error
    if ball1.xSpeed == 0 and ball1.ySpeed == 0:
        ball1.xSpeed = 0.05
        ball1.ySpeed = 0.05
    
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
            ball1.xSpeed = -ballV*math.cos(hitAngle)*1/5
            ball1.xSpeed = ballV*math.sin(hitAngle)*1/5
    
    
    # If two colliding balls are in same x or y level        
    if ball1.rect.x == ball2.rect.x or ball1.rect.y == ball2.rect.y:
        ballV = (ball1.xSpeed**2 + ball1.ySpeed**2)**0.5
        ball1.ySpeed, ball2.xSpeed = ball1.ySpeed, ball1.xSpeed
        ball1.xSpeed, ball2.ySpeed = 0, 0
             


# Gameboard class
class Gameboard(object):
    
    # Initialize values for gameboard
    def __init__(self, x, y, width, height):        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.friction = 0.5
        self.color = (33, 137, 88)
    
        
    # Draw the game board
    def draw(self, screen):      
        pygame.draw.rect(screen, self.color, \
        (self.x, self.y, self.width, self.height), 0)
        
        
# Ball class        
class Ball(pygame.sprite.Sprite):
    
    # Initialize values for ball
    def __init__(self, x, y, color):
        super().__init__()
        
        self.radius = 15    # Constant for all pool balls
        self.xSpeed = 0
        self.ySpeed = 0
        self.color = color

        
        # diameter of circle, also width and height of surface
        side = 2*self.radius 
        
        self.image = pygame.Surface((side, side))
        self.image.fill((33, 137, 88))
        self.image.set_colorkey((33, 137, 88))
        pygame.draw.circle(self.image, self.color,(self.radius, self.radius), \
                           self.radius, 0)
        self.rect = self.image.get_rect()
        self.rect.center = x,y


    # Update ball position, speed, angle    
    def update(self, balls, holes, fric):
        
        # Check if ball falls into holes
        for hole in holes:
            for ball in balls:
                dist = distance(hole.rect.x, hole.rect.y, ball.rect.x, ball.rect.y)
                if dist <= (hole.radius + 15)*3/5:
                    ball.kill()
        
        
        # Check if collision occurs
        for ball in balls:
            if ball != self and pygame.sprite.collide_circle(self, ball):
                # Add this condition to prevent collision function running when
                # two balls have negligible speed
                if (abs(self.xSpeed) > 0.15 or abs(self.ySpeed) > 0.15) \
                or (abs(ball.xSpeed) > 0.15 or abs(ball.ySpeed) > 0.15):
                    # Make sure ball with speed is of first parameter
                    if self.xSpeed == 0 and self.ySpeed == 0:
                        collide(ball, self)
                    else:
                        collide(self,  ball)
                        
        
                
        # Update ball position
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed
        
        # Apply add friction to ball speed
        if self.xSpeed != 0 or self.ySpeed != 0:
            if abs(self.xSpeed)+abs(self.ySpeed) != 0:
                xFric = abs(self.xSpeed)/(abs(self.xSpeed)+\
                abs(self.ySpeed))*fric
                yFric = abs(self.ySpeed)/(abs(self.xSpeed)+\
                abs(self.ySpeed))*fric
                
                # Check whether friction should apply to negative or positive
                # x direction
                if self.xSpeed > 0:
                    if self.xSpeed - xFric > 0:
                        self.xSpeed -= xFric
                    else:
                        # Stop xspeed of ball when xspeed is zero
                        self.xSpeed = 0
                elif self.xSpeed < 0:
                    if self.xSpeed + xFric < 0:
                        self.xSpeed += xFric
                    else:
                        self.xSpeed = 0

                # Check whether friction should apply to negative or positive
                # y direction                    
                if self.ySpeed > 0:
                    if self.ySpeed - yFric > 0:
                        self.ySpeed -= yFric
                    else:
                        # Stop yspeed ball when yspeed is zero
                        self.ySpeed = 0
                elif self.ySpeed < 0:
                    if self.ySpeed + yFric < 0:
                        self.ySpeed += yFric
                    else:
                        self.ySpeed = 0

# Hole Class
class Hole(pygame.sprite.Sprite):
    
    radius = 25    # Constant for all holes
    color = (0, 0, 0)    # All holes are black
    
    # Init values:
    def __init__(self, x, y):
        super().__init__()
                
        # diameter of circle, also width and height of surface
        side = 2*Hole.radius 
        
        self.image = pygame.Surface((side, side))
        self.image.fill((33, 137, 88))
        self.image.set_colorkey((33, 137, 88))
        pygame.draw.circle(self.image, Hole.color,(Hole.radius, Hole.radius), \
                           Hole.radius, 0)
        self.rect = self.image.get_rect()
        self.rect.center = x,y
        
        
class Cue(pygame.sprite.Sprite):
    
    color = (176, 101, 34)
    width = 100
    height = 5
    
    # Initialize values
    def __init__(self, x, y, angle):
        super().__init__()        
        self.image = pygame.Surface((Cue.width, Cue.height))
        #self.image = pygame.transform.rotate(self.image, angle)
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))
        pygame.draw.rect(self.image, Cue.color, \
                        (0, 0, Cue.width, Cue.height), 0)
        self.rect = self.image.get_rect()
        self.rect.center = x,y
        print(x)
        
        
        
            
    


# Pygame class                   
class Pygame():
    
    # Init function 
    def init(self):
        
        # Initialize gameboard and sprite groups
        self.xStart = self.margin
        self.yStart = self.margin
        self.width = self.width-2*self.margin
        self.height = self.height-2*self.margin
        self.gameboard = Gameboard(self.xStart, self.yStart, \
                                   self.width, self.height)
        self.ballGroup = pygame.sprite.Group() 
        self.holeGroup = pygame.sprite.Group()
        
        
        # Add holes to sprite group
        xFirstCol = self.margin + Hole.radius
        xSecondCol = self.width/2 + self.margin
        xThirdCol = self.width + self.margin - Hole.radius
        yFirstRow = self.margin + Hole.radius
        ySecondRow = self.height + self.margin - Hole.radius
        
        listPos = [(xFirstCol, yFirstRow), (xSecondCol, yFirstRow), \
                   (xThirdCol, yFirstRow), (xFirstCol, ySecondRow), \
                   (xSecondCol, ySecondRow), (xThirdCol, ySecondRow)]
                   
        for pos in listPos:
            self.holeGroup.add(Hole(pos[0], pos[1]))
        
        
        
        # Set up initial positions of colored balls
        positions = self.calculatePositions()
        for pos in positions:        
            self.ballGroup.add(Ball(pos[0], pos[1], (247, 56, 56)))            
        whiteX = self.width/4
        whiteY = self.height/2 
        
        # Initialize white ball
        self.whiteBall = Ball(whiteX, whiteY, (255, 255, 255))
        self.ballGroup.add(self.whiteBall)
        
        # Initilize cue position
        self.xCue = pygame.mouse.get_pos()[0]
        self.yCue = pygame.mouse.get_pos()[1]
        xDist = self.whiteBall.rect.centerx - self.xCue
        yDist = self.whiteBall.rect.centery - self.yCue
        angle = math.atan(xDist/yDist)/math.pi*180
        self.cue = pygame.sprite.Group() 
        self.cue.add(Cue(self.xCue, self.yCue, angle))
        self.hasHit = False
        for cue in self.cue:
            print(cue.rect.centerx)
        

    def mouseMotion(self):
        if self.hasHit == False:
            self.xCue = pygame.mouse.get_pos()[0]
            self.yCue = pygame.mouse.get_pos()[1]
            
        
    
    
    # Timerfired function    
    def timerFired(self, dt):


        self.ballGroup.update(self.ballGroup, self.holeGroup, \
        self.gameboard.friction)
        
        # Check if ball pool ball colides with border
        for ball in self.ballGroup:
            if ball.rect.y <= self.margin or \
            ball.rect.y >= self.height-self.margin:
                ball.ySpeed = -ball.ySpeed
            elif ball.rect.x <= self.margin or \
            ball.rect.x >= self.width-self.margin:
                ball.xSpeed = -ball.xSpeed
                
        # Check if all balls have stopped moving and cue stick appears
        numMoving = 0
        for ball in self.ballGroup:
            if ball.xSpeed == 0 and ball.ySpeed == 0:
                numMoving += 1
                
        if numMoving  == 0:
            self.hasHit = False
            
                
        
            
        
    def redrawAll(self, screen):
        self.gameboard.draw(screen)
        self.ballGroup.draw(screen)
        self.holeGroup.draw(screen)
        if self.hasHit == False:
            self.cue.draw(screen)
        
        
    # init values of the Pygame class
    def __init__(self, width=800, height=600, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.margin = 40
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()
    
    
    # Calculate positions of initial colored balls    
    def calculatePositions(self):     
        r = 15
        d = 2*r
        distanceX = d*math.cos(math.pi/6)
        distanceY = d*math.sin(math.pi/6)
        
        firstX = (self.width-2*self.margin)/3*2 + self.margin
        firstY1 = self.height/2
        
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
                (thirdX+8, thirdY1+8), (thirdX+8, thirdY2), \
                (thirdX+8, thirdY3-8),
                (fourthX+12, fourthY1+12), (fourthX+12, fourthY2+8), \
                (fourthX+12, fourthY3-8),(fourthX+12, fourthY4-12), 
                (fifthX+16, fifthY1+16), (fifthX+16, fifthY2+8), \
                (fifthX+16, fifthY3),(fifthX+16, fifthY4-8), \
                (fifthX+16, fifthY5-16)]
        
        
        
        
    # Run main function    
    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.whiteBall.xSpeed = 50
                    self.whiteBall.ySpeed = 0
                elif event.type == pygame.QUIT:
                    playing = False
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion()
            screen.fill((255,255,255))
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()


def main():
    game = Pygame()
    game.run()

if __name__ == '__main__':
    main()
    
            
                    

            
                
                
        
        
        
    