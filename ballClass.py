import math
import pygame
import collisions

# Ball class        
class Ball(pygame.sprite.Sprite):
    
    radius = 13    # Constant for all pool balls
    
    # Initialize values for ball
    def __init__(self, x, y, color):
        super().__init__()
        
        self.xSpeed = 0
        self.ySpeed = 0
        self.color = color

        
        # diameter of circle, also width and height of surface
        side = 2*Ball.radius 
        
        self.image = pygame.Surface((side, side))
        self.image.fill((33, 137, 88))
        self.image.set_colorkey((33, 137, 88))
        pygame.draw.circle(self.image, self.color,(Ball.radius, Ball.radius), \
                           Ball.radius, 0)
        self.rect = self.image.get_rect()
        self.rect.center = x,y


    # Update ball position, speed, angle    
    def update(self, balls, holes, fric):
        
        # Check if ball falls into holes
        for hole in holes:
            for ball in balls:
                dist = collisions.distance(hole.rect.x, hole.rect.y, \
                                           ball.rect.x, ball.rect.y)
                if dist <= (hole.radius + 15)*3/5:
                    ball.kill()
        
        
        # Check if collision occurs
        for ball in balls:
            if ball != self and pygame.sprite.collide_circle(self, ball):
                # Add this condition to prevent collision function running when
                # two balls have negligible speed
                '''
                if (abs(self.xSpeed) > 0.02 or abs(self.ySpeed) > 0.02) \
                or (abs(ball.xSpeed) > 0.02 or abs(ball.ySpeed) > 0.02):
                '''
                # Make sure ball with speed is of first parameter
                if self.xSpeed == 0 and self.ySpeed == 0 and \
                (ball.xSpeed != 0 or ball.ySpeed != 0):
                    collisions.collide(ball, self)
                elif abs(self.xSpeed) <= 0.01 and abs(self.xSpeed) <= 0.01 \
                and abs(self.ySpeed) <= 0.01 and abs(self.xSpeed) <= 0.01:
                    continue
                else:
                    collisions.collide(self,  ball)
                
                '''
                else:
                    self.xSpeed, self.ySpeed = 0, 0
                    ball.xSpeed, ball.ySpeed = 0, 0
                '''
                        
        
                
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