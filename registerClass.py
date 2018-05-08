import onionGpio

# class to control a shift register chip
class shiftRegister:
    # instantiates the GPIO objects based on the pin numbers
    def __init__(self, dataPin, serialClock, registerClock):
        self.ser = onionGpio.OnionGpio(dataPin)
        self.srclk = onionGpio.OnionGpio(serialClock)
        self.rclk = onionGpio.OnionGpio(registerClock)
        self.setup()

    # Pulses the latchpin - write the outputs to the data lines
    def latch(self):
        self.rclk.setValue(0)
        self.rclk.setValue(1)
        self.rclk.setValue(0)

    # Clear all the LEDS by pulsing the Serial Clock 8 times in and then the rclk once
    def clear(self):
        self.ser.setValue(0)
        for x in range(0, 8): #Clears out all the values currently in the register
            self.srclk.setValue(0)
            self.srclk.setValue(1)
            self.srclk.setValue(0)

        self.latch()

    # sets the GPIOs to output with an initial value of zero
    def setup(self):
        self.ser.setOutputDirection(0)
        self.srclk.setOutputDirection(0)
        self.rclk.setOutputDirection(0)

        self.clear()

    # push a bit into the shift register
    #   sets the serial pin to the correct value and then pulses the serial clock to shift it in
    def inputBit(self, inputValue):
        self.ser.setValue(inputValue)
        self.srclk.setValue(0)
        self.srclk.setValue(1)
        self.srclk.setValue(0)


    # push a byte to the shift regiter
    #   splits the input values into individual values and inputs them. Then pulses the latch pin to show the output.
    def outputBits(self, inputString):
        bitList = list(inputString) # Splits the string into a list of individual characters ("11000000" -> ["1","1","0","0","0","0","0","0"])
        bitList = bitList[::-1]      # reverses the string to send LSB first
        for bit in bitList:
            bit = int(bit) # Transforms the character back into an int ("1" -> 1)
            self.inputBit(bit)
        self.latch()
