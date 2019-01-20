#############################
# The Sockets Client Framework is modeled from the sample code from the 15-112 website
# https://drive.google.com/drive/folders/0B3Jab-H-9UIiZ2pXMExjdDV1dW8

# Pygame Animation Framework is modeled from the pygame lecture notes from the 15-112 website
# https://github.com/LBPeraza/Pygame-Asteroids

# This file runs the game mode of the pool game. It sets up the board graphics, 
# imports from the collision file to detect and mimic various physics collisions,
# and responds to user interaction.
#############################  


import math
import pygame
import collisions
import positions
import ballClass
import graphics
import text
import startScreen 
import endScreen

import socket
import threading
from queue import Queue
'''
HOST = "" 
PORT = 50003
'''

# Pygame class                   
class Pygame():
    
    # Init function 
    def init(self):
        
        # Pygame sound effects
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_mode()    
        self.cueStrike = pygame.mixer.Sound("cueStrike.wav")
        self.hitHole = pygame.mixer.Sound('hitHole.wav')
        self.countDown = pygame.mixer.Sound('timer.wav')
        self.countDownIsPlaying = False
        
        # Initialize gameboard and sprite groups
        self.boardWidth = self.width-2*self.margin
        self.boardHeight = self.height-3*self.margin
        self.gameboard = graphics.Gameboard(self.margin, self.margin, \
                                   self.boardWidth, self.boardHeight)
        self.ballGroup = pygame.sprite.Group() 
        self.holeGroup = pygame.sprite.Group()
        self.solidDraw = pygame.sprite.Group()
        self.stripedDraw = pygame.sprite.Group()
        self.whiteDraw = pygame.sprite.Group()
        self.blackDraw = pygame.sprite.Group()
        
        # Initialize borders
        self.border = graphics.Border(self.width, \
                      self.height, self.margin, self.boardHeight)
        
        
        # Add holes to sprite group
        listPos = positions.holePositions(self.margin, \
        graphics.Border.innerMargin, self.boardWidth, self.boardHeight)           
        for pos in listPos:
            self.holeGroup.add(graphics.Hole(pos[0], pos[1]))
        
        
        # Set up initial positions of colored balls
        ballPos = positions.ballStartPositions(self.width, \
                                             self.margin, self.height)

 
        # Add striped and solid balls to sprte group
        self.ballGroup = ballClass.initialPos(self.ballGroup, \
        self.width, self.margin, self.height, ballPos)
              
                     
        # Initialize black ball
        self.ballGroup.add(ballClass.blackBall(ballPos[4][0], \
                ballPos[4][1], (0, 0, 0), '8'))

      
        # Initialize white ball                       
        whiteX = self.width/4
        whiteY = (self.height-self.margin)/2 
        self.whiteBall = ballClass.whiteBall(whiteX, whiteY, \
                                            (255, 255, 255), None)
        self.ballGroup.add(self.whiteBall)
        
        # Bool value for drawing gray shadows on balls not of player's type
        self.drawgray = True 
        
        
        # Initialize mouse drag, press, motion boolean vales
        self.hasHit = False
        self.hasPressed = False
        self.cueStriking = False
        self.showGuideLines = True
        self.dragWhiteBall = False
        self.whiteOnPress = False
        self.startCheck = False
        self.maxDrag = False
        self.forceApplied = 0
        self.hintOn = False
        
        # Initialize cue stick
        self.xCue = 0
        self.yCue = 0
        self.cueSpeed = 30
        listPos = self.cuePositionNotPressed()
        self.cue = graphics.Cue(listPos[0], listPos[1], listPos[2], listPos[3])
        self.minForceApplied = self.cue.distanceFromWhite * 0.3
        
        # Initialize guideLines
        listPosLines = self.guideLinesPos()
        self.guideLines = graphics.GuideLines(listPosLines[0], listPosLines[1],\
                          self.angle)
        
        # Maximum allowed force 
        self.maxApplied = 100
        
        # Initialize player character text
        self.player1 = None
        self.player2 = None
        self.firstHoleHit = False
        
        # Timer per player move
        self.timer = True
        self.firstCheck = True
        self.maxTime = 20
        
        # Hint button color
        self.hintCol = (51, 153, 255)
        self.hint2Col = (51, 153, 255)
        self.hint2On = False
        
  
    # Return guide lines position
    def guideLinesPos(self):
        return positions.guideLinePosition(self.angle, self.xCue, \
               self.yCue, self.whiteBall.rect.centerx,\
               self.whiteBall.rect.centery, graphics.Cue.distanceFromWhite)
        
        
    # Return cue position
    def cuePositionNotPressed(self):
        
        # Return the angle of the cue stick and white ball
        self.angle = positions.cueAngle(self.xCue, self.yCue, \
                     self.whiteBall.rect.centerx, self.whiteBall.rect.centery)
                     
        # Call function cuePosition in positions with self value parameters
        return positions.cuePosition(self.angle, self.xCue, self.yCue, \
                self.whiteBall.rect.centerx, self.whiteBall.rect.centery, \
                graphics.Cue.distanceFromWhite, graphics.Cue.length)
                
            
    # Keep track of orginal curser positions when mouse is pressed
    def mousePressed(self):
        # Only responds to mouse presses when the cue hasn't stroke the ball 
        if self.hasHit == False and self.dragWhiteBall == False:
            self.hasPressed = True    # hasPressed condition turns on
            self.xDragInitial = pygame.mouse.get_pos()[0]
            self.yDragInitial = pygame.mouse.get_pos()[1]
            self.x1CueInitial = self.cue.x1
            self.x2CueInitial = self.cue.x2
            self.y1CueInitial = self.cue.y1
            self.y2CueInitial = self.cue.y2
        
        # Check to see if clicked on hint button  
        if self.hintOn == True:
            xhit = pygame.mouse.get_pos()[0]
            yhit = pygame.mouse.get_pos()[1]
            pos = text.hintPos1(self.width, self.height, self.margin)
            pos2 = text.hintPos2(self.width, self.height, self.margin)
            
            if text.clickHint(xhit, yhit, pos):
                self.drawgray = True
            if text.clickHint(xhit, yhit, pos2):
                self.hint2On = True
                  
            self.hasPressed = False


        
        # Get position of white ball when mouse is pressed while dragging white    
        if self.dragWhiteBall:
            
            # Check if white ball is placed within correct bounds
            if positions.boundsForWhite(self.margin, \
                                        self.boardWidth, self.boardHeight):
                self.whiteBall.rect.centerx = pygame.mouse.get_pos()[0]
                self.whiteBall.rect.centery = pygame.mouse.get_pos()[1]
                self.whiteOnPress = True
                
                msg = 'whiteFixed %d %d\n' % (self.whiteBall.rect.centerx, \
                self.whiteBall.rect.centery)
                self.server.send(msg.encode())
            

    
    # Cue stick strikes when mouse is released
    def mouseReleased(self):
        # Released for cue strike and minimum force is applied
        if not self.dragWhiteBall and self.forceApplied > self.minForceApplied:
        
            # Change cue movement: begins to move and strike
            self.cueStriking = True
            self.hasPressed = False
            
            # Change timer conditions
            self.timer = False
            self.firstCheck = True
            if self.countDownIsPlaying:
                self.countDown.stop()
                self.countDownIsPlaying = False
            
            msg = 'cueReleased\n'
            self.server.send(msg.encode())

        
        # Released for white ball placement        
        if self.dragWhiteBall:

            # Check if white ball is placed within correct bounds
            if positions.boundsForWhite(self.margin, \
                                        self.boardWidth, self.boardHeight):
                self.whiteOnPress = False
                self.dragWhiteBall = False
                self.hint2On = False
                self.whiteBall.holeViolation = False
                
                # Change timer conditions
                self.timer = True
                self.firstCheck = True
                if self.countDownIsPlaying:
                    self.countDown.stop()
                    self.countDownIsPlaying = False
                    
                msg = 'whiteBallBounds\n'
                self.server.send(msg.encode())

        

    # A cue stick follows the cursor position when no balls are moving on board
    def mouseMotion(self):

        # Motion turns on when mouse hasn't been pressed and cue hasn't striken
        if self.hasHit == False and self.hasPressed == False and \
        self.dragWhiteBall == False:
            self.hintOn = True   # Draw gray on non player type ball
            self.xCue = pygame.mouse.get_pos()[0]
            self.yCue = pygame.mouse.get_pos()[1]
            listPos = self.cuePositionNotPressed()
            self.cue = graphics.Cue(listPos[0], listPos[1], listPos[2], \
                                    listPos[3])
            listPosLines = self.guideLinesPos()
            self.guideLines = graphics.GuideLines(listPosLines[0], \
                              listPosLines[1],self.angle) 
                              
            msg = 'cue %f %f %f %f %f %f %f\n' % (listPos[0], \
            listPos[1], listPos[2], listPos[3], listPosLines[0], \
            listPosLines[1], self.angle)
            self.server.send(msg.encode())
                                               
         
        # Mouse motion for puting down white ball
        if self.dragWhiteBall and not self.whiteOnPress:
            self.whiteBall.rect.centerx = pygame.mouse.get_pos()[0]
            self.whiteBall.rect.centery = pygame.mouse.get_pos()[1]
            
            msg = 'placeWhite %d %d\n' % (self.whiteBall.rect.centerx,\
            self.whiteBall.rect.centery)
            self.server.send(msg.encode())
            
        # If cursor above button, button changes color   
        if self.hintOn == True:
            xhit = pygame.mouse.get_pos()[0]
            yhit = pygame.mouse.get_pos()[1]
            pos = text.hintPos1(self.width, self.height, self.margin)
            pos2 = text.hintPos2(self.width, self.height, self.margin)
            if text.clickHint(xhit, yhit, pos):
                self.hintCol = (204, 229, 255)
            else:
                self.hintCol = (51, 153, 255)
                
            if text.clickHint(xhit, yhit, pos2):
                self.hint2Col = (204, 229, 255)
            else:
                self.hint2Col = (51, 153, 255)
                
                
                
                

    # cue stick moves according to the mouse drag distance to strike the ball        
    def mouseDrag(self):
        self.hasPressed = True
        self.hintOn = False
        self.drawgray = False    # Remove gray color for non-type balls
        self.showGuideLines = False
        self.hint2On = False
            
        if self.hasHit == False:
            self.xDrag = pygame.mouse.get_pos()[0]
            self.yDrag = pygame.mouse.get_pos()[1]
            dragX1Dist = self.xDrag - self.xDragInitial
            dragY1Dist = self.yDrag - self.yDragInitial
            dragDist = (dragX1Dist**2 + dragY1Dist**2)**0.5
            cuePosToWhiteX = self.x1CueInitial - self.whiteBall.rect.centerx
            cuePosToWhiteY = self.y1CueInitial - self.whiteBall.rect.centery
            
            distX = self.cue.x1 - self.whiteBall.rect.centerx
            distY = self.cue.y1 - self.whiteBall.rect.centery
            # force of cue stick depends on its distance from the whiteBall
            self.forceApplied = (distX**2+distY**2)**0.5 * 0.35
            if self.forceApplied > self.maxApplied:
                self.forceApplied = self.maxApplied
                self.maxDrag = True
            else:
                self.maxDrag = False

            
            # Make sure the mouse drags in same direction as cue stick
            if dragX1Dist * cuePosToWhiteX >= 0 and \
            dragY1Dist * cuePosToWhiteY >= 0 and not self.maxDrag:
                self.cue.x1 = self.x1CueInitial + dragDist*math.cos(self.angle)
                self.cue.x2 = self.x2CueInitial + dragDist*math.cos(self.angle)
                self.cue.y1 = self.y1CueInitial - dragDist*math.sin(self.angle)
                self.cue.y2 = self.y2CueInitial - dragDist*math.sin(self.angle)
                
            msg = 'drag %f %f %f %f %f\n' % (self.cue.x1, \
            self.cue.x2, self.cue.y1, self.cue.y2, self.forceApplied)
                
            self.server.send(msg.encode())
                    
   
    
    # Timerfired function    
    def timerFired(self, dt):
        
        # Check if ball falls into holes
        for hole in self.holeGroup:
            for ball in self.ballGroup:
                dist = collisions.distance(hole.rect.x, hole.rect.y, \
                                           ball.rect.x, ball.rect.y)
                
                # Ball falls into hole if slightly overlaps with hole
                if dist <= (hole.radius + ballClass.Ball.radius)*3/5 or \
                ball.rect.x  < self.margin \
                or ball.rect.x > self.boardWidth + self.margin \
                or ball.rect.y < self.margin or \
                ball.rect.y > self.boardHeight + self.margin:
                    
                    if not self.dragWhiteBall:
                        self.hitHole.play()
                    
                    # Check whether this is first ball in hole
                    if not self.firstHoleHit and ball.color != (255, 255, 255):
                        
                        # This loop only operates once
                        self.firstHoleHit = True   
                        
                        # Match player with their ball type
                        if (type(ball) == ballClass.Ball) and self.display1 or \
                        type(ball) != ballClass.Ball and not self.display1:
                            self.player1 = text.Player('solid', 1, \
                                                        self.player1Name,[])
                            self.player2 = text.Player('striped', 2, \
                                                        self.player2Name,[])
                            
                        elif type(ball) != ballClass.Ball and self.display1 or \
                        type(ball) == ballClass.Ball and not self.display1:
                            self.player1 = text.Player('striped', 1, \
                                                        self.player1Name,[])
                            self.player2 = text.Player('solid', 2, \
                                                        self.player2Name,[])
                    
                    # Add score to player (Player 1 playing)       
                    if self.display1 and ball.color != (255, 255, 255) and \
                    ball.color != (0,0,0):
                        
                        # Check the player strikes the correct ball type
                        if (self.player1.type == 'striped' and \
                        type(ball) != ballClass.Ball) or \
                        (self.player1.type == 'solid' and \
                        type(ball) == ballClass.Ball):                   
                            
                            self.player1.ballList += [[ball.number, ball.color]]
                            # Player continues only if correct ball is stiked
                            text.Player.playerContinue = True
                            
                        # Otherwise add point to opponent    
                        else:
                            self.player2.ballList += [[ball.number, ball.color]]
                            
                            
                    # Add score to player (Player 2 playing)
                    elif not self.display1 and ball.color != (255, 255, 255) \
                    and ball.color != (0, 0, 0):
                        if (self.player2.type == 'striped' and \
                        type(ball) != ballClass.Ball) or \
                        (self.player2.type == 'solid' and \
                        type(ball) == ballClass.Ball):
                        
                            self.player2.ballList += [[ball.number, ball.color]]
                            # Player continues only if correct ball is stiked
                            text.Player.playerContinue = True
                            
                        # Otherwise add point to opponent    
                        else:
                            self.player1.ballList += [[ball.number, ball.color]]

                    # Kill ball if ball is not white      
                    if ball.color != (255, 255, 255) and ball.color != (0,0,0): 
                        ball.kill()
                     
                    # When 8-pool is hit into hole
                    elif ball.color == (0, 0, 0):
                        ball.kill()
                        if (self.currPlayer == "Player1" and self.display1) or\
                        (self.currPlayer == "Player2" and not self.display1):
                            if (self.display1 and len(self.player1.ballList) \
                            == 7) or (not self.display1 and \
                            len(self.player2.ballList)) == 7:
                                msg = 'endMode %s %s %s\n' % (not self.display1, True, False) 
                                self.server.send(msg.encode())
                                endScreen.main(self.player1Name, \
                                self.player2Name, self.display1, True, True)
                            else:
                                msg = 'endMode %s %s %s\n' % (not self.display1, False, True)
                                self.server.send(msg.encode())
                                endScreen.main(self.player1Name, \
                                self.player2Name, self.display1, False, False)

 
                    # Rule violation if white ball falls into hole    
                    elif ball.color == (255, 255, 255):
                        self.whiteBall.holeViolation = True
                        self.xSpeed = 0
                        self.ySpeed =0


        # Check collisions with balls, change speed and direction if necessary,
        # update ball position
        self.ballGroup.update(self.ballGroup, self.holeGroup, \
        self.gameboard.friction, self.dragWhiteBall, \
        self.margin, self.boardHeight, self.boardWidth)
        
        
        # Check for collisions with borders
        collisions.collideBorder(self.ballGroup, self.margin, \
        self.boardHeight, self.boardWidth)
        
        
        # Only update cue movement when mouse is released 
        # and cue is stiking the ball
        if self.cueStriking:
            self.cue.x1 -= self.cueSpeed*math.cos(self.angle)
            self.cue.y1 += self.cueSpeed*math.sin(self.angle)
            self.cue.x2 -= self.cueSpeed*math.cos(self.angle)
            self.cue.y2 += self.cueSpeed*math.sin(self.angle)

            # Check whether cue has striked the whiteball
            if collisions.distance(self.cue.x1, self.cue.y1, self.whiteBall.\
            rect.centerx, self.whiteBall.rect.centery) <= ballClass.Ball.radius:
                # Adjust volume of cue strike based on size of force applied
                self.cueStrike.set_volume(self.forceApplied/self.maxApplied)
                self.cueStrike.play()
                
                self.whiteBall.xSpeed = -self.forceApplied*math.cos(self.angle)
                self.whiteBall.ySpeed = self.forceApplied*math.sin(self.angle)

                # Cue stick disappears
                self.hasHit = True
                self.cueStriking = False
                self.showGuideLines = True
                self.startCheck = True
                self.forceApplied = 0
                
        # Check if there is still moving balls after cue strike:
        # If none, then next player's turn
        if self.startCheck: 

            # Check if all balls have stopped moving
            numMoving = 0
            for ball in self.ballGroup:
                if ball.xSpeed != 0 and ball.ySpeed != 0:
                    numMoving += 1
            
            if numMoving  == 0:
                self.timer = True
                
                # If so, cue stick reappears
                self.hasHit = False
                self.startCheck = False
                if text.Player.playerContinue == False:
                    self.display1 = not self.display1
                text.Player.playerContinue = False

                # If white hits hole or misses balls then mouse controls white
                if self.whiteBall.violation or self.whiteBall.holeViolation:
                    self.dragWhiteBall = True 
                    self.hint2On = True
                
                
                # Include this so cue appears at depending on current position 
                # of the cursor instead of its last position before strike    
                if self.hasHit == False and self.hasPressed == False:
                    listPos = self.cuePositionNotPressed()
                    self.cue = graphics.Cue(listPos[0], listPos[1], listPos[2],\
                                            listPos[3])
                    linesPos = self.guideLinesPos()
                    self.guideLines = graphics.GuideLines(linesPos[0], \
                                                        linesPos[1], self.angle)                        
                
                
                self.whiteBall.violation = True
                self.whiteBall.holeViolation = False

            # Balls are still coliding. No move should be played yet
            else:
                self.hasHit = True
        

        #and ((self.display1 and self.currPlayer == 'Player1') \
        # or (not self.display1 and self.currPlayer == 'Player2'))                   
    
    # Draw and update the game board    
    def redrawAll(self, screen):
        self.gameboard.draw(screen)
        self.border.draw(screen)
        self.holeGroup.draw(screen)
        text.hintBox(screen, self.width, self.height, self.margin, self.hintCol)
        self.ballGroup.draw(screen)
        text.hintBox2(screen, self.width, self.height, self.margin, \
        self.hint2Col)
        
        if self.hint2On:
            collisions.drawAllLines(screen, self.ballGroup, self.player1, \
            self.player2, self.display1, self.whiteBall.rect.centerx,\
            self.whiteBall.rect.centery, self.holeGroup, self.boardWidth, \
            self.margin, self.boardHeight)

        # Doesn't draw cue when balls are still moving
        if self.hasHit == False and self.dragWhiteBall == False:
            self.cue.draw(screen)
        
        if self.player1 != None:
            # Draw gray on balls if not the current player's type during move      
            if self.hasHit == False and self.dragWhiteBall == False and \
            self.drawgray:
                # Current player's move
                if (self.currPlayer == "Player1" and self.display1) or \
                (self.currPlayer == 'Player2' and not self.display1):
                    # Draw solid shade striped
                    if (self.display1 and self.player1.type == 'solid') or\
                    (not self.display1 and self.player2.type == 'solid'):
                        ballClass.grayShade(screen, self.ballGroup, \
                        self.solidDraw,self.stripedDraw, self.whiteDraw,\
                        self.blackDraw, 'solid')
                        
                    # Draw striped shade solid
                    elif (self.display1 and self.player1.type == 'striped') or\
                    (not self.display1 and self.player2.type == 'striped'):
                            
                        ballClass.grayShade(screen, self.ballGroup, \
                        self.solidDraw, self.stripedDraw, self.whiteDraw, \
                        self.blackDraw, 'striped') 
                        
                    ballClass.Ball.white = (255, 255, 255)
                    self.solidDraw = pygame.sprite.Group()
                    self.stripedDraw = pygame.sprite.Group() 
                    self.whiteDraw = pygame.sprite.Group()
                    self.blackDraw = pygame.sprite.Group()
                    
                else:
                    self.ballGroup.draw(screen)     
        
        
        if self.showGuideLines and not self.hasHit and not self.dragWhiteBall:
            self.guideLines.draw(screen)
            
        # If whiteball has fallen into holes and is being dragged
        if self.dragWhiteBall:
            x = self.whiteBall.rect.centerx
            y = self.whiteBall.rect.centery
            r = ballClass.Ball.radius
            pygame.draw.circle(screen, (255, 255, 255), (x, y), r, 0)

        # Show force font
        text.forceText(screen, self.width, self.margin, \
        self.boardHeight, self.boardWidth, self.forceApplied, self.maxApplied)
            
         
        # If no player has hit a ball yet
        if self.player1 == None:
            if (self.currPlayer == "Player1" and self.display1) \
            or (self.currPlayer == 'Player2' and not self.display1):
                if self.countDownIsPlaying:
                    text.Player.drawNone(screen, self.width, self.margin, \
                    "Hurry Up!")
                else:
                    text.Player.drawNone(screen, self.width, self.margin, \
                    "Your Turn")                   
               
            # If other player's turn show his/her name
            else:
                if not self.display1:
                    text.Player.drawNone(screen, self.width, self.margin, \
                    '%s\'s turn' % self.player2Name)
                else:
                    text.Player.drawNone(screen, self.width, self.margin, \
                    '%s\'s turn' % self.player1Name)

            # Empty score at bottom
            self.font = pygame.font.Font('cmunti.ttf', 15)
            text1 = self.font.render(self.player1Name, True, (0, 0, 0))
            screen.blit(text1, (self.margin, self.boardHeight + self.margin))
            text2 = self.font.render(self.player2Name, True, (0, 0, 0))
            screen.blit(text2, (self.margin, self.boardHeight + 2*self.margin))
            
            
       # If a ball has been hit and player has a ball type
        else:                       
            if not self.countDownIsPlaying:
                # Show 'Your turn' if current player's turn
                if self.currPlayer == "Player1" and self.display1:
                    self.player1.currTurn(screen, self.width, self.margin)
                elif self.currPlayer == 'Player2' and not self.display1:
                    self.player2.currTurn(screen, self.width, self.margin)
                # Otherwise display opponent's name when not your turn
                else:
                    if self.display1:
                        self.player1.draw(screen, self.width, self.margin) 
                    else:
                        self.player2.draw(screen, self.width, self.margin) 
                        
            # If time is running out
            else:
                # Notify the current player
                if (self.currPlayer == "Player1" and self.display1) \
                or (self.currPlayer == 'Player2' and not self.display1):
                    text.Player.drawNone(screen, self.width, self.margin, \
                    "Hurry Up!")
                else:
                    if self.display1:
                        self.player1.draw(screen, self.width, self.margin) 
                    else:
                        self.player2.draw(screen, self.width, self.margin) 
                    
                    
                
            # Draws the score down at bottom
            self.player1.drawScore(screen, self.margin, \
                                   self.boardHeight, self.boardWidth)
            self.player2.drawScore(screen, self.margin, \
                                   self.boardHeight, self.boardWidth)
                                  
        # Show time remaining bar
        if self.timer:
            text.timebar(screen, self.countDownIsPlaying, self.margin, \
            self.boardWidth, self.boardHeight, self.maxTime, self.seconds)  
                
                
    # init values of the Pygame class
    def __init__(self, width=1000, height=640, fps=50, title="112 Pool Game"):
        self.width = width
        self.height = height
        self.margin = 40
        self.fps = fps
        self.title = title
        self.bgColor = 	(230, 230, 250)    # Lavendar
        pygame.init()

           
    # Run main function    
    def run(self, name1, name2, bool, serverMsg=None, server=None):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        self.player1Name = name1
        self.player2Name = name2
        self.serverMsg = serverMsg
        self.server = server
        self.amPlay1 = bool
        playing = True
        while playing:
            time = clock.tick(self.fps)
            
            # Set timer per player
            if self.timer:
                if self.firstCheck:
                    startTicks = pygame.time.get_ticks()
                    self.firstCheck = False
                self.seconds = (pygame.time.get_ticks()-startTicks)/1000
                
                # Play count down noise when player time is running out
                if self.maxTime - self.seconds <= 5:
                    self.countDown.play()
                    self.countDownIsPlaying = True
                    
                # Switch to next player if max time is exceeded
                if self.maxTime - self.seconds <= 0:
                    self.timer = False
                    self.firstCheck = True
                    self.display1 = not self.display1
                    self.dragWhiteBall = True
                    self.hint2On = True
                    self.countDownIsPlaying = False
                    self.countDown.stop()
                
            
            # Update current board state in accordance with the other player
            while (self.serverMsg.qsize() > 0):
                msg = self.serverMsg.get(False)
                print("received: ", msg, "\n")
                msg = msg.split()
                command = msg[0]     # Instruction
                
                # Player 1 always plays first
                if command == 'newPlayer':
                    if self.amPlay1:  
                        self.currPlayer = 'Player1'
                        self.display1 = True
                    else:
                        self.currPlayer = 'Player2'
                        self.display1 = True
                        
                    # currPlayer doesn't switch during first strike
                    self.firstMove = True    
                
                # Command for cue stick motion 
                if command == "cue":
                    if not self.firstMove:
                        self.currPlayer = msg[1]
                    cuex1 = float(msg[2])
                    cuey1 = float(msg[3])
                    cuex2 = float(msg[4])
                    cuey2 = float(msg[5])
                    linex = float(msg[6])
                    liney = float(msg[7])
                    angle = float(msg[8])
                    self.firstMove = True
                    self.guideLines = graphics.GuideLines(linex, liney, angle)
                    self.cue = graphics.Cue(cuex1, cuey1, cuex2, cuey2)
                    self.angle = angle
            
                # Command for cue stick currently being dragged    
                elif command == 'drag':
                    if not self.firstMove:
                        self.currPlayer = msg[1]
                    cuex1 = float(msg[2])
                    cuey1 = float(msg[4])
                    cuex2 = float(msg[3])
                    cuey2 = float(msg[5])
                    forceApplied = float(msg[6])
                    self.firstMove = True
                    
                    self.cue = graphics.Cue(cuex1, cuey1, cuex2, cuey2)
                    self.forceApplied = forceApplied
                    self.hasPressed = True
                    self.hint2On = False
                
                # Command for releasing the cue stick    
                elif command == "cueReleased":
                    self.cueStriking = True
                    self.hasPressed = False
                    self.timer = False
                    self.firstCheck = True
                    if self.countDownIsPlaying:
                        self.countDown.stop()
                        self.countDownIsPlaying = False
                
                # Command for checking the correct bounds placement of whiteball    
                elif command == 'whiteBallBounds':
                    self.whiteOnPress = False
                    self.dragWhiteBall = False
                    self.hint2On = False
                    self.timer = True
                    self.firstCheck = True
                    if self.countDownIsPlaying:
                        self.countDown.stop()
                        self.countDownIsPlaying = False
                    self.whiteBall.holeViolation = False
                
                # Command for moving white ball after illegal hit
                elif command == 'placeWhite':
                    self.whiteBall.rect.centerx = float(msg[2])
                    self.whiteBall.rect.centery = float(msg[3])
                     
                # Command for placing the white ball
                elif command == 'whiteFixed':
                    self.whiteBall.rect.centerx = float(msg[2])
                    self.whiteBall.rect.centery = float(msg[3])
                    self.whiteOnPress = True
                
                # Command for running endScreen
                elif command == 'endMode':
                    if msg[2] == str(True):
                        bool1 = True
                    elif msg[2] == str(False):
                        bool1 = False
                        
                    if msg[3] == str(True):
                        bool = True
                    elif msg[3] == str(False):
                        bool = False
                        
                    if msg[4] == str(True):
                        win = True
                    elif msg[4] == str(False):
                        win = False
                    endScreen.main(self.player1Name, self.player2Name, \
                    bool1, bool, win)
                    
                serverMsg.task_done() 
                  
            self.timerFired(time)
                    

            for event in pygame.event.get():
                # Make sure player cannot control board when not his own turn
                if (self.currPlayer == "Player1" and self.display1) or \
                (self.currPlayer == "Player2" and not self.display1) \
                or self.cueStriking:
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        self.mouseReleased()
                    elif (event.type == pygame.MOUSEMOTION and
                        event.buttons == (0, 0, 0)):
                        self.mouseMotion()
                    elif event.type == pygame.MOUSEBUTTONDOWN and \
                    event.button == 1:
                        self.mousePressed()
                    elif (event.type == pygame.MOUSEMOTION and
                    event.buttons[0] == 1):
                        self.mouseDrag()

                if event.type == pygame.QUIT:
                    playing = False
                
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()
        

# Set up for socket module        
def main(name1, name2, bool):
    
    def handleServerMsg(server, serverMsg):
        server.setblocking(1)
        msg = ""
        command = ""
        while True:
            msg += server.recv(10).decode()
            command = msg.split("\n")
            while (len(command) > 1):
                readyMsg = command[0]
                msg = "\n".join(command[1:])
                serverMsg.put(readyMsg)
                command = msg.split("\n")
    HOST = '127.0.0.1'
    PORT = 50001
        
        
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    server.connect((HOST,PORT))
    
    print("connected to server")
    serverMsg = Queue(100)
        

    threading.Thread(target = handleServerMsg, args = \
    (server, serverMsg)).start()
    Pygame().run(name1, name2, bool, serverMsg, server)


    