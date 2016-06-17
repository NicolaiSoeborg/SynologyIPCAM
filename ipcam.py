#!/usr/bin/env python3

##########################
PIN_sensorA = 0          # Sensor A. Activated => 1
PIN_bell = 1             # Bell. Press => 1
PIN_door = 2             # Door. Closed => 1
PIN_sensorB = 3          # Sensor B. Activated => 1
#SETTLE_TIME = 5.0       # Wait 5 sec between reqs
##########################
import sys, time, datetime
from subprocess import call
from sys import exit

import pifacedigitalio
pifacedigitalio.init()

def log(txt, die = False):
    t = datetime.datetime.now().strftime("%Y/%b/%d %H:%M:%S")
    print("[%s] %s" % (t,txt))
    if die: sys.exit()

def get_val(pin):
    global pifacedigitalio
    return pifacedigitalio.digital_read(pin)

def get_event():
    if get_val(PIN_bell) == 1:
        return (True, 4, "Door bell")
    if get_val(PIN_door) == 1:
        # These rules apply, if door is closed (PIN_door == 1)
        if get_val(PIN_sensorA) == 1:
            return (True, 3, "Sensor A")
        if get_val(PIN_sensorB) == 1:
               return (True, 5, "Sensor B")
    return (False, 0, "Nothing")

#pfd = pifacedigitalio.PiFaceDigital()
#listener = pifacedigitalio.InputEventListener(chip=pifacedigitalio)
#for i in range(8): listener.register(i, pifacedigitalio.IODIR_BOTH, iodir_on_pin), SETTLE_TIME)
#listener.activate()

try:
    log("Process is active.")
    while True:
        alarm, eventId, eventName = get_event()
        if alarm:
            log("ALERT: %s." % eventName)
            call(["./trigger.py", str(eventId)])
            #sys.stdout.flush() # Not needed when using tmux
        time.sleep(0.1) # busy-waiting is stupid, but InputEventListener does not work on my PiFace

except KeyboardInterrupt:
    log("KeyboardInterrupt!")
except:
    log("Got unknown exception!?")

log("Ending.")
#listener.deactivate()
pifacedigitalio.deinit() # disables interrupts and closes the file
