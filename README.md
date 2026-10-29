Yo

This is the repo where I'll organize and store all my TekForsk projects

Firstly, we have project 1: ToFLys(Teknologi og Forskningslære lysprosjekt)


1. The hardware used

  VEML7700
    
    VEML7700 is a high accuracy ambient light digital 16-bit
resolution sensor in a miniature transparent 6.8 mm x
2.35 mm x 3.0 mm package. It includes a high sensitive
photo diode, a low noise amplifier, a 16-bit A/D converter
and supports an easy to use I2C bus communication
interface


  Micro:bit

    A pocket-sized, programmable microcontroller board designed by the BBC to help students learn coding and physical computing


2. The firm-/software
  
  We have programmed the micro:bit in micropython by flashing the code from a computer onto the microbit. The flashed MicroPython (.hex) file communicates with the sensor via i2c (SDA and SCL cable)


3. Need-to-know terminology
  I²C (Inter-Integrated Circuit)
  
  A communication protocol used by the micro:bit to communicate with the VEML7700.

  
  Register
  
  A storage location inside the VEML7700 that holds configuration settings or measurement data.

  
  Register address
  
  A value identifying a specific register inside the sensor, such as 0x00 or 0x04.

  
  Bit field
  
  A group of bits within a register that controls a particular setting, such as gain or integration time.

  
  Bitwise operations
  
  Operations that manipulate individual bits, such as AND (&), OR (|) and NOT (~).

  
  Bit mask
  
  A binary pattern used to select, clear or modify specific bits.

  
  Bit shifting
  
  Moving bits left (<<) or right (>>) to position them correctly.

  
  Binary
  
  A base-2 number system using only 0 and 1. Python uses the prefix 0b for binary literals.

  
  Hexadecimal
  
  A base-16 number system using digits 0–9 and letters A–F. Python uses the prefix 0x.

  
  Gain
  
  A setting that adjusts the sensor's sensitivity to light and its measurable range.

  
  Integration time
  
  The period over which the sensor collects light for a measurement.

  
  Reserved bits
  
  Bits in a register whose values are specified or restricted by the manufacturer.

  
  ALS_CONF
  
  The register address for the VEML7700's ambient-light sensor configuration register.

  
  ALS_GAIN
  
  The name used for the gain setting or its corresponding value mapping in the code.

  
  ALS_IT
  
  The name used for the integration-time setting or its corresponding value mapping in the code.

  
  repeat=True
  
  An argument to i2c.write() that prevents a stop condition from being sent at the end of that write, allowing the following I²C operation to continue the transaction.

  
  LSB and MSB
  
  Least Significant Byte and Most Significant Byte: the lower and upper eight bits of a 16-bit value, respectively.

  
  Raw reading
  
  The numerical value read directly from the sensor before conversion into a physical unit such as lux.

  
  Sampling interval
  
  The time between successive measurements recorded by the program.

  
  Exception handling
  
  Managing runtime errors using Python constructs such as try, except and raise.

  
  Global variable
  
  A variable defined outside a function or method. The global keyword allows a function to assign to that variable.

  
  Bitwise complement
  
  The operation performed by ~, which inverts an integer's bits according to Python's integer semantics.