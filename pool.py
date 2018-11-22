import math
import pygame
import collisions
import positions
import ballClass
import graphics
import text


# Pygame class                   
class Pygame():
    
    # Init function 
    def init(self):
        
        # Initialize gameboard and sprite groups
        self.xStart = self.margin
        self.yStart = self.margin
        self.boardWidth = self.width-2*self.margin
        self.boardHeight = self.height-2*self.margin
        self.gameboard = graphics.Gameboard(self.xStart, self.yStart, \
                                   self.boardWidth, self.boardHeight)
        self.ballGroup = pygame.sprite.Group() 
        self.holeGroup = pygame.sprite.Group()
        
        
        # Add holes to sprite group
        xFirstCol = self.margin + graphics.Hole.radius
        xSecondCol = self.boardWidth/2 + self.margin
        xThirdCol = self.boardWidth + self.margin - graphics.Hole.radius
        yFirstRow = self.margin + graphics.Hole.radius
        ySecondRow = self.boardHeight + self.margin - graphics.Hole.radius
        
        listPos = [(xFirstCol, yFirstRow), (xSecondCol, yFirstRow), \
                   (xThirdCol, yFirstRow), (xFirstCol, ySecondRow), \
                   (xSecondCol, ySecondRow), (xThirdCol, ySecondRow)]
                   
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
        whiteY = self.height/2 
        self.whiteBall = ballClass.whiteBall(whiteX, whiteY, (255, 255, 255), None)
        self.ballGroup.add(self.whiteBall)
        
        
        # Initialize mouse drag, press, motion boolean vales
        self.hasHit = False
        self.hasPressed = False
        self.cueStriking = False
        self.showGuideLines = True
        self.dragWhiteBall = False
        self.whiteOnPress = False
        self.startCheck = False
        
        # Initialize cue stick
        self.xCue = 0
        self.yCue = 0
        self.cueSpeed = 30
        listPos = self.cuePositionNotPressed()
        self.cue = graphics.Cue(listPos[0], listPos[1], listPos[2], listPos[3])
        
        # Initialize guideLines
        listPosLines = self.guideLinesPos()
        self.guideLines = graphics.GuideLines(listPosLines[0], listPosLines[1],\
                          self.angle)
  
        # Initialize Player1 text
        self.display1 = True
        self.display1Full = None
        self.firstBallJustHit = True
        self.player1 = None
        self.player2 = None
        self.firstHoleHit = False
        
        
  
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
            
        if self.dragWhiteBall:
            self.whiteBall.rect.centerx = pygame.mouse.get_pos()[0]
            self.whiteBall.rect.centery = pygame.mouse.get_pos()[1]
            self.whiteOnPress = True
            

    
    # Cue stick strikes when mouse is released
    def mouseReleased(self):
        if not self.dragWhiteBall:
            distX = self.cue.x1 - self.whiteBall.rect.centerx
            distY = self.cue.y1 - self.whiteBall.rect.centery
            # force of cue stick depends on its distance from the whiteBall
            self.forceApplied = (distX**2+distY**2)**0.5 * 0.4
            
            # bool vales switch
            self.cueStriking = True
            self.hasPressed = False

                
        if self.dragWhiteBall:
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
            
            # Make sure the mouse drags in same direction as cue stick
            if dragX1Dist * cuePosToWhiteX >= 0 and \
            dragY1Dist * cuePosToWhiteY >= 0:
                self.cue.x1 = self.x1CueInitial + dragDist*math.cos(self.angle)
                self.cue.x2 = self.x2CueInitial + dragDist*math.cos(self.angle)
                self.cue.y1 = self.y1CueInitial - dragDist*math.sin(self.angle)
                self.cue.y2 = self.y2CueInitial - dragDist*math.sin(self.angle)
                    
   
    
    # Timerfired function    
    def timerFired(self, dt):
        
        # Update ball group
        self.ballGroup.update(self.ballGroup, self.holeGroup, \
        self.gameboard.friction)
        
        if ballClass.Ball.firstHoleHit and self.player1 == None:
            print('here')
            listType = text.checkType(ballClass.Ball.firstSolid, self.display1)
            self.player1 = text.Player(listType[0], 1)
            self.player2 = text.Player(listType[1], 2)
            self.firstHoleHit = False

        
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
                self.display1 = not self.display1

                if self.whiteBall.violation:
                    self.dragWhiteBall = True 
                
                if self.hasHit == False and self.hasPressed == False:
                    listPos = self.cuePositionNotPressed()
                    self.cue = graphics.Cue(listPos[0], listPos[1], listPos[2],\
                                            listPos[3])
                    linesPos = self.guideLinesPos()
                    self.guideLines = graphics.GuideLines(linesPos[0], \
                                                        linesPos[1], self.angle)
                                                        
                self.whiteBall.violation = True

            else:
                self.hasHit = True
        

           
            
    
    # Draw and update the game board    
    def redrawAll(self, screen):
        self.gameboard.draw(screen)
        self.holeGroup.draw(screen)
        self.ballGroup.draw(screen)
        if self.hasHit == False and self.dragWhiteBall == False:
            self.cue.draw(screen)
        if self.showGuideLines and not self.hasHit and not self.dragWhiteBall:
            self.guideLines.draw(screen)
        if self.dragWhiteBall:
            x = self.whiteBall.rect.centerx
            y = self.whiteBall.rect.centery
            r = ballClass.Ball.radius
            pygame.draw.circle(screen, (255, 255, 255), (x, y), r, 0)
            
        if self.player1 == None:
            if self.display1:
                text.Player.drawNone(screen, self.width, self.margin, True)
            else:
                text.Player.drawNone(screen, self.width, self.margin, False)
       
        else:
            if self.display1:
                self.player1.draw(screen, self.width, self.margin) 
            else:
                self.player2.draw(screen, self.width, self.margin)
                
            
        
        
    # init values of the Pygame class
    def __init__(self, width=800, height=600, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.margin = 40
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
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
                if event.type == pygame.KEYDOWN:
                    self.whiteBall.xSpeed = 50
                    self.whiteBall.ySpeed = 0
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
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
            screen.fill((255,255,255))
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()


def main():
    game = Pygame()
    game.run()

if __name__ == '__main__':
    main()
    
            
                    

            
                
                
        
        
        
    