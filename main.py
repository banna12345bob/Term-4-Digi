from microbit import *
import audio

timer = 0
display.show(Image(
    "00000:"
    "09090:"
    "00000:"
    "09990:"
    "00000"))
audio.play(Sound.HELLO)

while True:
    if pin_logo.is_touched():
        timer = 0
        display.show(Image.HAPPY)
    elif accelerometer.was_gesture('shake'):
        timer = 0
        display.show(Image.SURPRISED)
        
    else:
        sleep(500)
        timer += 0.5
        # sleep for half a second only to make it react more quickly to logo touch & shake
        
    if timer == 20:
        display.show(Image.SAD)
       
    elif timer == 30:
        display.show(Image.ASLEEP)
    
    elif timer == 40:
        display.show(Image.SKULL)
       
        break
