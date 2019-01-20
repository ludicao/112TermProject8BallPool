#############################
# File IO functions modeled from the 15-112 website
# https://www.cs.cmu.edu/~112/notes/notes-strings.html

# This file contains functions and classes of text such as the reading player's 
# name from name entry box, the player's ball type, buttons, and name inputs. It
# also include the basix IO functions that open the highScore.txt file, reads
# in player scores, an updates the file whenever a game is over and a player 
# wins.
#############################


import pygame
import pool
import ballClass
import math
import os

# Player class
class Player():
    
    # Check whether player continues if hits a ball
    playerContinue = False
    

    # Draw the text if when name and type needn't match
    @ staticmethod
    def drawNone(screen, screenWidth, margin, name):
        font = pygame.font.Font('cmunti.ttf', 30)
        text = font.render(name, True, (0, 0, 0))
            
        x = screenWidth / 2 - text.get_rect().width/2
        y = 0
        
        screen.blit(text, (x,y))
    
    # Initial values
    def __init__(self, type, num, name, ballList):
        self.type = type
        self.name = name
        self.num = num
        self.ballList = ballList
    
    # Draw the text on top showing opponent's turn with ball type    
    def draw(self, screen, screenWidth, margin):
        self.font = pygame.font.Font('cmunti.ttf', 30)
        text = self.font.render('%s\'s turn: %s' % (str(self.name), self.type), \
               True, (0, 0, 0))
               
        x = screenWidth/2 - text.get_rect().width/2
        y = 0
        
        screen.blit(text, (x,y))
        
    
    # Draw text if it's current player's turn
    def currTurn(self, screen, screenWidth, margin):
        self.font = pygame.font.Font('cmunti.ttf', 30)
        text = self.font.render('Your Turn: %s' % (self.type), True, (0, 0, 0))
               
        x = screenWidth/2 - text.get_rect().width/2
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
                startx = int(screenMargin + text.get_rect().width + 2 \
                + 3*i*radius + screenMargin)
                self.drawStriped(screen, startx, starty, \
                self.ballList[i][0], self.ballList[i][1])
        
        # Draw solid Balls        
        elif self.type == 'solid':
            if self.num == 1:
                starty = boardHeight + screenMargin + ballClass.Ball.radius
            elif self.num == 2:
                starty = boardHeight + 2*screenMargin + ballClass.Ball.radius
                
            for i in range(len(self.ballList)):
                startx = int(screenMargin + text.get_rect().width + 2 \
                + 3*i*radius + screenMargin)
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

             


# Draw the force bar and text            
def forceText(screen, width, margin, bh, bw, forceApplied, maxForce):
    font = pygame.font.Font('cmunti.ttf', 20)
    textForce = font.render('Force: ', True, (0, 0, 0))
    startForceX = width/5*3
    startForceY = 1.5*margin + bh
    screen.blit(textForce, (startForceX, startForceY))
    barWidth = bw/6
    barHeight = margin
    width = forceApplied/maxForce * barWidth
    pygame.draw.rect(screen, (204, 0, 102), \
                    (startForceX + 70, startForceY, width, barHeight), 0)
                    
# Draw the time remaining bar
def timebar(screen, countDownBool, margin, bw, bh, maxTime, seconds):
    if countDownBool:
        color = (219, 40, 40)
    else:
        color = (204, 0, 102)
    font = pygame.font.Font('cmunti.ttf', 20)
    text = font.render('Time', True, (0, 0, 0))
    screen.blit(text, (margin, 0))
    barWidth = bw/6
    barHeight = margin*0.75
    startY = (margin - barHeight)/2
    width = (maxTime - seconds)/maxTime * barWidth
    pygame.draw.rect(screen, color, (margin + \
            text.get_rect().width + 20, startY, width, barHeight), 0)
            
            
            
# Show the hint box for ball type
def hintBox(screen, width, height, margin, color):
    listPos = hintPos1(width, height, margin)
    x = listPos[0]
    widthBox = listPos[1]
    height = listPos[2]
    y = listPos[3]
    pygame.draw.rect(screen, color, (x, y, widthBox, height), 0)
    
    font = pygame.font.Font('cmunti.ttf', 20)
    text = font.render('Hint1', True, (0, 0, 0))
    xText = x + widthBox/2 - text.get_rect().width/2
    yText = y + height/2 - text.get_rect().height/2
    screen.blit(text, (xText, yText))

# Return the coordinates of the hint box for ball type
def hintPos1(width, height, margin):
    x = width*0.7
    widthBox = width * 0.1
    height = margin * 0.75
    y = (margin - height)/2
    return ([x, widthBox, height, y])



# Show the hint box for guide lines
def hintBox2(screen, width, height, margin, color):
    listPos = hintPos2(width, height, margin)
    x = listPos[0]
    widthBox = listPos[1]
    height = listPos[2]
    y = listPos[3]
    pygame.draw.rect(screen, color, (x, y, widthBox, height), 0)
    
    font = pygame.font.Font('cmunti.ttf', 20)
    text = font.render('Hint2', True, (0, 0, 0))
    xText = x + widthBox/2 - text.get_rect().width/2
    yText = y + height/2 - text.get_rect().height/2
    screen.blit(text, (xText, yText))
 
# Return the coordinates of the hint box for guide lines
def hintPos2(width, height, margin):
    x = width*0.85
    widthBox = width * 0.1
    height = margin * 0.75
    y = (margin - height)/2
    return ([x, widthBox, height, y])
    
    
# Check whether clicked on hint buttons
def clickHint(xhit, yhit, pos):
    xmin = pos[0]
    xmax = pos[0] + pos[1]
    ymin = pos[3]
    ymax = pos[3] + pos[2]
    
    if xhit <= xmax and xhit >= xmin and yhit <= ymax and yhit >= ymin:
        return True

# Read the high score text file and convert the string into list separated 
# by individuals        
def readScores(path):
    listNames = []
    with open(path, "rt") as f:
        scores = f.read()
        nameScores = scores.split('\n')
        for name in nameScores:
            listNames.append(name)
    return listNames
    
    
# Return the list of names so the highest scoring player is in most front 
def order(path):
    listNew = []
    listNames = readScores(path)
    dictOrder = dict()
    for i in range(len(listNames)):
        nameScore = listNames[i].split()
        dictOrder[int(nameScore[1])] = nameScore[0]
    for key in sorted(dictOrder):
        listNew.append(str(key) + " " + dictOrder[key] + '\n')
    return listNew
    
 
# Return the string of names so the highest scoring player is in most front  
def updateScore(player, path):
    hasPlayer = False
    listNames = readScores(path)
    listNew = ''
    for i in range(len(listNames)):
        nameScore = listNames[i].split()
        if nameScore[0] == player + ':':
            hasPlayer = True
            listNew += nameScore[0] + ' ' + str(int(nameScore[1])+1) + '\n'
        else:
            listNew += nameScore[0] + ' ' + nameScore[1] + '\n'
    if not hasPlayer:
        listNew += player + ': ' + '1' + '\n'
        
    return listNew[:-1]
    
# Write the content into the highScore text file    
def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)
    
    

    
        
        
        
        
        

    
        
            
            
        
               
        
            
        

    
    
        

        
        
    