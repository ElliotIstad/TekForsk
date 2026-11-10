from microbit import *

ad = 0x48
with open("initdata.txt") as f:
    i2c.init()
    for reg in range(0x00, 0x08):
        i2c.write(ad, bytes([reg]), repeat=True)
        f.write(str(i2c.read(ad, 2)) + "\n")