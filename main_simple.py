from machine import Pin
from utime import sleep

outputs = [13, 12, 14, 27, 26, 25, 33, 32, 23]
inputs  = [16, 17,  4,  2, 15,  5, 18, 19, 34]

state = {}
for o in outputs:
    state[o] = 0
    Pin(o, Pin.OUT).off()

def update(pin, so):
    if so:
        pin.off()
        return 0
    else:
        pin.on()
        return 1

while True:
    for i, o in zip(inputs, outputs):
        pi = Pin(i, Pin.IN, Pin.PULL_DOWN)
        po = Pin(o, Pin.OUT)
        
        val = pi.value()
        if val:
            state[o] = update(po, state[o])
            sleep(1)
        
        sleep(0.01)
    print(state.values())
