#!/usr/bin/python3

import sys
import select

# The main concept of the application is a state object that contain the current state of the
# machine: be it idle or currently washing.

# A state is define (for the moment) as a 3-tuple
# (name :: String, desiredWaterLevel :: Double, currentWaterLevel :: Double)
# where water levels are number between 0.0 and 1.0
idleState = ("idle", 0, 0)

states = {
    "cotton" : ("cotton", 0.0, 0.0),
    "disinfection" : ("disinfection", 0.5, 0.0),
    "rough" : ("rough", 0.0, 0.0),
    "soaking-spinning" : ("soaking-spinning", 1.0, 0.0),
    "synthetic" : ("synthetic", 0.0, 0.0)
}

# The differents states can respond to different inputs. Those can be time related (e.g. timed
# passed and we now need to switch from soaking to spinning), sensor related (e.g. the water sensor
# indicate that the water tank is full) or user related (e.g. the user push the stop button).
#
# Those input are represent as function that receive a state, some input informations and produce
# a new state corresponding to the responce of the system (e.g. if the desired water capacity is
# achieved, the function could trigger an output to stop the water valve and return a new state
# where we start to add soap.
def timePassed(state, delta=1.0):
    return state

def waterSensor(state, value = 1.0):
    return (
        "{}-water-sensor".format(state[0]),
        state[1],
        state[2]
    )

def stop(state):
    return idleState

# Helper functions
def showPrompt(state):
    print("{}> ".format(state[0]), end="")
    sys.stdout.flush()

inputs = {
    "water-sensor" : waterSensor,
    "stop" : stop
}

# The main loop will wait for inputs and execute them on the state. Furthermore, it will trigger
# a time input every 0.1 second to let the state evolve with time.
#
# You can quit the main loop by pressing Ctrl-d
state = idleState
print("Road Runner : Machine à laver")
showPrompt(state)
eof = False
while not eof:
    (r,w,e) = select.select([sys.stdin],[],[],0.1)
    if not r:
        state = timePassed(state)
    else:
        command = sys.stdin.readline().strip()
        if not command:
            eof = True;
            print() # Insert a newline before to quit
        elif command in states:
            state = states[command]
            showPrompt(state)
        elif command in inputs:
            state = inputs[command](state)
            showPrompt(state)
        else:
            print("Unknow command: '{}'".format(command))
            showPrompt(state)

