from microbit import *
import radio

radio.on()
player = 2
radio.config(channel=player)
while True:
    try:
        # radio.send_bytes("x"+str(accelerometer.get_x()))
        radio.send_bytes(str(player)+"y"+str(pin0.read_analog() - 495))
        display.show(Image.ANGRY)
    except:
        display.scroll("FAIL")
        radio.send_bytes("FAIL")