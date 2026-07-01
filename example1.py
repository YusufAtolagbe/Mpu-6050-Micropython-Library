"""
Examlpe code for interfacing with the mpu6050 using this library
This code uses the micropython i2c library to interface with the mpu6050 sensor module on a low level.
In the gy521 breakout board, the ADO0 pin is grounded, making the device i2c addres 0x68

"""


######LIBRARIES AND IMPORTS#######
from machine import Pin, I2C
from utime import sleep
from imu import Mpu6050

#create an object of the i2c library
mpu_6050 = I2C(1, scl=Pin(27), sda=Pin(26), freq=400000)

#create object of the Mpu6050 class
imu_sensor = Mpu6050(mpu_6050, 0x68)

#Take readings
while True:
        
    readings = imu_sensor.take_measurements()
    print(f"accel_x: {readings[0]} g,\t"
        f"accel_y: {readings[1]} g,\t"
        f"accel_z: {readings[2]} g,\n"
        f"temp: {readings[3]} celcius,\n"
        f"gyro_x: {readings[4]} °/s,\t"
        f"gyro_y: {readings[5]} °/s,\t"
        f"gyro_z: {readings[6]} °/s,")
        
    sleep(1) #delay 1 sec
        


