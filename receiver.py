from bitio.src import microbit
import math
import pygame

pygame.init()
screen = pygame.display.set_mode()

microbit.radio.on()
x, y = 0, 0
running = True
while running:
    incoming = microbit.radio.receive_bytes()
    incoming = incoming[2:-1]
    if incoming[0] == "x":
        x = int(incoming[1:len(incoming)])
        if x<0.0:
            x *= -1
    elif incoming[0] == "y":
        y = int(incoming[1:len(incoming)])
        if y<0.0:
            y *= -1
    acceleration = math.sqrt(pow(x, 2) + pow(y, 2))
    if (acceleration-1000.0)>0:
        print(acceleration-1000.0)

    # Pygame stuff
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (0,0,255), (250, 250), 75)
    pygame.display.flip()

pygame.quit()