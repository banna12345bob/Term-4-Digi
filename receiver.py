from bitio.src import microbit
import math, pygame, time, threading

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

class ThreadWithReturnValue(threading.Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return

def getInputMicrobitRadio(channel):
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
                return yIn
        return 0
    except:
        return 0

def getInputMicrobit(channel):
    incoming = 0
    try:
        if channel == 1:
            incoming = microbit.pin0.read_analog() - 495 + 6
        elif channel == 2:
            incoming = microbit.pin1.read_analog() - 495 - 18
        yIn = int(incoming)
        return yIn
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

sensitivity, speed = 1, 7
yIn1 = yIn2 = 0
yOne = yTwo = screen.get_height() / 2 - 100
x, y = screen.get_width() / 2 - 20, screen.get_height() / 2 - 20
running, flip = True, False
bounceAngle = bounceAngleY = bounceAngleX = score1 = score2 = 0
dt = now = prev_time = cooldown = 0
paddleHeight = 200
targetFPS = 60
while running:
    keyState = pygame.key.get_pressed()
    if keyState[pygame.K_e]:
        speed += 1
    if keyState[pygame.K_r]:
        speed -= 1

    now = time.time()
    if prev_time != 0:
        dt = now - prev_time
    yOne = max(0, min(yOne, screen.get_height() - paddleHeight))
    yTwo = max(0, min(yTwo, screen.get_height() - paddleHeight))

    player1 = pygame.Rect(screen.get_width() - 100, yOne, 25, paddleHeight)
    player2 = pygame.Rect(100, yTwo, 25, paddleHeight)
    ball = pygame.Rect(x, y, 20, 20)

    if x > screen.get_width() - 100 and yOne <= y <= yOne + paddleHeight and cooldown > 25:
        colide1 = True
    elif x < 100 and yTwo <= y <= yTwo + paddleHeight and cooldown > 25:
        colide2 = True
    else:
        colide1 = colide2 = False
    if colide1 or colide2:
        cooldown = 0
        
    if colide1:
        intersectY = y - ((x - (yOne + 200)) * y) / x
        relativeIntersectY = (yOne + (200 / 2)) - intersectY
        normalizedRelativeIntersectionY = (relativeIntersectY / (200 / 2))
        bounceAngle = normalizedRelativeIntersectionY * 75
        bounceAngleY = bounceAngleX = bounceAngle
        if flip == False:
            bounceAngleX *= -1
            speed += 1
        flip = True
    elif colide2:
        intersectY = y - ((x - (yOne + 200)) * y) / x
        relativeIntersectY = (yOne + (200 / 2)) - intersectY
        normalizedRelativeIntersectionY = (relativeIntersectY / (200 / 2))
        bounceAngle = normalizedRelativeIntersectionY * 75
        bounceAngleY = bounceAngleX = bounceAngle
        if flip == True:
            bounceAngleX *= -1
            speed += 1
        flip = False

    x += speed * math.cos(bounceAngleX) * targetFPS * dt
    y += speed * -math.sin(bounceAngleY) * targetFPS * dt
    
    if y <= 0 or y >= screen.get_height() - 20:
        if cooldown > 4:
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
    if x >= screen.get_width():
        score1 += 1
        x, y = screen.get_width() / 2 - 20, screen.get_height() / 2 - 20
        yOne = yTwo = screen.get_height() / 2 - 100
        bounceAngle = bounceAngleY = 0
        bounceAngleX = 180
        speed = 7

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
    screen.blit(font.render("speed: "+str(speed), 1, (255, 0, 0)), (200, 40))
    screen.blit(font.render("score1: "+str(score1), 1, (255, 0, 0)), (300, 20))
    screen.blit(font.render("score2: "+str(score2), 1, (255, 0, 0)), (300, 40))
    screen.blit(font.render("x: " + str(x), 1, (255, 0, 0)), (400, 20))
    screen.blit(font.render("y: " + str(y), 1, (255, 0, 0)), (400, 40))
    screen.blit(font.render("time: " + str(now), 1, (255, 0, 0)), (600, 20))
    screen.blit(font.render("prev_Time: " + str(prev_time), 1, (255, 0, 0)), (600, 40))
    screen.blit(font.render("cooldown: " + str(cooldown), 1, (255, 0, 0)), (850, 20))
    
    cooldown += 1
    clock.tick(0)
    prev_time = now
    pygame.display.update()

pygame.quit()