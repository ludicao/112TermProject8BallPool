

# Simple splash screen with Python and Pygame

# --- Press ESCAPE to exit ---

# initialize
import pygame
pygame.init()
pygame.mouse.set_visible(0)

# colours
lightblue = 130, 150, 255
white = 255,255,255
black = 0,0,0
red = 255,0,0
grey = 119,119,119

# background screen
def backGroundScreen(colour):
   '''Setup background screen
   In: colourTUPLE.
   Return: screenOBJ'''
   screen = pygame.display.set_mode((320,240))  
   backgrnd = colour
   screen.fill(backgrnd)
   pygame.display.flip()
   return screen

background = lightblue
screen = backGroundScreen(background)

# Create a font
# When font name = None, Pygame returns a default font
def getFont(name = None, size = 20):
   '''Create a font object'''
   font = pygame.font.Font(name, size)
   return font

# Render the text
def putText(fontOBJ, message = "Test", position = (10,10),
            forecolour = black, backcolour = white):
   '''Create a font object'''
   antialias = True
   text = fontOBJ.render(message, antialias, forecolour, backcolour)
   # Create a rectangle
   textRect = text.get_rect()
   textRect.topleft = position
   # Blit the text
   screen.blit(text, textRect)
   pygame.display.update()


# Create a font and render the header line

headerfont = getFont(None,34)
header = "Ben NanoNote"
position = 10,10
putText(headerfont, header, position, 
	forecolour = red,	
	backcolour = background)

# Now the body text

bodylines = [
	[(140, 80), "Open source software"],
	[(140, 100), "Copyleft schematics"],
	[(140, 120), "Linux"]]
bodyfont = getFont(None, 22)
for line in bodylines:
   position, text = line
   putText(bodyfont, text, position,
           forecolour = white,
	   backcolour = background )

# Now the footer text

footerfont = getFont(None, 18)
footerlines = [
	[(10,200), "This demonstration powered by"],
	[(10,215), "Python and Pygame"]]
for line in footerlines:
    position, text = line
    putText(footerfont, text, position,
	backcolour = background)

# Draw the 'Ben' symbol

linesToDraw = [
	[(20, 80), (120, 80)],
	[(67, 60), (67, 160)],
	[(55, 140), (80, 140)],
	[(67, 80), (20, 160)],
	[(67, 80), (120, 160)]
	]

colour = grey
width = 10
for line in linesToDraw:
    start, end = line
    pygame.draw.line(
  	screen, colour, start, end, 
	width)
pygame.display.update()

# Wait for keypress
# Loop until keypress = ESCAPE
done = False
while not done:
   for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
         if (event.key == pygame.K_ESCAPE):
            done = True