from microbit import *
import time as t

VEML7700 = 0x10
ALS_CONF = 0x00
#7 bit slave address = 0x10
#write address = 0x20

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

def Configure_Sensor():


while A.is_pressed() and b.is_pressed() != True:
    print("ingenting å se her")