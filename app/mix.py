import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
from time import sleep

def mix(query):  # module that activates the dispensers

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

    syncbuttonY = 17  # GPIO for button that syncs the Y-axis motor
    GPIO.setup(syncbuttonY, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button
    syncbuttonX = 22 # GPIO for button that syncs the x-axis motor
    GPIO.setup(syncbuttonX, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button
    GPIO.setup(Xenable, GPIO.OUT)
    GPIO.setup(Yenable, GPIO.OUT)

    Xpos = 0 # postition of x axis in steps
    FromAToB = 620  # the distance between two dispensers
    steps = 0  # calculatet steps that are going to be taken



    GPIO.output(Yenable, GPIO.LOW)
    while(GPIO.input(syncbuttonY) == GPIO.HIGH):
       print("SYNCY")
       Yaxis.motor_go(True, "Full", 5, .001, False, .05)
    
    GPIO.output(Yenable, GPIO.HIGH)
    # sets Xenable to Low therfore enabling the X motor
    GPIO.output(Xenable, GPIO.LOW)
    while(GPIO.input(syncbuttonX) == GPIO.HIGH):
        Xaxis.motor_go(False, "Full", 5, .001, False, .05)
    # sets Xenable to high therfore releasing the X motor
    GPIO.output(Xenable, GPIO.HIGH)

    # The List is sorted descending like 4321 because the paser only takes sorted input in form 4321
    query = sorted(query)
  
    print("sorted:...")
    print(sorted(query))
    GPIO.output(Xenable, GPIO.LOW)
        # goes to dispenser (xaxis)
    Xaxis.motor_go(True, "Full", 10, .0005, False, .05)
        # sets Xenable to high therfore releasing the X motor
    GPIO.output(Xenable, GPIO.HIGH)
    
    for position, count in query:

        steps = (FromAToB * position) - Xpos  # calculate steps needed
        Xpos = Xpos + steps  # update xpos
        print(steps)

        # sets Xenable to Low therfore enabling the X motor
        GPIO.output(Xenable, GPIO.LOW)
        # goes to dispenser (xaxis)
        Xaxis.motor_go(True, "Full", steps, .0005, False, .05)
        # sets Xenable to high therfore releasing the X motor
        GPIO.output(Xenable, GPIO.HIGH)

        for count in range(count):
            print("activate")
            # sets Xenable to LOW therfore activating the X motor
            GPIO.output(Yenable, GPIO.LOW)
            # Yaxis activates the dispenser (up)
            Yaxis.motor_go(False, "Full",1300, .001, False, .05)
            sleep(0.7)
            # Yaxis going down so program can continue
            Yaxis.motor_go(True, "Full", 1300, .001, False, .05)
            # sets Xenable to high therfore releasing the X motor
            GPIO.output(Yenable, GPIO.HIGH)

    # sets Xenable to Low therfore enabling the X motor
    GPIO.output(Xenable, GPIO.LOW)
    # goes back most of the way home
    Xaxis.motor_go(False, "Full", Xpos-5, .001, False, .05)    #symncs the y axis minus 630 steps cause 0 == 6
    while(GPIO.input(syncbuttonX) == GPIO.HIGH):
        Xaxis.motor_go(False, "Full", 5, .001, False, .05)
    # sets Xenable to high therfore releasing the X motor
    GPIO.output(Xenable, GPIO.HIGH)

    GPIO.cleanup()

# uncomment for testing
#query = [(5,1)]

#
#mix(query)
