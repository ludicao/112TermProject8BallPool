import pygame
import pool
import ballClass
import math

# Player class
class Player():
    
    # Check whether player continues if hits a ball
    playerContinue = False
    
    # Initial values
    def __init__(self, type, num, ballList):
        self.type = type
        self.num = num
        self.ballList = ballList
    
    # Draw the text on top matching player with ball type    
    def draw(self, screen, screenWidth, margin):
        self.font = pygame.font.Font('cmunti.ttf', 30)
        text = self.font.render('Player %s: %s' % (str(self.num), self.type), \
               True, (0, 0, 0))
               
        x = screenWidth/3
        y = 0
        
        screen.blit(text, (x,y))


    # Draw the text on top if player has no ball type yet
    @ staticmethod
    def drawNone(screen, screenWidth, margin, bool):
        font = pygame.font.Font('cmunti.ttf', 30)
        # bool indicates whether it's player 1 text or player 2 text
        if bool:
            text = font.render('Player 1', True, (0, 0, 0))
        else:
            text = font.render('Player 2', True, (0, 0, 0))
            
        x = screenWidth/5*2
        y = 0
        
        screen.blit(text, (x,y))



    # Draw hit balls on bottom of screen    
    def drawScore(self, screen, screenMargin, boardHeight, boardWidth):
        radius = ballClass.Ball.radius
        startX = screenMargin
        
        # Player 2 has a greater startY
        if self.num == 2:
            startY = boardHeight + 2*screenMargin
        elif self.num == 1:
            startY = boardHeight + screenMargin
            
        
        self.font = pygame.font.Font('cmunti.ttf', 15)
        text = self.font.render('Player %s:' % str(self.num), True, (0, 0, 0))
        screen.blit(text, (startX, startY))
        
        # Draw striped balls
        if self.type == 'striped':
            # Match striped balls to the right player
            if self.num == 1:
                starty = boardHeight + screenMargin + ballClass.Ball.radius
            elif self.num == 2:
                starty = boardHeight + 2*screenMargin + ballClass.Ball.radius
            
            for i in range(len(self.ballList)):
                startx = int(boardWidth/8 + 3*i*radius + screenMargin)
                self.drawStriped(screen, startx, starty, \
                self.ballList[i][0], self.ballList[i][1])
        
        # Draw solid Balls        
        elif self.type == 'solid':
            if self.num == 1:
                starty = boardHeight + screenMargin + ballClass.Ball.radius
            elif self.num == 2:
                starty = boardHeight + 2*screenMargin + ballClass.Ball.radius
                
            for i in range(len(self.ballList)):
                startx = int(boardWidth/8 + 3*i*radius + screenMargin)
                self.drawSolid(screen, startx, starty, \
                self.ballList[i][0], self.ballList[i][1])
    
                
    # Draw solid balls
    def drawSolid(self, screen, startx, starty, number, color):
        radius = ballClass.Ball.radius
        innerRadius = ballClass.Ball.innerRadius
        self.font = pygame.font.Font('Aller_Rg.ttf', 9)
        textNum = self.font.render(number, True, (0, 0, 0))
        
        # Bottom colored layer
        pygame.draw.circle(screen, color,(startx, starty), radius, 0)        
        
        # White circle on second layer                  
        pygame.draw.circle(screen, (255, 255, 255), \
        (startx, starty), innerRadius, 0)
       
       
        # Number is in center of ball 
        x = startx + ballClass.Ball.radius/2 - textNum.get_rect().width/2
        y = starty + ballClass.Ball.radius/2 -textNum.get_rect().height/2
        screen.blit(textNum, (startx-innerRadius+2, starty-innerRadius+2))
        
    # Draw striped balls
    def drawStriped(self, screen, startx, starty, number, color):        
        radius = ballClass.Ball.radius
        innerRadius = ballClass.Ball.innerRadius
        colorRadius = ballClass.stripedBalls.colorRadius
        
        self.font = pygame.font.Font('Aller_Rg.ttf', 9)
        textNum = self.font.render(number, True, (0, 0, 0))

        # Bottom white layer(white strips)
        pygame.draw.circle(screen, (255, 255, 255),(startx, starty), radius, 0)        
                    
        # Colored circle on second layer                   
        pygame.draw.circle(screen, color,(startx, starty), colorRadius, 0)
            
        # White circle on thrid layer
        pygame.draw.circle(screen, (255, 255, 255),\
                          (startx, starty), innerRadius, 0)
       
        # Number is in center of ball                 
        x = startx + ballClass.Ball.radius/2 - textNum.get_rect().width/2
        y = starty + ballClass.Ball.radius/2 -textNum.get_rect().height/2
        screen.blit(textNum, (startx-innerRadius+2, starty-innerRadius+2))
            

            
        
               
        
            
        

    
    
        

        
        
    