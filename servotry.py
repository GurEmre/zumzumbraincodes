#simple test icine bak

pwm.set_pwm_freq(60)

while True:
    pwm.set_pwm(0,0,servo_min)
    time.sleep(1)
    pwm.set_pwm(0,0,servo_max)
    time.sleep(1)

    pwm.set_pwm(1,0,servo_min)
    time.sleep(1)
    pwm.set_pwm(1,0,servo_max)
    time.sleep(1)

    pwm.set_pwm(2,0,servo_min)
    time.sleep(1)
    pwm.set_pwm(2,0,servo_max)
    time.sleep(1)