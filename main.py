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
B = button_b

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
except Exception as error:
    print("an error occured:", error)
    raise
sensor.alter_gain()
sensor.alter_IT()

i2c.init()
i2c.write(
    VEML7700,
    bytes([ALS_CONF,
    config & 0xFF,
    (config >> 8) & 0xFF
    ]))

i2c.write(VEML7700, bytes([0x04]) repeat=True)
data = i2c.read(VEML7700,2)
readabledataish = data[0] | (data[1] << 8)
with open("data.txt", "a") as file:
    file.write(str(data))

while A.is_pressed() and B.is_pressed() != True:
    print("ingenting å se her")