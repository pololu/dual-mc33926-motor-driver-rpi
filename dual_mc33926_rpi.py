import wiringpi2

# Motor speeds for this library are specified as numbers
# between -MAX_SPEED and MAX_SPEED, inclusive.
_max_speed = 480  # 19.2 MHz / 2 / 480 = 20 kHz
MAX_SPEED = _max_speed

io_initialized = False
def io_init():
  global io_initialized
  if io_initialized:
    return

  wiringpi2.wiringPiSetupGpio()
  wiringpi2.pinMode(12, wiringpi2.GPIO.PWM_OUTPUT)
  wiringpi2.pinMode(13, wiringpi2.GPIO.PWM_OUTPUT)

  wiringpi2.pwmSetMode(wiringpi2.GPIO.PWM_MODE_MS)
  wiringpi2.pwmSetRange(MAX_SPEED)
  wiringpi2.pwmSetClock(2)

  wiringpi2.pinMode(22, wiringpi2.GPIO.OUTPUT)
  wiringpi2.pinMode(23, wiringpi2.GPIO.OUTPUT)
  wiringpi2.pinMode(24, wiringpi2.GPIO.OUTPUT)
  wiringpi2.pinMode(25, wiringpi2.GPIO.OUTPUT)

  io_initialized = True

class Motor(object):
    MAX_SPEED = _max_speed

    def __init__(self, pwm_pin, dir_pin, en_pin):
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self.en_pin = en_pin

    def enable(self):
        io_init()
        wiringpi2.digitalWrite(self.en_pin, 1)

    def disable(self):
        io_init()
        wiringpi2.digitalWrite(self.en_pin, 0)

    def setSpeed(self, speed):
        if speed < 0:
            speed = -speed
            dir_value = 1
        else:
            dir_value = 0

        if speed > MAX_SPEED:
            speed = MAX_SPEED

        io_init()
        wiringpi2.digitalWrite(self.dir_pin, dir_value)
        wiringpi2.pwmWrite(self.pwm_pin, speed)

class Motors(object):
    MAX_SPEED = _max_speed

    def __init__(self):
        self.motor1 = Motor(12, 24, 22)
        self.motor2 = Motor(13, 25, 23)

    def enable(self):
        self.motor1.enable()
        self.motor2.enable()

    def disable(self):
        self.motor1.disable()
        self.motor2.disable()

    def setSpeeds(self, m1_speed, m2_speed):
        self.motor1.setSpeed(m1_speed)
        self.motor2.setSpeed(m2_speed)

motors = Motors()
