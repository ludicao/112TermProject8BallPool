import math
import pygame
import collisions
import positions
import ballClass
import graphics
import text
import startScreen 
import endScreen

# Pygame class                   
class Pygame():
    
    # Init function 
    def init(self):
        
        # Initialize gameboard and sprite groups
        self.boardWidth = self.width-2*self.margin
        self.boardHeight = self.height-3*self.margin
        self.gameboard = graphics.Gameboard(self.margin, self.margin, \
                                   self.boardWidth, self.boardHeight)
        self.ballGroup = pygame.sprite.Group() 
        self.holeGroup = pygame.sprite.Group()
        
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
        ballColor = ballClass.Ball.colorList()
        ballType = ballClass.Ball.ballType()
        ballNum = ballClass.Ball.ballNumber()
        
        for i in range(4):  
            if ballType[i] == True:
                self.ballGroup.add(ballClass.Ball(ballPos[i][0], \
                ballPos[i][1], ballColor[i], str(ballNum[i])))
            else:
                self.ballGroup.add(ballClass.stripedBalls(ballPos[i][0], \
                ballPos[i][1], ballColor[i], str(ballNum[i])))
                
        for i in range(4, len(ballPos)-1):
            if ballType[i] == True:
                self.ballGroup.add(ballClass.Ball(ballPos[i+1][0], \
                ballPos[i+1][1], ballColor[i], str(ballNum[i])))
            else:
                self.ballGroup.add(ballClass.stripedBalls(ballPos[i+1][0], \
                ballPos[i+1][1], ballColor[i], str(ballNum[i])))
            

        # Initialize black ball
        self.ballGroup.add(ballClass.blackBall(ballPos[4][0], \
                ballPos[4][1], (0, 0, 0), '8'))
            
            
        # Initialize white ball                       
        whiteX = self.width/4
        whiteY = (self.height-self.margin)/2 
        self.whiteBall = ballClass.whiteBall(whiteX, whiteY, \
                                            (255, 255, 255), None)
        self.ballGroup.add(self.whiteBall)
        
        
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
        
        # Initialize cue stick
        self.xCue = 0
        self.yCue = 0
        self.cueSpeed = 30
        listPos = self.cuePositionNotPressed()
        self.cue = graphics.Cue(listPos[0], listPos[1], listPos[2], listPos[3])
        self.minForceApplied = self.cue.distanceFromWhite * 0.4
        
        # Initialize guideLines
        listPosLines = self.guideLinesPos()
        self.guideLines = graphics.GuideLines(listPosLines[0], listPosLines[1],\
                          self.angle)
  
        # Initialize player character text
        self.display1 = True
        self.player1 = None
        self.player2 = None
        self.firstHoleHit = False
        
        # Maximum allowed force 
        self.maxApplied = 100
        
  
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
        
        # Get position of white ball when mouse is pressed while dragging white    
        if self.dragWhiteBall:
            
            # Check if white ball is placed within correct bounds
            if positions.boundsForWhite(self.margin, \
                                        self.boardWidth, self.boardHeight):
                self.whiteBall.rect.centerx = pygame.mouse.get_pos()[0]
                self.whiteBall.rect.centery = pygame.mouse.get_pos()[1]
                self.whiteOnPress = True
            

    
    # Cue stick strikes when mouse is released
    def mouseReleased(self):
        # Released for cue strike and minimum force is applied
        if not self.dragWhiteBall and self.forceApplied > self.minForceApplied:
        
            # bool vales switch
            self.cueStriking = True
            self.hasPressed = False

        
        # Released for white ball placement        
        if self.dragWhiteBall:

            # Check if white ball is placed within correct bounds
            if positions.boundsForWhite(self.margin, \
                                        self.boardWidth, self.boardHeight):
                self.whiteOnPress = False
                self.dragWhiteBall = False

        

    # A cue stick follows the cursor position when no balls are moving on board
    def mouseMotion(self):

        # Motion turns on when mouse hasn't been pressed and cue hasn't striken
        if self.hasHit == False and self.hasPressed == False and \
        self.dragWhiteBall == False:
            self.xCue = pygame.mouse.get_pos()[0]
            self.yCue = pygame.mouse.get_pos()[1]
            listPos = self.cuePositionNotPressed()
            self.cue = graphics.Cue(listPos[0], listPos[1], listPos[2], \
                                    listPos[3])
            listPosLines = self.guideLinesPos()
            self.guideLines = graphics.GuideLines(listPosLines[0], \
                              listPosLines[1],self.angle) 
         
        # Mouse motion for puting down white ball
        if self.dragWhiteBall and not self.whiteOnPress:
            self.whiteBall.rect.centerx = pygame.mouse.get_pos()[0]
            self.whiteBall.rect.centery = pygame.mouse.get_pos()[1]
            

    # cue stick moves according to the mouse drag distance to strike the ball        
    def mouseDrag(self):
        self.hasPressed = True
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
            self.forceApplied = (distX**2+distY**2)**0.5 * 0.4
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
                    
   
    
    # Timerfired function    
    def timerFired(self, dt):
        
        # Check if ball falls into holes
        for hole in self.holeGroup:
            for ball in self.ballGroup:
                dist = collisions.distance(hole.rect.x, hole.rect.y, \
                                           ball.rect.x, ball.rect.y)
                
                # Ball falls into hole if slightly overlaps with hole
                if dist <= (hole.radius + ballClass.Ball.radius)*3/5:
                    
                    # Check whether this is first ball in hole
                    if not self.firstHoleHit:
                        
                        # This loop only operates once
                        self.firstHoleHit = True   
                        
                        # Match player with their ball type
                        if (type(ball) == ballClass.Ball) and self.display1 or \
                        type(ball) != ballClass.Ball and not self.display1:
                            self.player1 = text.Player('solid', 1, [])
                            self.player2 = text.Player('striped', 2, [])
                            
                        elif type(ball) != ballClass.Ball and self.display1 or \
                        type(ball) == ballClass.Ball and not self.display1:
                            self.player1 = text.Player('striped', 1, [])
                            self.player2 = text.Player('solid', 2, [])
                    
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
                        # Player wins
                        if (self.display1 and len(self.player1.ballList) == 7) \
                        or (not self.display1 and len(self.player2.ballList)) \
                        == 7:
                            ball.kill()
                            endMode = endScreen.endScreen(self.display1, True)                        
                            endMode.run()
                            
                        # Illegal situation: opponent automatically wins
                        else :
                            ball.kill()
                            endMode = endScreen.endScreen(self.display1, False)
                            endMode.run()
                            
                            
                    
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
                # If so, cue stick reappears
                self.hasHit = False
                self.startCheck = False
                if text.Player.playerContinue == False:
                    self.display1 = not self.display1
                text.Player.playerContinue = False

                # If white hits hole or misses balls then mouse controls white
                if self.whiteBall.violation or self.whiteBall.holeViolation:
                    self.dragWhiteBall = True 
                    
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
        

                       
    
    # Draw and update the game board    
    def redrawAll(self, screen):
        self.gameboard.draw(screen)
        self.border.draw(screen)
        self.holeGroup.draw(screen)
        self.ballGroup.draw(screen)
        
        # Doesn't draw cue when balls are still moving
        if self.hasHit == False and self.dragWhiteBall == False:
            self.cue.draw(screen)
        if self.showGuideLines and not self.hasHit and not self.dragWhiteBall:
            self.guideLines.draw(screen)
            
        # If whiteball has fallen into holes and is being dragged
        if self.dragWhiteBall:
            x = self.whiteBall.rect.centerx
            y = self.whiteBall.rect.centery
            r = ballClass.Ball.radius
            pygame.draw.circle(screen, (255, 255, 255), (x, y), r, 0)

        # Show force font
        font = pygame.font.Font('cmunti.ttf', 20)
        textForce = font.render('Force: ', True, (0, 0, 0))
        startForceX = self.width/5*3
        startForceY = 1.5*self.margin+self.boardHeight
        screen.blit(textForce, (startForceX, startForceY))
        barWidth = self.boardWidth/6
        barHeight = self.margin
        width = self.forceApplied/self.maxApplied * barWidth
        pygame.draw.rect(screen, (204, 0, 102), \
                        (startForceX + 70, startForceY, width, barHeight), 0)
         
        # If no player has hit a ball yet
        if self.player1 == None:
            if self.display1:
                text.Player.drawNone(screen, self.width, self.margin, True)
            else:
                text.Player.drawNone(screen, self.width, self.margin, False)
            self.font = pygame.font.Font('cmunti.ttf', 15)
            text1 = self.font.render('Player 1:', True, (0, 0, 0))
            screen.blit(text1, (self.margin, self.boardHeight + self.margin))
            text2 = self.font.render('Player 2:', True, (0, 0, 0))
            screen.blit(text2, (self.margin, self.boardHeight + 2*self.margin))
            
       # If a ball has been hit and player has a ball type
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
                
        
        
    # init values of the Pygame class
    def __init__(self, width=1000, height=640, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.margin = 40
        self.fps = fps
        self.title = title
        self.bgColor = 	(230, 230, 250)    # Lavendar
        pygame.init()

           
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
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased()
                elif event.type == pygame.QUIT:
                    playing = False
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed()
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag()
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()


# Run the game
def main():
    startMode = startScreen.startScreen()
    startMode.run()

if __name__ == '__main__':
    main()
    
            
                    

            
                
                
        
        
        
    