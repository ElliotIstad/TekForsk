from microbit import *
import time as t

VEML7700 = 0x10
ALS_CONF = 0x00
#7 bit slave address = 0x10
#write address = 0x20
Config = 0b0

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
ALS_GAIN_VALUE = {
    0b00: 1,
    0b01: 2,
    0b10: 0.125,
    0b11: 0.25
}
ALS_IT_MS = {
    0b1100: 25,
    0b1000: 50,
    0b0000: 100,
    0b0001: 200,
    0b0010: 400,
    0b0011: 800
}

A = button_a
B = button_b

class ConfigureSensor():
    def __init__(self, Gain, IT):
        self.Gain = Gain
        self.Integration = IT
    
    def AlterGain(self):
        global Config
        Config = Config & ~(0b11 << 11)
        Config = Config | (self.Gain << 11)

    def AlterIT(self):
        global Config
        Config = Config & ~(0b1111 << 6)
        Config = Config | (self.Integration << 6)


def RawToLux(Reading):
    # This uses the gain and integration time selected for the sensor.
    Resolution = (
        0.0042
        * (800 / ALS_IT_MS[Sensor.Integration])
        * (2 / ALS_GAIN_VALUE[Sensor.Gain])
    )
    Lux = Resolution * Reading
    Lux = (((6.0135e-13 * Lux - 9.3924e-9) * Lux + 8.1488e-5) * Lux + 1.0023) * Lux
    return Lux


try:
    Sensor = ConfigureSensor(
        ALS_GAIN["gain2"],
        ALS_IT["IT200"]
    )
except Exception as Error:
    print("an error occured:", Error)
    raise
Sensor.AlterGain()
Sensor.AlterIT()

# Send the settings to the sensor over I2C.
i2c.init()
i2c.write(
    VEML7700,
    bytes([ALS_CONF,
        Config & 0xFF,
        (Config >> 8) & 0xFF
    ]))

# Wait for button A before starting the measurements.
while not A.is_pressed():
    t.sleep(1)

with open("data.txt", "a") as DataFile:
    with open("lux.txt", "a") as LuxFile:
        with open("time_per_datapoint.txt", "a") as TimeFile:
            RunStartMS = running_time()
            PreviousSampleMS = RunStartMS

            # Keep taking readings until A and B are pressed together.
            while not (A.is_pressed() and B.is_pressed()):
                i2c.write(VEML7700, bytes([0x04]), repeat=True)
                Data = i2c.read(VEML7700, 2)
                RawReading = Data[0] | (Data[1] << 8)
                Lux = RawToLux(RawReading)
                SampleTimeMS = running_time()

                DataFile.write(str(RawReading) + "\n")
                LuxFile.write("{:.4f}\n".format(Lux))
                TimeFile.write(
                    str(SampleTimeMS - PreviousSampleMS) + "\n"
                )
                PreviousSampleMS = SampleTimeMS

                # Pause between readings so the sensor can take another measurement.
                t.sleep_ms(200)

            RuntimeMS = running_time() - RunStartMS

with open("runtime.txt", "a") as RuntimeFile:
    RuntimeFile.write(str(RuntimeMS) + "\n")

Config = Config | 0b1
i2c.write(VEML7700, bytes([ALS_CONF,
    Config & 0xFF,
    (Config >> 8) & 0xFF]))
display.show(Image.HEART)
t.sleep(1)