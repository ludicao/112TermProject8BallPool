import math
import pygame
import collisions
import text

# Ball class        
class Ball(pygame.sprite.Sprite):
    
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
                (176, 80, 32),  # stripped brown
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
        pygame.draw.circle(self.imageWhite, (255, 255, 255), \
        (Ball.innerRadius, Ball.innerRadius), Ball.innerRadius, 0)
        dest = Ball.radius - Ball.innerRadius
        self.image.blit(self.imageWhite,(dest, dest))
        
        # Blitting position differs if it's a two digit or one digit number
        if len(str(self.number)) == 2:
            self.image.blit(text, (10, 8))
        else:
            self.image.blit(text, (12, 8))


    # Update ball position, speed, angle    
    def update(self, balls, holes, fric):        
        # Check if collision occurs
        for ball in balls:
            if ball != self and pygame.sprite.collide_circle(self, ball):
                # Make sure ball with speed is of first parameter
                if self.xSpeed == 0 and self.ySpeed == 0 and \
                (ball.xSpeed != 0 or ball.ySpeed != 0):
                    if ball.color == (255, 255, 255):
                        ball.violation = False                  
                    collisions.collide(ball, self)
                elif abs(self.xSpeed) <= 0.01 and abs(self.xSpeed) <= 0.01 \
                and abs(self.ySpeed) <= 0.01 and abs(self.xSpeed) <= 0.01:
                    continue
                else:
                    if self.color == (255, 255, 255):
                        ball.violation = False                  
                    collisions.collide(self,  ball)

        
        oldX = self.rect.x
        oldY = self.rect.y
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed        
        # Update ball position:
        for ball in balls:
            if self != ball and pygame.sprite.collide_circle(self, ball): 
                collisions.adjustCollision(self, ball, oldX, oldY, Ball.radius)
    

        
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
        pygame.draw.circle(self.image, (255, 255, 255),(Ball.radius, Ball.radius), \
                           Ball.radius, 0)        
        self.rect = self.image.get_rect()
        self.rect.center = x,y
        
        
        # Colored circle on second layer                   
        self.imageColor = pygame.Surface((colorSide, colorSide))
        self.imageColor.fill((255, 255, 255))
        self.imageColor.set_colorkey((255, 255, 255))
        pygame.draw.circle(self.imageColor, self.color, \
        (stripedBalls.colorRadius, stripedBalls.colorRadius), \
        stripedBalls.colorRadius, 0)
        dest = Ball.radius - stripedBalls.colorRadius
        self.image.blit(self.imageColor,(dest, dest))
        
        
        # White circle on thrid layer
        self.imageWhite = pygame.Surface((innerSide, innerSide))
        self.imageWhite.fill((self.color))
        self.imageWhite.set_colorkey((self.color))
        pygame.draw.circle(self.imageWhite, (255, 255, 255), \
        (Ball.innerRadius, Ball.innerRadius), Ball.innerRadius, 0)
        dest = Ball.radius - Ball.innerRadius
        self.image.blit(self.imageWhite, (dest, dest))
        destText = (side**2+side**2)**0.5*math.cos(math.pi/4)
        
        
        # Blitting positions differs if number is two digits or one
        if len(str(self.number)) == 2:
            self.image.blit(text, (10, 8))
        else:
            self.image.blit(text, (12, 8))
          
