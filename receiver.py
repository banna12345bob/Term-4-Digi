from bitio.src import microbit
import math

microbit.radio.on()
x, y = 0, 0
while True:
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