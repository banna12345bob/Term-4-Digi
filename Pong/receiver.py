from bitio.src import microbit
import math, pygame, time

# I'm sorry

# https://stackoverflow.com/questions/29640685/how-do-i-detect-collision-in-pygame
pygame.init()
screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Displays text that says hello in green
font = pygame.font.SysFont(None, 24)
scoreFont = pygame.font.SysFont(None, 100)

def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = font.render(fps, 1, (255, 0, 0))
	return fps_text

def getInputMicrobit(channel):
    incoming = 0
    if channel == 1:
        incoming = microbit.pin0.read_analog() - 495
    elif channel == 2:
        incoming = microbit.pin1.read_analog() - 495
    if 20 > incoming > -20:
        incoming = 0
    return incoming

def getInputKeyboard(channel):
    keyState = pygame.key.get_pressed()
    if keyState[pygame.K_DOWN]:
        if channel == 2:
            return 250
    if keyState[pygame.K_UP]:
        if channel == 2:
            return -250
    if keyState[pygame.K_w]:
        if channel == 1:
            return -250
    if keyState[pygame.K_s]:
        if channel == 1:
            return 250
    return 0

sensitivity, speed = 1, 7
yOne = yTwo = screen.get_height() / 2 - 100
x, y = screen.get_width() / 2 - 20, screen.get_height() / 2 - 20
running, flip = True, False
bounceAngleY = bounceAngleX = score1 = score2 = 0
dt = now = prev_time = cooldown = 0
paddleHeight = 200
targetFPS = 60
paddleCooldown, edgeCooldown = 0, 7
showColider = showAdvanced = showPos = showTime = False
debug = False
dCooldown = 30

while running:
    if debug:
        # Debug stuff Only applies if in debug mode
        dCooldown += 1
        keyState = pygame.key.get_pressed()
        keyRepeat = pygame.key.get_repeat()
        if keyState[pygame.K_e] and dCooldown > 5:
            speed += 1
            dCooldown = 0
        if keyState[pygame.K_r] and dCooldown > 5:
            speed -= 1
            dCooldown = 0
        if keyState[pygame.K_h] and dCooldown > 5:
            # Ew ew gross don't do this but it works
            if showAdvanced == False and showColider == False and showPos == False and showTime == False:
                showAdvanced = True
                dCooldown = 0
            elif showAdvanced == True and showColider == False and showPos == False and showTime == False:
                showAdvanced = False
                dCooldown = 0
            if showAdvanced == False and showColider == False and showPos == False and showTime == False:
                showPos = True
                dCooldown = 0
            elif showAdvanced == False and showColider == False and showPos == True and showTime == False:
                showPos = False
                dCooldown = 0
            if showAdvanced == False and showColider == False and showPos == False and showTime == False:
                showTime = True
                dCooldown = 0
            elif showAdvanced == False and showColider == False and showPos == False and showTime == True:
                showTime = False
                dCooldown = 0
            if showColider == False and showAdvanced == False and showPos == False and showTime == False:
                dCooldown = 0
                showColider = True
            elif showColider == True and showAdvanced == False and showPos == False and showTime == False:
                dCooldown = 0
                showColider = False


    now = time.time()
    if prev_time != 0:
        dt = now - prev_time

    yOne = max(0, min(yOne, screen.get_height() - paddleHeight))
    yTwo = max(0, min(yTwo, screen.get_height() - paddleHeight))

    player1 = pygame.Rect(screen.get_width() - 100, yOne, 25, paddleHeight)
    player2 = pygame.Rect(100, yTwo, 25, paddleHeight)
    player1Colide = pygame.Rect(screen.get_width()-100, yOne, 1000, paddleHeight)
    player2Clolide = pygame.Rect(-875, yTwo, 1000, paddleHeight)
    ball = pygame.Rect(x, y, 20, 20)

    # https://gamedev.stackexchange.com/questions/4253/in-pong-how-do-you-calculate-the-balls-direction-when-it-bounces-off-the-paddl
    if ball.colliderect(player1Colide) and cooldown > paddleCooldown:
        intersectY = y - ((x - (100 + 25)) * (y)) / (x)
        relativeIntersectY = (yOne + (paddleHeight / 2)) - intersectY
        normalizedRelativeIntersectionY = (relativeIntersectY / (paddleHeight / 2))
        bounceAngle = normalizedRelativeIntersectionY * 75
        bounceAngleY = bounceAngle
        if flip == False:
            speed += 1
            flip = True
            bounceAngleX = 180
        cooldown = 0
        colide1 = True
    elif ball.colliderect(player2Clolide) and cooldown > paddleCooldown:
        intersectY = y - ((x - (100 + 25)) * (y)) / (x)
        relativeIntersectY = (yTwo + (paddleHeight / 2)) - intersectY
        normalizedRelativeIntersectionY = (relativeIntersectY / (paddleHeight/2))
        bounceAngle = normalizedRelativeIntersectionY * 75
        bounceAngleY = bounceAngleX = bounceAngle
        if flip == True:
            speed += 1
            flip = False
            bounceAngleX = 0
        cooldown = 0
        colide2 = True
    else:
        colide1 = colide2 = False

    x += speed * math.cos(bounceAngleX) * targetFPS * dt
    y += speed * -math.sin(bounceAngleY) * targetFPS * dt
    
    if y <= 0 or y >= screen.get_height() - 20 and cooldown > edgeCooldown:
        bounceAngleY *= -1
        cooldown = 0

    # Very icky ties movement speed to FPS. Fixed by limiting FPS to 60
    yTwo += getInputMicrobit(1) * 0.025 * sensitivity * targetFPS * dt
    yOne += getInputMicrobit(2) * 0.025 * sensitivity * targetFPS * dt

    if x <= 0:
        score2 += 1
        x, y = screen.get_width() / 2 - 20, screen.get_height() / 2 - 20
        yOne = yTwo = screen.get_height() / 2 - 100
        speed = 7
        bounceAngle = bounceAngleY = bounceAngleX = 0
        flip = False
    if x >= screen.get_width():
        score1 += 1
        x, y = screen.get_width() / 2 - 20, screen.get_height() / 2 - 20
        yOne = yTwo = screen.get_height() / 2 - 100
        bounceAngle = bounceAngleY = 0
        bounceAngleX = 180
        speed = 7
        flip = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Draws ball
    pygame.draw.rect(screen, (255, 255, 255), ball)
    # Draws padles
    pygame.draw.rect(screen, (255, 255, 255), player1)
    pygame.draw.rect(screen, (255, 255, 255), player2)
    if showColider == True:
        if not colide1:
            pygame.draw.rect(screen, (0, 255, 0), player1Colide)
        else:
            pygame.draw.rect(screen, (255, 0, 0), player1Colide)
        if not colide2:
            pygame.draw.rect(screen, (0, 255, 0), player2Clolide)
        else:
            pygame.draw.rect(screen, (255, 0, 0), player2Clolide)

    # FPS counter
    if debug:
        screen.blit(update_fps(), (20, 20))
    if showAdvanced:
        screen.blit(font.render("flip: "+str(flip), 1, (255, 0, 0)), (200, 20))
        screen.blit(font.render("speed: "+str(speed), 1, (255, 0, 0)), (200, 40))
        screen.blit(font.render("Dubug mode: showAdvanced", 1, (255, 0, 0)), (screen.get_width() - 400, 40))
    if showPos:
        screen.blit(font.render("x: " + str(x), 1, (255, 0, 0)), (400, 20))
        screen.blit(font.render("y: " + str(y), 1, (255, 0, 0)), (400, 40))
        screen.blit(font.render("Dubug mode: showPos", 1, (255, 0, 0)), (screen.get_width() - 400, 40))
    if showTime:
        screen.blit(font.render("time: " + str(now), 1, (255, 0, 0)), (600, 20))
        screen.blit(font.render("prev_Time: " + str(prev_time), 1, (255, 0, 0)), (600, 40))
        screen.blit(font.render("cooldown: " + str(cooldown), 1, (255, 0, 0)), (850, 20))
        screen.blit(font.render("Dubug mode: showTime", 1, (255, 0, 0)), (screen.get_width() - 400, 40))
    if showColider:
        screen.blit(font.render("Dubug mode: showColider", 1, (255, 0, 0)), (screen.get_width() - 400, 40))
    screen.blit(scoreFont.render(str(score1), 1, (255, 255, 255)), (550, 100))
    screen.blit(scoreFont.render(str(score2), 1, (255, 255, 255)), (screen.get_width() - 550, 100))
    
    cooldown += 1
    clock.tick(30)
    prev_time = now
    pygame.display.update()

pygame.quit()
