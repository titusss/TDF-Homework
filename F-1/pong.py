# The Pong game is from
# "Pong Tutorial using Pygame – Adding a Scoring System"
# May 27th, 2019
# By Anonyous, 101Computing.net
# https://www.101computing.net/pong-tutorial-using-pygame-adding-a-bouncing-ball/

import pygame
from paddle import Paddle
from ball import Ball
import time
from adafruit_crickit import crickit
from adafruit_seesaw.neopixel import NeoPixel

# Initialize crickit pot controls
ss = crickit.seesaw
potRight = crickit.SIGNAL2
potLeft = crickit.SIGNAL3
ss.pin_mode(potRight, ss.INPUT)
ss.pin_mode(potLeft, ss.INPUT)

# Vibration motor init
crickit.drive_1.frequency = 1000

# Button init
BUTTON_1 = crickit.SIGNAL1 
buttonOnePrev = False  # stores value of last iteration
buttonOneCurr = False  # stores value of current iteration
ss.pin_mode(BUTTON_1, ss.INPUT_PULLUP)

# Neopixel init
num_pixels = 24  # Number of pixels driven from Crickit NeoPixel terminal
pixels = NeoPixel(crickit.seesaw, 20, num_pixels)

def lightUpNeopixel(rgb_tuple):
    pixels.fill(rgb_tuple)
    pixels.show()
    time.sleep(0.1)
    pixels.fill((0,0,0))
    pixels.show()

def translate(value, leftMin, leftMax, rightMin, rightMax): #Attributed to Adam Luchjenbroers, 12/8/2009
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def vibrate(strength):
    crickit.drive_1.fraction = strength  # half on/off
    crickit.drive_1.fraction = 0.0

pygame.init()
 
# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
 
# Open a new window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")

def setPositions():
    paddleA = Paddle(WHITE, 10, 100)
    paddleA.rect.x = 20
    paddleA.rect.y = 200
    
    paddleB = Paddle(WHITE, 10, 100)
    paddleB.rect.x = 670
    paddleB.rect.y = 200
    
    ball = Ball(WHITE,10,10)
    ball.rect.x = 345
    ball.rect.y = 195

    #Initialise player scores
    scoreA = 0
    scoreB = 0

setPositions()
 
#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()
 
# Add the car to the list of objects
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)
 
# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True
 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while carryOn:
    # Read Potentiometer value
    potRightValue = ss.analog_read(potRight)
    potLeftValue = ss.analog_read(potLeft)
    # Potentiometer mapping
    potLeftValueAdjusted = translate(potLeftValue, 10, 1023, 0, 1000)
    potRightValueAdjusted = translate(potRightValue, 10, 1023, 0, 1000)
    # Read button values
    buttonOnePrev = buttonOneCurr			# reset our "reading" of the button
    buttonOneCurr = ss.digital_read(BUTTON_1)	# actually read the button and set that to a variable called "buttonOneCurr"

    # --- Main event loop
    if not buttonOneCurr and buttonOnePrev:
        vibrate(0.5)
        setPositions()
        lightUpNeopixel((0,255,0))
        time.sleep(0.8)
        vibrate(0.5)
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we exit this loop
        elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                     carryOn=False
 
    #Moving the paddles when the use uses the arrow keys (player A) or "W/S" keys (player B) 
    keys = pygame.key.get_pressed()
    paddleA.rect[1] = potLeftValueAdjusted
    paddleB.rect[1] = potRightValueAdjusted
 
    # --- Game logic should go here
    all_sprites_list.update()
    
    #Check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x>=690:
        scoreA+=1
        lightUpNeopixel((255,0,0))
        vibrate(0.5)
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x<=0:
        scoreB+=1
        vibrate(0.5)
        lightUpNeopixel((0,0,255))
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y>490:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y<0:
        ball.velocity[1] = -ball.velocity[1]     
 
    #Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
      ball.bounce()
      vibrate(0.1)
    
    # --- Drawing code should go here
    # First, clear the screen to black. 
    screen.fill(BLACK)
    #Draw the net
    pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)
    
    #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen) 
 
    #Display scores:
    font = pygame.font.Font(None, 74)
    text = font.render(str(scoreA), 1, WHITE)
    screen.blit(text, (250,10))
    text = font.render(str(scoreB), 1, WHITE)
    screen.blit(text, (420,10))
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
    # --- Limit to 60 frames per second
    clock.tick(60)
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()