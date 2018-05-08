from registerClass import shiftRegister
import signal

# instantiate a shift register object
#   Data pin is GPIO 1, serial clock pin is GPIO 2, Latch pin is GPIO 3
shiftRegister = shiftRegister(1,2,3)

# Signal interrupt handler to exit after the animation has finished when Ctrl-C is pressed
def signal_handler(signal, frame):
    global interrupted
    interrupted = True

signal.signal(signal.SIGINT, signal_handler)


# To create the animation on the LEDs through the shift register,
# we use a binary number instead of a string. We can move the lights
# around by bitshfting instead of string operations.
value = 0b11000000
interrupted = False

# infinite loop - runs main program code continuously
while True:
    # this animation has 12 different frames, so we'll loop through each one
    for x in range(0, 12):
        # we need to transform the binary value into a string only when sending it to the shift register
        bytestring = format(value, '08b')
        shiftRegister.outputBits(bytestring)
        # now we are free to manipulate the binary number using bitshifts

        # if in the first half (6 frames) of the animation, move the LEDs to the right
        if x < 6:
            value >>= 1 # Shifts all digits right by one (11000000 -> 01100000)
        # else we must be in the second half, so move the LEDs to the left
        else:
            value <<= 1 # Shifts all digits left by one (01100000 -> 11000000)
    # interrupt (Ctrl-C) handler
    if interrupted:
        shiftRegister.clear() # turn off the LEDs
        break
