from bitio.src import microbit
import math
import pygame
import pygame.camera

from pygame.examples import camera

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
    print("x: "+str(x))
    print("y: "+str(y))

    # Pygame stuff
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (0,0,255), (0, 0), 75)
    pygame.draw.circle(screen, (0,0,255), (max(0, min(x, screen.get_width())), max(0, min(y, screen.get_height()))), 75)
    pygame.display.flip()

pygame.quit()