from bitio.src import microbit
from multiprocessing import Process
import math
import pygame


# https://gamedev.stackexchange.com/questions/4253/in-pong-how-do-you-calculate-the-balls-direction-when-it-bounces-off-the-paddl
# https://stackoverflow.com/questions/29640685/how-do-i-detect-collision-in-pygame
pygame.init()
screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Displays text that says hello in green
font = pygame.font.SysFont(None, 24)

microbit.radio.on()
def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = font.render(fps, 1, (255, 0, 0))
	return fps_text

sensitivity, speed = 5, 5
yIn1 = yIn2 = 0
yOne = yTwo = screen.get_height() / 2 - 100
x, y = screen.get_width() / 2 - 20, screen.get_height() / 2 - 20
running, flip, yFlip = True, False, False
bounceAngle = bounceAngleY = 0
while running:
    yOne = max(0, min(yOne, screen.get_height() - 200))
    yTwo = max(0, min(yTwo, screen.get_height() - 200))

    player1 = pygame.Rect(screen.get_width() - 100, yOne, 25, 200)
    player2 = pygame.Rect(100, yTwo, 25, 200)
    ball = pygame.Rect(x, y, 20, 20)

    colide1 = ball.colliderect(player1)
    colide2 = ball.colliderect(player2)
    if colide1:
        intersectY = y - ((x - (yOne + 200)) * y) / x
        relativeIntersectY = (yOne+(200/2)) - intersectY
        normalizedRelativeIntersectionY = (relativeIntersectY/(200/2))
        bounceAngle = normalizedRelativeIntersectionY * 75
        bounceAngleY = bounceAngle
        if flip == False:
            speed += 1
        flip = True
    elif colide2:
        intersectY = y - ((x - (yOne + 200)) * y) / x
        relativeIntersectY = (yOne+(200/2)) - intersectY
        normalizedRelativeIntersectionY = (relativeIntersectY/(200/2))
        bounceAngle = normalizedRelativeIntersectionY * 75
        bounceAngleY = bounceAngle
        if flip == True:
            speed += 1
        flip = False

    if not flip:
        if yFlip:
            # instead of this set a flag saying that you hit the edge something like yFlip
            x += speed*math.cos(bounceAngle)
            y += speed*math.sin(90)
            yFlip = False
        else:
            x += speed*math.cos(bounceAngle)
            y += speed*math.sin(bounceAngleY)
    elif flip:
        # x -= 2 * speed
        if yFlip:
            x -= speed*math.cos(bounceAngle)
            y += speed*math.sin(90)
            yFlip = False
        else:
            x -= speed*math.cos(bounceAngle)
            y += speed*math.sin(bounceAngleY)
    if y <= 0 or y >= screen.get_height() - 20:
        bounceAngleY *= -1

    incoming = microbit.radio.receive_bytes()
    incoming = incoming[2:-1]
    if incoming[0] == "1":
        if incoming[1] == "y":
            yIn1 = int(incoming[2:len(incoming)])
            yTwo += yIn1 * 0.025 * sensitivity
    elif incoming[0] == "2":
        if incoming[1] == "y":
            yIn2 = int(incoming[2:len(incoming)])-20
            yOne += yIn2 * 0.025 * sensitivity

    if x <= 0 or x >= screen.get_width():
        x, y = screen.get_width() / 2 - 20, screen.get_height() / 2 - 20
        yOne = yTwo = screen.get_height() / 2 - 100
        speed = 5

    # Pygame stuff
    # Events
    keyState = pygame.key.get_pressed()
    # Very icky ties movement speed to FPS. Fixed by limiting FPS to 60
    # sensitivity = 1
    # if keyState[pygame.K_DOWN]:
    #     yOne += 10 * sensitivity
    # if keyState[pygame.K_UP]:
    #     yOne -= 10 * sensitivity
    # if keyState[pygame.K_w]:
    #     yTwo -= 10 * sensitivity
    # if keyState[pygame.K_s]:
    #     yTwo += 10 * sensitivity
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    
    # Draws ball
    pygame.draw.rect(screen, (255, 255, 255), ball)
    # Draws padles
    pygame.draw.rect(screen, (0, 0, 255), player1)
    pygame.draw.rect(screen, (255, 0, 0), player2)

    # FPS counter
    screen.blit(update_fps(), (20, 20))
    screen.blit(font.render("flip: "+str(flip), 1, (255, 0, 0)), (200, 20))
    screen.blit(font.render("yFlip: "+str(yFlip), 1, (255, 0, 0)), (300, 20))

    # Limits FPS to 60
    clock.tick(60)

    pygame.display.update()

pygame.quit()