
import RPi.GPIO as GPIO
import time 
class Motor:
    PWM_FREQ = 50
    #STEP = 90 #rotate angle
    def __init__(self,CONTROL_PIN)  :     
        self.CONTROL_PIN = CONTROL_PIN
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.CONTROL_PIN, GPIO.OUT)
        self.pwm = GPIO.PWM(CONTROL_PIN, Motor.PWM_FREQ)
        self.pwm.start(0)
        print("Motor Set up already!!")
       
    def change_duty_cycle(self,angle):
        print('角度={: >3}'.format(angle))
        duty_cycle = (0.05 * Motor.PWM_FREQ) + (0.19 * Motor.PWM_FREQ * angle / 180)
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.3)