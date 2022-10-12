from microbit import *
import radio

radio.on()
while True:
    try:
        radio.send_bytes(str(accelerometer.get_values()))
    except:
        radio.send_bytes("FAIL")
    display.show(Image.ANGRY)