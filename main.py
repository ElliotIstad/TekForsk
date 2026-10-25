from microbit import *
import time as t

VEML7700 = 0x10
ALS_CONF = 0x00
#7 bit slave address = 0x10
#write address = 0x20
config = 0b0

ALS_GAIN = {
    "gain1" : 0b00,
    "gain2" : 0b01,
    "gain1/8" : 0b10,
    "gain1/4" : 0b11
}
ALS_IT = {
    "IT25" : 0b1100,
    "IT50" : 0b1000,
    "IT100" : 0b0000,
    "IT200" : 0b0001,
    "IT400" : 0b0010,
    "IT800" : 0b0011
}

A =  button_a
b = button_b

class configure_sensor():
    def __init__(self, gain, IT):
        self.gain = gain
        self.integration = IT
    
    def alter_gain(self):
        global config
        config = config & ~(0b11 << 11)
        config = config | (self.gain << 11)

    def alter_IT(self):
        global config
        config = config & ~(0b1111 << 6)
        config = config | (self.integration << 6)

try:
    sensor = configure_sensor(
    ALS_GAIN["gain" + input("pick a gain level. 1, 2, 1/8 or 1/4 : ")],
    ALS_IT["IT" + input("pick an integration time (in ms). 25, 50, 100, 200, 400 or 800 : ")]
)
except:
    print("an error occured buddy")

i2c.init()
i2c.write(
    VEML7700,
    bytes([ALS_CONF,
    config & 0xFF,
    (config >> 8) & 0xFF
    ]))

sensor.alter_gain()
sensor.alter_IT()

"""
0001100011000000
jeg vil endre gain til 00 (er 11 nå)
da må jeg 1:
    0b11 << 11
    #har nå en ny som er - 0001100000000000
steg 2:
    inverse den nye
    ~(0b11 << 11)
steg 3:
    så slå de sammen med en AND
    config = config & ~(0b11 << 11)

jeg vil endre gain til 01
steg 1:
    først må jeg endre 12:11 til 00
    config = config & ~(0b11 << 11)
steg 2:
    etter det kan jeg bare pushe de flatt med en OR
    config = config | (0b01 << 11)
"""


while A.is_pressed() and b.is_pressed() != True:
    print("ingenting å se her")