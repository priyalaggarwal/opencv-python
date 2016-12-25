import cv2
import imutils
import pygame
from pygame.locals import *
import sys, time, random

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FONTSIZE=24
FPS = 40
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 8
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 10
PLAYERMOVERATE = 5

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: #escape quits
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False


#initialisation
pygame.init()
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Car race')
done = False
clock = pygame.time.Clock()

#default system font
font = pygame.font.Font(None, FONTSIZE)

#sounds
_sound_library = {}
def play_sound(path):
  global _sound_library
  sound = _sound_library.get(path)
  if sound == None:
  	sound = pygame.mixer.Sound(path)
  	sound_library[path] = sound
  sound.play()

#images
_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                #canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(path)
                _image_library[path] = image
        return image

# "Start" screen
drawText('Press any key to start the game.', font, screen, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
pygame.display.update()
waitForPlayerToPressKey()

# images
playerImage = get_image('image/car1.png')
car3 = get_image('image/car3.png')
car4 = get_image('image/car4.png')
playerRect = playerImage.get_rect()
baddieImage = get_image('image/car2.png')
sample = [car3,car4,baddieImage]
wallLeft = get_image('image/left.png')
wallRight = get_image('image/right.png')

camera = cv2.VideoCapture(0)

# blue color range
lowerColor = (110,50,50)
upperColor = (130,255,255)


left = 250
flag=None
prevX=None
prevY=None
x = 30
y = 30
CV_FILLED = -1

baddies = []
score = 0

def gameControl(moveLeft, moveRight):
	_, frame = camera.read()
	frame = imutils.resize(frame, 500)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	mask = cv2.inRange(hsv, lowerColor, upperColor)
	mask = cv2.erode(mask, None, iterations=1)
	mask = cv2.dilate(mask, None, iterations=1)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]

	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
	
		if M["m00"]>0: 
			(centerX, centerY) = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		if radius>10:
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, (centerX, centerY), 5, (0, 0, 255), CV_FILLED)

			if centerX>198:
				moveRight = False
				moveLeft = True
			else:
				moveLeft = False
				moveRight = True

	cv2.imshow('frame', frame)
	cv2.waitKey(1)
	return moveLeft, moveRight


moveLeft = moveRight = False
playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
baddieAddCounter = 0
	
while True: # the game loop
	score +=1
	moveLeft, moveRight = gameControl(moveLeft, moveRight)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			terminate()

	baddieAddCounter += 1
	if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize =30

            newBaddie = {'rect': pygame.Rect(random.randint(140, 485), 0 - baddieSize, 23, 47),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(random.choice(sample), (23, 47)),
                        }
            baddies.append(newBaddie)
            sideLeft= {'rect': pygame.Rect(0,0,126,600),
                       'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                       'surface':pygame.transform.scale(wallLeft, (126, 599)),
                       }
            baddies.append(sideLeft)
            sideRight= {'rect': pygame.Rect(497,0,303,600),
                       'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                       'surface':pygame.transform.scale(wallRight, (303, 599)),
                       }
            baddies.append(sideRight)

	
    	# Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
        	playerRect.move_ip(PLAYERMOVERATE, 0)

        for b in baddies:
        	b['rect'].move_ip(0, b['speed'])

        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Draw the game world on the window.
        screen.fill(BACKGROUNDCOLOR)

        drawText('Score: %s' % (score), font, screen, 128, 0)

        screen.blit(playerImage, playerRect)

        
        for b in baddies:
            screen.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the car have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
        	break

        clock.tick(FPS)

drawText('Game over', font, screen, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press any key to play again.', font, screen, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 30)
pygame.display.update()
time.sleep(2)
camera.release()
waitForPlayerToPressKey()