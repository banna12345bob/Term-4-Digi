from bitio.src import microbit

microbit.radio.on()
while True:
    incoming = microbit.radio.receive_bytes()
    try:
        print(incoming[2:-1])
    except:
        print("RECEIVER FAIL")