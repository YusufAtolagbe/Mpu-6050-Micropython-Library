import time

###CONSTANTS(REGISTERS)
WHO_AM_I = 0x75

PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19

GYRO_CONFIG = 0x1B

ACCEL_CONFIG = 0x1C

CONFIG = 0x1A

ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40

TEMP_OUT_H = 0x41
TEMP_OUT_L = 0x42
GYRO_XOUT_H = 0x43
GYRO_XOUT_L = 0x44
GYRO_YOUT_H = 0x45
GYRO_YOUT_L = 0x46
GYRO_ZOUT_H = 0x47
GYRO_ZOUT_L = 0x48


class Mpu6050:
    # Initialization function, initialize pins and set up device
    def __init__(self, i2c, ADDR):
        self.ADDR = ADDR
        self.i2c = i2c
        # confirm sensor availabilty
        try:
            self.ADDR = self.i2c.readfrom_mem(self.ADDR, WHO_AM_I, 1)[0]
            if self.ADDR != 0x68 and self.ADDR != 0x69:
                raise ValueError("Wrong sensor")
            
        except OSError:
            raise OSError("MPU6050 not found")

        
        self._buf = bytearray(14)   #buffer for storing measurements values

        self.i2c.writeto_mem(self.ADDR, PWR_MGMT_1, bytes([0x00]))
        time.sleep_ms(100)
       
        self.i2c.writeto_mem(self.ADDR, CONFIG, bytes([0x04]))

        self.i2c.writeto_mem(self.ADDR, SMPLRT_DIV, bytes([9]))  

        self.i2c.writeto_mem(self.ADDR, GYRO_CONFIG, bytes([0x00]))

        # Accelerometer range: write 00 to 0x1C(AFS_SEL) to set the range to ±2g
        self.i2c.writeto_mem(self.ADDR, ACCEL_CONFIG, bytes([0x00]))

        # set accelerometer and gyro calibration values
        self.accel_scale = 1 / 16384  # ±2g
        self.gyro_scale = 1 / 131  # ±250°/s


#####FUNCTIONS########

    def config_filter(self, freq):		#configure digital filter

        if freq == 256:
            val = 0x00

        elif freq == 188:
            val = 0x01

        elif freq == 98:
            val = 0x02

        elif freq == 42:
            val = 0x03

        elif freq == 20:
            val = 0x04

        elif freq == 10:
            val = 0x05

        elif freq == 5:
            val = 0x06

        else:
            raise ValueError("Invalid filter frequency")

        self.i2c.writeto_mem(self.ADDR, CONFIG, bytes([val]))


    def config_gyro(self, gyro_range):		#configure gyroscope full scale range 

        if gyro_range == 250:
            reg_val = 0x00
            self.gyro_scale = 1 / 131

        elif gyro_range == 500:
            reg_val = 0x08
            self.gyro_scale = 1 / 65.5

        elif gyro_range == 1000:
            reg_val = 0x10
            self.gyro_scale = 1 / 32.8

        elif gyro_range == 2000:
            reg_val = 0x18
            self.gyro_scale = 1 / 16.4

        else:
            raise ValueError("Invalid gyro range")

        self.i2c.writeto_mem(self.ADDR, GYRO_CONFIG, bytes([reg_val]))


    def config_accel(self, accel_range):		#configure accelerometer full scale range

        if accel_range == 2:
            regc_val = 0x00
            self.accel_scale = 1 / 16384

        elif accel_range == 4:
            regc_val = 0x08
            self.accel_scale = 1 / 8192

        elif accel_range == 8:
            regc_val = 0x10
            self.accel_scale = 1 / 4096

        elif accel_range == 16:
            regc_val = 0x18
            self.accel_scale = 1 / 2048

        else:
            raise ValueError("Invalid accel range")

        self.i2c.writeto_mem(self.ADDR, ACCEL_CONFIG, bytes([regc_val]))


    def take_measurements(self):
        # Take measurements


        self.i2c.readfrom_mem_into(self.ADDR, ACCEL_XOUT_H, self._buf)

        # unpack each 16-bit(two bytes) value
        ax = (self._buf[0] << 8) | self._buf[1]
        ay = (self._buf[2] << 8) | self._buf[3]
        az = (self._buf[4] << 8) | self._buf[5]
        temp = (self._buf[6] << 8) | self._buf[7]
        gx = (self._buf[8] << 8) | self._buf[9]
        gy = (self._buf[10] << 8) | self._buf[11]
        gz = (self._buf[12] << 8) | self._buf[13]
        
        #Two complement values
        ax = ax - 65536 if ax & 0x8000 else ax
        ay = ay - 65536 if ay & 0x8000 else ay
        az = az - 65536 if az & 0x8000 else az
        temp = temp - 65536 if temp & 0x8000 else temp
        gx = gx - 65536 if gx & 0x8000 else gx
        gy = gy - 65536 if gy & 0x8000 else gy
        gz = gz - 65536 if gz & 0x8000 else gz

        # Calibration

        ax *= self.accel_scale
        ay *= self.accel_scale
        az *= self.accel_scale

        temp = (temp / 340) + 36.53

        gx *= self.gyro_scale
        gy *= self.gyro_scale
        gz *= self.gyro_scale

        return ax, ay, az, temp, gx, gy, gz





