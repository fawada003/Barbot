
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

    
def sync():
    GPIO.setmode(GPIO.BCM)

    ms = (-1, -1, -1)  # sets micro step GPIO not necessary so -1  B
    Xdirection = 20  # GPIO to dir
    Xstep = 21  # GPIO to step
    Xenable = 3  # GPIO to enable or disable stepper bord via logic low = enabled high = disabled
    Xaxis = RpiMotorLib.A4988Nema(Xdirection, Xstep, ms, "A4988")

    Ydirection = 26  # GPIO to dir
    Ystep = 19  # GPIO to step
    Yenable = 2  # GPIO to enable or disable stepper bord via logic low = enabled high = disabled
    Yaxis = RpiMotorLib.A4988Nema(Ydirection, Ystep, ms, "A4988")

    syncbuttonX = 22  # GPIO for button that syncs the x-axis motor
    syncbuttonY = 17  # GPIO for button that syncs the Y-axis motor
    GPIO.setup(syncbuttonY, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button
    GPIO.setup(syncbuttonX, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button
    GPIO.setup(Xenable, GPIO.OUT)
    GPIO.setup(Yenable, GPIO.OUT)    
    GPIO.output(Yenable, GPIO.LOW)
    while(GPIO.input(syncbuttonY) == GPIO.HIGH):
       print("SYNCY")
       Yaxis.motor_go(True, "Full", 5, .001, False, .05)
    
    GPIO.output(Yenable, GPIO.HIGH)
   
    GPIO.output(Xenable, GPIO.LOW)
    while(GPIO.input(syncbuttonX) == GPIO.HIGH):
        print("syncX")
        Xaxis.motor_go(False, "Full", 8, .001, False, .05)
    
    GPIO.output(Xenable, GPIO.HIGH)

   

    GPIO.cleanup()

