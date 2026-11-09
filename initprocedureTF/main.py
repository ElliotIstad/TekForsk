from microbit import *

ad = 0x48
with open("initdata.txt") as f:
    i2c.init()
    i2c.write(ad, bytes([0x00]), repeat=True)
    f.write(str(i2c.read(ad, 2)) + "\n")

    i2c.write(ad, bytes([0x01]), repeat=True)
    f.write(str(i2c.read(ad, 2)) + "\n")

    i2c.write(ad, bytes([0x02]), repeat=True)
    f.write(str(i2c.read(ad, 2)) + "\n")

    i2c.write(ad, bytes([0x03]), repeat=True)
    f.write(str(i2c.read(ad, 2)) + "\n")

    i2c.write(ad, bytes([0x04]), repeat=True)
    f.write(str(i2c.read(ad, 2)) + "\n")

    i2c.write(ad, bytes([0x05]), repeat=True)
    f.write(str(i2c.read(ad, 2)) + "\n")

    i2c.write(ad, bytes([0x06]), repeat=True)
    f.write(str(i2c.read(ad, 2)) + "\n")

    i2c.write(ad, bytes([0x07]), repeat=True)
    f.write(str(i2c.read(ad, 2)) + "\n")