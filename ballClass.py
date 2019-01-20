#############################
# This file initializes the ball sprite class and initializes subclasses stripped balls, 
# whiteball, and blackball. It also includes functions to draw gray shades 
# on top of current player's opposite type balls. The balls are drawn through 
# the pygame.draw function.
# The ball class also contains an update() function which updates its posision
# and speed when it collides with other balls or the borders. It also checks to 
# see whether it has overlapped with another object after collision and takes 
# measures to prevent such overlapping from happening.
#############################


import math
import pygame
import collisions
import text
import positions

# Ball class        
class Ball(pygame.sprite.Sprite):
    
    # Pygame sound effects 
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_mode()
    ballHit = pygame.mixer.Sound("ballHit.wav")
    
    grayColor1 = (208,206,206)
    grayColor2 = (225,225,225)
    white = (255, 255, 255)
    
    radius = 15   
    innerRadius = 6    # All striped balls have an inner white circle
    
    @staticmethod
    # Return the colors of the ball                    
    def colorList():
        return [(255, 248, 18), # yellow
                (255, 27, 27),  # red
                (255, 27, 27),  # striped red
                (64, 148, 34),  # green
                (64, 148, 34),  # striped greed
                (255, 248, 18), # striped yellow
                (164, 14, 164), # purple
                (176, 80, 32),  # striped brown
                (255, 128, 0),  # striped orange
                (164, 14, 164), # striped purple
                (255, 128, 0),  # orange
                (51, 51, 255),  # striped blue
                (51, 51, 255),  # blue
                (176, 80, 32),  # brown
                ]
    
    # Return list of ball types, False for stripped and True for full color          
    def ballType():
        return [True, True, False, False, True, False, True, False, False, 
                False, True, False, True, True]
    
 
 
    # Return list of ball numbers            
    def ballNumber():
        return [1, 3, 11, 14, 8, 6, 2, 4, 15, 13, 12, 5, 10, 2, 7]
    
    
    # Initial values for balls
    def __init__(self, x, y, color, number):
        pygame.sprite.Sprite.__init__(self)
        
        self.xSpeed = 0
        self.ySpeed = 0
        self.color = color
        self.number = number
        self.font = pygame.font.Font('Aller_Rg.ttf', 9)
        text = self.font.render(number, True, (0, 0, 0))


        side = 2*Ball.radius
        innerSide = 2*Ball.innerRadius
        
        # Bottom colored layer
        self.image = pygame.Surface((side, side))
        self.image.fill((33, 137, 88))
        self.image.set_colorkey((33, 137, 88))
        pygame.draw.circle(self.image, self.color,(Ball.radius, Ball.radius), \
                           Ball.radius, 0)        
        self.rect = self.image.get_rect()
        self.rect.center = x,y
        
        # White circle on second layer                   
        self.imageWhite = pygame.Surface((innerSide, innerSide))
        self.imageWhite.fill((self.color))
        self.imageWhite.set_colorkey((self.color))
        pygame.draw.circle(self.imageWhite, Ball.white, \
        (Ball.innerRadius, Ball.innerRadius), Ball.innerRadius, 0)
        dest = Ball.radius - Ball.innerRadius
        self.image.blit(self.imageWhite,(dest, dest))
        
        x = side/2 - text.get_rect().width/2
        y = side/2 - text.get_rect().height/2
        self.image.blit(text, (x, y))
        
        self.hasCollided = False


    # Update ball position, speed, angle    
    def update(self, balls, holes, fric, dragWhite, margin, boardHeight, boardWidth):
        
        # Check collision with borders
        collisions.collideBorder(self, margin, boardHeight, boardWidth)
        
        # Update ball position:
        oldX = self.rect.centerx
        oldY = self.rect.centery
        self.rect.centerx += self.xSpeed
        self.rect.centery += self.ySpeed  
        
        # Make sure ball doesn't overlap another ball when its position is 
        # updated after the collision method
        for ball in balls:
            if not dragWhite:
                if (self != ball and pygame.sprite.collide_circle(self, ball)) \
                or (self != ball and \
                collisions.detectFast(self, ball, oldX, oldY)):
                    selfSpeed = (self.xSpeed**2 + self.ySpeed**2)**0.5
                    # Adjust collision volume based on ball speed
                    if selfSpeed/30 >= 1:
                        selfSpeed = 30
                    Ball.ballHit.set_volume(selfSpeed/30)
                    Ball.ballHit.play()
                    collisions.adjustCollision(self, ball, oldX, oldY)
                    if self.color == (255, 255, 255):                    
                        self.violation = False

                    

        
        # Apply friction to ball speed
        if self.xSpeed != 0 or self.ySpeed != 0:
            if abs(self.xSpeed)+abs(self.ySpeed) != 0:
                xFric = abs(self.xSpeed)/(abs(self.xSpeed)+\
                abs(self.ySpeed))*fric
                yFric = abs(self.ySpeed)/(abs(self.xSpeed)+\
                abs(self.ySpeed))*fric
                
                # Check whether friction should apply to negative or positive
                # x direction
                if self.xSpeed >= 0:
                    if self.xSpeed - xFric >= 0:
                        self.xSpeed -= xFric
                    else:
                        # Stop xspeed of ball when xspeed is zero
                        self.xSpeed = 0
                elif self.xSpeed < 0:
                    if self.xSpeed + xFric <= 0:
                        self.xSpeed += xFric
                    else:
                        self.xSpeed = 0

                # Check whether friction should apply to negative or positive
                # y direction                    
                if self.ySpeed >= 0:
                    if self.ySpeed - yFric >= 0:
                        self.ySpeed -= yFric
                    else:
                        # Stop yspeed ball when yspeed is zero
                        self.ySpeed = 0
                elif self.ySpeed < 0:
                    if self.ySpeed + yFric <= 0:
                        self.ySpeed += yFric
                    else:
                        self.ySpeed = 0
                        
        

        # Make sure ball doesn't go beyond the border when its position just 
        # changed after the collideBorder method
        listRange = collisions.borderCheck(self, margin, boardHeight, \
                                                         boardWidth)
        if False in listRange:
            collisions.adjustBorderCollision(self, oldX, \
                        oldY, margin, boardHeight, boardWidth)
    

               
        
# Whiteball class
class whiteBall(Ball):
    
    def __init__(self, x, y, color, number):
        super().__init__(x, y, color, number)
        # Violation when ball doesn't strike other balls or goes into holes
        self.violation = True  
        self.holeViolation = False  
        

# Black Ball class        
class blackBall(Ball):
    
    def __init__(self, x, y, color, number):
        super().__init__(x, y, color, number)
        # Violation when ball goes into holes before other balls
        self.blackViolation = False

# Striped Balls         
class stripedBalls(Ball):
    
    colorRadius = 12    # Radius of the colored circle
    
    def __init__(self, x, y, color, number):
        
        super().__init__(x, y, color, number)
        self.font = pygame.font.Font('Aller_Rg.ttf', 10)
        text = self.font.render(number, True, (0, 0, 0))
        
        side = 2*Ball.radius
        colorSide = 2*stripedBalls.colorRadius
        innerSide = 2*Ball.innerRadius
        
        # Bottom white layer(white strips)
        self.image = pygame.Surface((side, side))
        self.image.fill((33, 137, 88))
        self.image.set_colorkey((33, 137, 88))
        pygame.draw.circle(self.image, Ball.white,(Ball.radius, Ball.radius), \
                           Ball.radius, 0)        
        self.rect = self.image.get_rect()
        self.rect.center = x,y
        
        
        # Colored circle on second layer                   
        self.imageColor = pygame.Surface((colorSide, colorSide))
        self.imageColor.fill(Ball.white)
        self.imageColor.set_colorkey(Ball.white)
        pygame.draw.circle(self.imageColor, self.color, \
        (stripedBalls.colorRadius, stripedBalls.colorRadius), \
        stripedBalls.colorRadius, 0)
        dest = Ball.radius - stripedBalls.colorRadius
        self.image.blit(self.imageColor,(dest, dest))
        
        
        # White circle on thrid layer
        self.imageWhite = pygame.Surface((innerSide, innerSide))
        self.imageWhite.fill((self.color))
        self.imageWhite.set_colorkey((self.color))
        pygame.draw.circle(self.imageWhite, Ball.white, \
        (Ball.innerRadius, Ball.innerRadius), Ball.innerRadius, 0)
        dest = Ball.radius - Ball.innerRadius
        self.image.blit(self.imageWhite, (dest, dest))
        destText = (side**2+side**2)**0.5*math.cos(math.pi/4)
        
        
        x = side/2 - text.get_rect().width/2
        y = side/2 - text.get_rect().height/2
        self.image.blit(text, (x, y))
        
    
# Draw the gray shade of opponent's ball when current player's turn
def grayShade(screen, ballGroup, solidDraw, whiteDraw, blackDraw, \
stripedDraw, playBall):
   
    solid = []
    striped = []
    for ball in ballGroup:
        if type(ball) == Ball:
            solid.append([ball.rect.centerx, ball.rect.centery, \
            ball.color, ball.number])
        elif type(ball) == stripedBalls:
            striped.append([ball.rect.centerx, ball.rect.centery,\
            ball.color, ball.number])
        elif type(ball) == whiteBall:
            white = [ball.rect.centerx, ball.rect.centery,\
            (255, 255, 255), None]
        elif type(ball) == blackBall:
            black = [ball.rect.centerx, ball.rect.centery,\
            (0, 0, 0), '8']
                        
    Ball.white = Ball.grayColor2
    
    # Draw solid and shade striped
    if playBall == 'solid':
        for i in range(len(solid)):    
            if solid[i][2] != (0, 0, 0) and solid[i][2] != (255, 255, 255):
                solidDraw.add(Ball(solid[i][0], solid[i][1], \
                solid[i][2], str(solid[i][3])))
        solidDraw.draw(screen)

        for i in range(len(striped)):      
            stripedDraw.add(stripedBalls(striped[i][0], striped[i][1], \
            Ball.grayColor1, str(striped[i][3])))
            
        stripedDraw.draw(screen)
        whiteDraw.add(whiteBall(white[0], white[1], white[2], white[3]))
        blackDraw.add(blackBall(black[0], black[1], black[2], black[3]))
        blackDraw.draw(screen)
        whiteDraw.draw(screen)

    # Draw striped and shade solide
    elif playBall == 'striped':

        for i in range(len(striped)):
            stripedDraw.add(stripedBalls(striped[i][0], striped[i][1], \
            striped[i][2], str(striped[i][3])))
        stripedDraw.draw(screen)
         
        for i in range(len(solid)):
            if solid[i][2] != (255, 255, 255):
                solidDraw.add(Ball(solid[i][0], solid[i][1], \
                Ball.grayColor1, str(solid[i][3])))
                
        solidDraw.draw(screen)
        whiteDraw.add(whiteBall(white[0], white[1], white[2], white[3]))
        blackDraw.add(blackBall(black[0], black[1], black[2], black[3]))
        blackDraw.draw(screen)
        whiteDraw.draw(screen)
        
        
        
# Add Initial ball positions to sprite group
def initialPos(ballGroup, width, margin, height, ballPos):
    ballColor = Ball.colorList()
    ballType = Ball.ballType()
    ballNum = Ball.ballNumber()
        
    for i in range(4):  
        if ballType[i] == True:
            ballGroup.add(Ball(ballPos[i][0], \
            ballPos[i][1], ballColor[i], str(ballNum[i])))
        else:
            ballGroup.add(stripedBalls(ballPos[i][0], \
            ballPos[i][1], ballColor[i], str(ballNum[i])))
                
    for i in range(4, len(ballPos)-1):
        if ballType[i] == True:
            ballGroup.add(Ball(ballPos[i+1][0], \
            ballPos[i+1][1], ballColor[i], str(ballNum[i])))
        else:
            ballGroup.add(stripedBalls(ballPos[i+1][0], \
            ballPos[i+1][1], ballColor[i], str(ballNum[i])))
            
    return ballGroup
    
# Check if clicked on correct type of ball
def clickBall(ballGroup, type, xCur, yCur):
    for ball in ballGroup:
        xMin = ball.rect.x
        xMax = ball.rect.x + 2*ball.radius
        yMin = ball.rect.y
        yMax = ball.rect.y + 2*ball.radius
        if xCur >= xMin and xCur <= xMax and yMin <= yCur and yMax >= yCur:
            return ([ball.rect.centerx, ball.rect.centery])
            
            

    

