import pygame
import pool
import ballClass
import math

# Player class
class Player():
    
    # Check whether player continues if hits a ball
    playerContinue = False
    
    # Initial values
    def __init__(self, type, num, name, ballList):
        self.type = type
        self.name = name
        self.num = num
        self.ballList = ballList
    
    # Draw the text on top matching player with ball type    
    def draw(self, screen, screenWidth, margin):
        self.font = pygame.font.Font('cmunti.ttf', 30)
        text = self.font.render('%s: %s' % (str(self.name), self.type), \
               True, (0, 0, 0))
               
        x = screenWidth/3
        y = 0
        
        screen.blit(text, (x,y))


    # Draw the text on top if player has no ball type yet
    @ staticmethod
    def drawNone(screen, screenWidth, margin, bool, name):
        font = pygame.font.Font('cmunti.ttf', 30)
        # bool indicates whether it's player 1 text or player 2 text
        if bool:
            text = font.render(name, True, (0, 0, 0))
        else:
            text = font.render(name, True, (0, 0, 0))
            
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
        text = self.font.render('%s:' % str(self.name), True, (0, 0, 0))
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
        

# Name entry box class        
class nameBox():
    
    # Initialize values
    def __init__(self, player, y, screenWidth, nameShow, textName, cur):
        self.x = screenWidth*0.4
        self.y = y
        self.width = screenWidth*0.2
        self.screenWidth = screenWidth
        self.color = (255, 255, 255)
        self.textColor = (192, 192, 192)
        self.player = player    # Player 1 or Player 2
        
        # If True, text entry updates the name being typed in
        # If False, text shows "Enter your name"
        self.nameShow = nameShow    
        
        
        self.textName = textName     # Player name typed in
        self.cur = cur    # If True shows the cursor
    
    
    # Draw the name entry box and the title 'Player 1' / 'Player 2'    
    def draw(self, screen):
        font = pygame.font.Font('Aller_Rg.ttf', 16)
        # Text title above the entry box 'Player 1' / 'Player 2'
        text = font.render(self.player, True, (255, 255, 255))
        screen.blit(text, (self.screenWidth/2 - text.get_rect().width/2, \
                           self.y ))
                           
        # Text inside the entry box
        fontSmall = pygame.font.Font('Aller_Rg.ttf', 15)
        textSmall = fontSmall.render('Enter your name here!', \
                                      True, self.textColor)
        topTextHeight = text.get_rect().height
        startYBox = topTextHeight + self.y + 2
        heightBox = textSmall.get_rect().height + 2
        
        # Draw dimensions of entry box based on text size
        pygame.draw.rect(screen, self.color, \
        (self.x, startYBox, self.width, heightBox))
        
        
        if not self.nameShow:
            screen.blit(textSmall, (self.x+1, startYBox + 1))
        # If box is clicked on, update typed name
        else:
            textName = fontSmall.render(self.textName, \
                                        True, self.textColor)
            cursorX = textName.get_rect().width + 1 + self.x
            cursorY = startYBox + 1
            cursorLen = textName.get_rect().height
            cursorYEnd = cursorY + cursorLen
            # If True shows cursor
            if self.cur:
                pygame.draw.lines(screen, self.textColor, False, \
            [(cursorX, cursorY), (cursorX, cursorYEnd)], 2)
            screen.blit(textName, (self.x + 1, startYBox + 1))


    # Returns the height of the entry box and the title
    def heightTextBox(self):
        font = pygame.font.Font('Aller_Rg.ttf', 15)
        text = font.render(self.player, True, (255, 255, 255))
        return text.get_rect().height + 2


    # Returns the starting position of y of the next name entry title
    def startYBox(self):
        font = pygame.font.Font('Aller_Rg.ttf', 16)
        text = font.render(self.player, True, (255, 255, 255))
        return text.get_rect().height + self.y + 2
        
        

        
        

        
        
            

            
        
               
        
            
        

    
    
        

        
        
    