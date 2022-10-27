from bitio.src import microbit
import math
import pygame


# https://gamedev.stackexchange.com/questions/4253/in-pong-how-do-you-calculate-the-balls-direction-when-it-bounces-off-the-paddl
# https://stackoverflow.com/questions/29640685/how-do-i-detect-collision-in-pygame
pygame.init()
screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Displays text that says hello in green
font = pygame.font.SysFont(None, 24)

def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = font.render(fps, 1, (255, 0, 0))
	return fps_text

def getInputMicrobit(channel):
    microbit.radio.on()
    microbit.radio.config(channel=channel)
    incoming = microbit.radio.receive_bytes()
    microbit.radio.off()
    incoming = incoming[2:-1]
    try:
        if incoming[0] == str(channel):
            if incoming[1] == "y":
                yIn = int(incoming[2:len(incoming)])-19
                print(yIn)
        return 0
    except:
        return 0

def getInputKeyboard(channel):
    keyState = pygame.key.get_pressed()
    sensitivity = 1
    if keyState[pygame.K_DOWN]:
        if channel == 2:
            return 50 * sensitivity
    if keyState[pygame.K_UP]:
        if channel == 2:
            return -50 * sensitivity
    if keyState[pygame.K_w]:
        if channel == 1:
            return -50 * sensitivity
    if keyState[pygame.K_s]:
        if channel == 1:
            return 50 * sensitivity
    return 0

sensitivity, speed = 5, 5
yIn1 = yIn2 = 0
yOne = yTwo = screen.get_height() / 2 - 100
x, y = screen.get_width() / 2 - 20, screen.get_height() / 2 - 20
running, flip = True, False
bounceAngle = bounceAngleY = bounceAngleX = score1 = score2 = 0
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
        bounceAngleY = bounceAngleX = bounceAngle
        if flip == False:
            bounceAngleX *= -1
            speed += 1
        flip = True
    elif colide2:
        intersectY = y - ((x - (yOne + 200)) * y) / x
        relativeIntersectY = (yOne+(200/2)) - intersectY
        normalizedRelativeIntersectionY = (relativeIntersectY/(200/2))
        bounceAngle = normalizedRelativeIntersectionY * 75
        bounceAngleY = bounceAngleX = bounceAngle
        if flip == True:
            bounceAngleX *= -1
            speed += 1
        flip = False

    x += speed*math.cos(bounceAngleX)
    y += speed*-math.sin(bounceAngleY)
    if y <= 0 or y >= screen.get_height() - 20:
        bounceAngleY *= -1

    # Very icky ties movement speed to FPS. Fixed by limiting FPS to 60
    # Multithreading Don't ask I don't know
    # https://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python
    yTwo += getInputKeyboard(1) * 0.025 * sensitivity
    yOne += getInputKeyboard(2) * 0.025 * sensitivity

    if x <= 0:
        score2 += 1
        x, y = screen.get_width() / 2 - 20, screen.get_height() / 2 - 20
        yOne = yTwo = screen.get_height() / 2 - 100
        speed = 5
        bounceAngle = bounceAngleY = bounceAngleX = 0
    if x >= screen.get_width():
        score1 += 1
        x, y = screen.get_width() / 2 - 20, screen.get_height() / 2 - 20
        yOne = yTwo = screen.get_height() / 2 - 100
        bounceAngle = bounceAngleY = 0
        bounceAngleX = 180
        speed = 5

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
    screen.blit(font.render("score1: "+str(score1), 1, (255, 0, 0)), (300, 20))
    screen.blit(font.render("score2: "+str(score2), 1, (255, 0, 0)), (300, 40))

    # Caps the FPS to 60
    clock.tick(60)

    pygame.display.update()

pygame.quit()