import pygame
import math

# Gameboard class
class Gameboard(object):   
    # Initialize values for gameboard
    def __init__(self, x, y, width, height):        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.friction = 1
        self.color = (33, 137, 88)
    
        
    # Draw the game board
    def draw(self, screen):      
        pygame.draw.rect(screen, self.color, \
        (self.x, self.y, self.width, self.height), 0)
        
        
# Hole Class
class Hole(pygame.sprite.Sprite):
    
    radius = 25   # Constant for all holes
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
        
# Cue class        
class Cue(pygame.sprite.Sprite):

    # Constant
    color = (176, 101, 34)
    length = 200
    distanceFromWhite = 30
    thickness = 4
    
    # Initialize values
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
     
    # Draw function
    def draw(self, screen):
        pygame.draw.lines(screen, Cue.color, False, \
        [(self.x1, self.y1), (self.x2, self.y2)], self.thickness)
        
        
# Class for guiding lines for cue stick to strike        
class GuideLines():
    
    gap = 20
    length = 40
    color = (255, 255, 255)
    extendingDist = 800
    thickness = 2
    
    def __init__(self, xStart, yStart, extendAngle):
        self.xStart = xStart
        self.yStart = yStart
        self.extendAngle = extendAngle

       
    def draw(self, screen):
        drawNum = self.extendingDist // (self.gap + self.length) + 1
        for i in range(drawNum):
            x1 = self.xStart - \
                 i*(self.length+self.gap)*math.cos(self.extendAngle)
            y1 = self.yStart + \
                 i*(self.length+self.gap)*math.sin(self.extendAngle)
            x2 = x1 + GuideLines.length*math.cos(self.extendAngle)
            y2 = y1 - GuideLines.length*math.sin(self.extendAngle)
            
            pygame.draw.lines(screen, self.color, False, \
                              [(x1, y1), (x2, y2)], self.thickness)


# Draw polygon whose sides are gameboard's borders                              
class Border():
    
    innerMargin = 60    # Inner margin of the gameboard
    
    # Two values determine how 'pushed in' the corner four holes are
    # Calculated values based on hole radius and inner margin
    distToCornerSide = (2*Hole.radius + 2**0.5*innerMargin) / 2**0.5
    extend = (distToCornerSide + 2*Hole.radius - innerMargin) / \
             (2*math.cos(math.pi/4))
    
    # Initialize variables for border size calculations and other values
    def __init__(self, screenWidth, screenHeight, outerMargin, boardHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.boardHeight = boardHeight
        self.outerMargin = outerMargin
        self.color = (210, 158, 52)
        
    
    # Return list of vertices of the top and bottom of the border polygon
    def calculateUpDown(self, starty, r, extend):
        outerMargin = self.outerMargin
        radius = Hole.radius
        extendX = Border.extend
        
        firstx = self.screenWidth - outerMargin - \
        Border.distToCornerSide + Border.extend*math.cos(math.pi/4)
        firsty = starty
        
        secondx = firstx - extendX*math.cos(math.pi/4)
        secondy = firsty + extend*math.cos(math.pi/4)
        
        thirdx = self.screenWidth/2 + 2*radius
        thirdy = secondy
        
        fourthx = self.screenWidth/2 + radius
        fourthy = thirdy -r
        
        fifthx = fourthx - 2*radius
        fifthy = fourthy
        
        sixthx = fifthx - radius
        sixthy = fifthy + r
        
        seventhx = outerMargin + Border.distToCornerSide
        seventhy = sixthy
        
        eigthx = seventhx - extendX*math.cos(math.pi/4)
        eigthy = seventhy - extend*math.cos(math.pi/4)
            
        return [(firstx, firsty),
                (secondx, secondy),
                (thirdx, thirdy),
                (fourthx, fourthy),
                (fifthx, fifthy),
                (sixthx, sixthy),
                (seventhx, seventhy),
                (eigthx, eigthy)]
                
    
    # Return list of vertices of the left and right side of the border polygon
    def calculateLeftRight(self, startx, extend):
        outerMargin = self.outerMargin
        extendY = Border.extend
        radius = Hole.radius
        
        firstx = startx
        firsty = outerMargin + Border.distToCornerSide - extendY*math.cos(math.pi/4)
        
        secondx = firstx + extend*math.cos(math.pi/4)
        secondy = firsty + extendY*math.cos(math.pi/4)
        
        thirdx = secondx
        thirdy = secondy + (self.boardHeight-2*Border.distToCornerSide)
        
        fourthx = thirdx - extend*math.cos(math.pi/4)
        fourthy = thirdy + extendY*math.cos(math.pi/4)
        
        return [(firstx, firsty),
                (secondx, secondy),
                (thirdx, thirdy),
                (fourthx, fourthy)]
    
    
    # Append four list of vertices of the four sides of the board to a new list   
    def calculatePoints(self):
        outerMargin = self.outerMargin
        listPoints = []
        starty = outerMargin + Border.innerMargin - Border.extend*math.cos(math.pi/4)
        topPoints = self.calculateUpDown(starty, Hole.radius, Border.extend)
        listPoints.extend(topPoints)
        
        startx = outerMargin + Border.innerMargin - Border.extend*math.cos(math.pi/4)
        leftPoints = self.calculateLeftRight(startx, Border.extend)
        listPoints.extend(leftPoints)
        
        starty = outerMargin + self.boardHeight - \
        Border.innerMargin + Border.extend*math.cos(math.pi/4)
        downPoints = self.calculateUpDown(starty, \
        -Hole.radius, -Border.extend)
        listPoints.extend(reversed(downPoints))
        
        startx = self.screenWidth - outerMargin - \
        Border.innerMargin + Border.extend*math.cos(math.pi/4)
        rightPoints = \
        self.calculateLeftRight(startx, -Border.extend)
        listPoints.extend(reversed(rightPoints))
        
        return listPoints
     
    # Draw the border polygon using the list of vertices
    def draw(self, screen):
        allPoints = self.calculatePoints()
        pygame.draw.polygon(screen, self.color, allPoints, 0)
        
        
        
        
        
        
