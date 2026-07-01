# MPU6050 MicroPython Library

A simple MicroPython library for interfacing with the **MPU6050** IMU (accelerometer + gyroscope + temperature sensor) over I2C. It works out of the box with breakout boards like the **GY-521**, and gives you easy access to acceleration, rotation, and temperature readings with just a few lines of code.

## What is the MPU6050?

The MPU6050 is a 6-axis motion tracking sensor. It combines:
- A **3-axis accelerometer** (measures acceleration/tilt along X, Y, Z)
- A **3-axis gyroscope** (measures rotation speed along X, Y, Z)
- A built-in **temperature sensor**

This library talks to the sensor over **I2C** and handles all the low-level register reads/writes for you, so you can just call a function and get real, calibrated values back.

## Features

- Simple setup — just pass in your I2C object and the sensor's address
- Configurable **accelerometer range**: ±2g, ±4g, ±8g, ±16g
- Configurable **gyroscope range**: ±250°/s, ±500°/s, ±1000°/s, ±2000°/s
- Configurable **digital low-pass filter** for smoother readings
- One function call (`take_measurements()`) returns everything: acceleration (g), temperature (°C), and rotation (°/s)
- Automatically checks that a real MPU6050 is connected when you create the sensor object

## Wiring Notes

If you're using a **GY-521** breakout board with the **AD0 pin grounded**, the sensor's I2C address will be `0x68`. (If AD0 is instead connected to 3.3V, the address becomes `0x69`.)

Connect:
- `SCL` → any I2C-capable pin on your board
- `SDA` → any I2C-capable pin on your board
- `VCC` → 3.3V
- `GND` → GND

## Installation

1. Copy `imu.py` onto your MicroPython board (using [Thonny](https://thonny.org/), `mpremote`, `ampy`, or your tool of choice).
2. Import it in your own code with `from imu import Mpu6050`.

## Quick Start

```python
from machine import Pin, I2C
from utime import sleep
from imu import Mpu6050

# Set up I2C
mpu_6050 = I2C(1, scl=Pin(27), sda=Pin(26), freq=400000)

# Create the sensor object (0x68 because AD0 is grounded)
imu_sensor = Mpu6050(mpu_6050, 0x68)

while True:
    readings = imu_sensor.take_measurements()
    print(f"accel_x: {readings[0]} g, accel_y: {readings[1]} g, accel_z: {readings[2]} g")
    sleep(1)
```

`take_measurements()` always returns a tuple of 7 values, in this order:

| Index | Value | Unit |
|-------|-------|------|
| 0 | Acceleration X | g |
| 1 | Acceleration Y | g |
| 2 | Acceleration Z | g |
| 3 | Temperature | °C |
| 4 | Gyroscope X | °/s |
| 5 | Gyroscope Y | °/s |
| 6 | Gyroscope Z | °/s |

## API Reference

| Method | Description |
|--------|-------------|
| `Mpu6050(i2c, ADDR)` | Creates the sensor object. `i2c` is your I2C object, `ADDR` is the sensor's I2C address (usually `0x68`). Raises an error if no MPU6050 is found. |
| `config_filter(freq)` | Sets the digital low-pass filter bandwidth. Accepts `256`, `188`, `98`, `42`, `20`, `10`, or `5` (Hz). |
| `config_gyro(gyro_range)` | Sets the gyroscope's full-scale range. Accepts `250`, `500`, `1000`, or `2000` (°/s). |
| `config_accel(accel_range)` | Sets the accelerometer's full-scale range. Accepts `2`, `4`, `8`, or `16` (g). |
| `take_measurements()` | Reads and returns all 7 values (acceleration x/y/z, temperature, gyro x/y/z) as a tuple. |

## Examples

Two ready-to-run example scripts are included in the [`examples/`](./examples) folder of this repository:

### `example1_default_config.py`
This is the simplest way to use the library. It creates the sensor object and starts taking readings **without changing any settings**, so the sensor runs on its default configuration (±2g accelerometer range, ±250°/s gyroscope range). Good starting point if you just want to confirm your sensor is working.

### `example2_custom_config.py`
This example shows how to **customize the sensor's behavior** before reading data. It configures:
- The digital filter to 188 Hz
- The gyroscope range to ±1000°/s
- The accelerometer range to ±4g

Use this as a template when your project needs a wider measurement range (e.g. detecting fast rotations or high-g accelerations) or smoother filtered data.

Both examples print live sensor readings once per second and can be run directly on your MicroPython board.

## License

MIT License — free to use, modify, and share.
