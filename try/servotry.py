
from __future__ import division
import time

import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

servo_min = 150  # Change to find suitable servo pos.
servo_max = 400  

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

pwm.set_pwm_freq(60)

print('Moving servo on channel 0, press Ctrl-C to quit...')
while True:
    status = str(input(">>>>   "))
    if(status == 'hold'):
        pwm.set_pwm(0, 0, 600)
        pwm.set_pwm(1, 0, 100)
        pwm.set_pwm(2, 0, 600)
    if(status == 'up'):
        pwm.set_pwm(0, 0, 600)
        pwm.set_pwm(1, 0, 100)
        pwm.set_pwm(2, 0, 400)
    if(status == 'down'):
        pwm.set_pwm(0, 0, 600)
        pwm.set_pwm(1, 0, 100)
        pwm.set_pwm(2, 0, 600)
    if(status == 'rel'):
        pwm.set_pwm(0, 0, 100)
        pwm.set_pwm(1, 0, 600)
        pwm.set_pwm(2, 0, 600)
     