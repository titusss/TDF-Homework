# The core Pong logic is from
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
from random import randint

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

def vibrate(strength, sleep_duration):
    crickit.drive_1.fraction = strength  # half on/off
    time.sleep(sleep_duration)
    crickit.drive_1.fraction = 0.0

pygame.init()
 
# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
 
# Open a new window
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
# size = (700, 500)
# screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")

paddleA = Paddle(WHITE, 10, 100)
paddleB = Paddle(WHITE, 10, 100)

ball = Ball(WHITE,10,10)

def setPositions():
    
    paddleA.rect.x = 20
    paddleA.rect.y = 200
    
    
    paddleB.rect.x = 770
    paddleB.rect.y = 200
    
    
    ball.rect.x = 345
    ball.rect.y = 195

    #Initialise player scores
    scoreA = 0
    scoreB = 0
    return paddleA, paddleB, ball, scoreA, scoreB

paddleA, paddleB, ball, scoreA, scoreB = setPositions()

#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()
 
# Add the car to the list of objects
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)
 
# Set Neopixel to empty
pixels.fill((0,0,0))
pixels.show()

# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True
 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
 
 
def mainMenu(buttonOneCurr, buttonOnePrev):
    inMenu = True
    while inMenu:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
              inMenu = False # Flag that we are done so we exit this loop
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                     inMenu = False
        
        font = pygame.font.Font(None, 32)
        fontArrow = pygame.font.Font(None, 64)
        text = font.render("Hold the red button to start", 1, WHITE)
        textArrow = fontArrow.render("^", 1, RED)
        for i in range(2):
            screen.fill(BLACK)
            pixels.fill((randint(0,255),randint(0,255),randint(0,255)))
            screen.blit(textArrow, (388,150))
            screen.blit(text, (260,250+i*3))
            time.sleep(0.3)
     
        # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
        buttonOnePrev = buttonOneCurr			# reset our "reading" of the button
        buttonOneCurr = ss.digital_read(BUTTON_1)	# actually read the button and set that to a variable called "buttonOneCurr"
        if not buttonOneCurr and buttonOnePrev:
            pixels.fill((0,0,0))
            pixels.show()
            inMenu = False

mainMenu(buttonOneCurr, buttonOnePrev)

# -------- Main Program Loop -----------
while carryOn:
    
    # Read Potentiometer value
    potRightValue = ss.analog_read(potRight)
    potLeftValue = ss.analog_read(potLeft)
    # Potentiometer mapping
    potLeftValueAdjusted = translate(potLeftValue, 10, 1023, 0, 380)
    potRightValueAdjusted = translate(potRightValue, 10, 1023, 0, 380)
    # Read button values
    buttonOnePrev = buttonOneCurr			# reset our "reading" of the button
    buttonOneCurr = ss.digital_read(BUTTON_1)	# actually read the button and set that to a variable called "buttonOneCurr"
    
    # --- Main event loop
    if not buttonOneCurr and buttonOnePrev:
        winnerColor = (0,255,0)
        winnerText = "   Left wins!!!"
        if scoreA > scoreB:
            winnerColor = (255,0,0)
            winnerText = "   Right wins!!!"
        elif scoreA == scoreB:
            winnerColor = (255,255,0)
            winnerText = "Both sides win!"
        screen.fill(BLACK)
        font = pygame.font.Font(None, 74)
        winnerText = font.render(winnerText, 1, winnerColor)
        screen.blit(winnerText, (200,210))
        pygame.display.flip()
        for i in range(24):
            pixels[i] = winnerColor
            time.sleep(0.08)
        vibrate(0.3, 0.2)
        vibrate(0.3, 0.2)
        vibrate(0.3, 0.2)
        pixels.fill((0,0,0))
        pixels.show()
        paddleA, paddleB, ball, scoreA, scoreB = setPositions()
        mainMenu(buttonOneCurr, buttonOnePrev)
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
    print(ball.velocity[0], ball.velocity[1])
    if ball.rect.x>=790:
        scoreA+=1
        lightUpNeopixel((255,0,0))
        vibrate(0.2, 0.1)
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x<=0:
        scoreB+=1
        vibrate(0.2, 0.1)
        lightUpNeopixel((0,0,255))
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y>450:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y<0:
        ball.velocity[1] = -ball.velocity[1] 
 
    #Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
      ball.bounce()
      vibrate(0.3, 0.05)
    
    # --- Drawing code should go here
    # First, clear the screen to black. 
    screen.fill(BLACK)
    #Draw the net
    pygame.draw.line(screen, WHITE, [399, 0], [399, 500], 5)
    
    #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen) 
 
    #Display scores:
    font = pygame.font.Font(None, 74)
    text = font.render(str(scoreA), 1, WHITE)
    screen.blit(text, (305,10))
    text = font.render(str(scoreB), 1, WHITE)
    screen.blit(text, (465,10))
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
    # --- Limit to 60 frames per second
    clock.tick(60)
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()
