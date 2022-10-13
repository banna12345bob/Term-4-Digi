from microbit import *
import radio

radio.on()
while True:
    try:
        radio.send_bytes("x"+str(accelerometer.get_x()))
        radio.send_bytes("y"+str(accelerometer.get_y()))
        display.show(Image.ANGRY)
    except:
        display.scroll("FAIL")
        radio.send_bytes("FAIL")