from microbit import *
import time as t

VEML7700 = 0x10
ALS_CONF = 0x00

ALS_GAIN = {
    "gain1" : 00,
    "gain2" : 01,
    "gain1/8" : 10,
    "gain1/4" : 11
}
ALS_IT = {
    "IT25" : 1100,
    "IT50" : 1000,
    "IT100" : 0000,
    "IT200" : 0001,
    "IT400" : 0010,
    "IT800" : 0011
}

A =  button_a
b = button_b

while A.is_pressed() and b.is_pressed() != True:
    print("ingenting å se her")