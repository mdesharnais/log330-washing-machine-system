#!/usr/bin/python3

import copy
import sys

# The main concept of the application is a state object that contain the current state of the
# machine: be it idle or currently washing.

class IddleState:
    pass

class CottonState:
    def __init__(self):
        self.currentWaterLevel = 0.0
        self.desiredWaterLevel = 0.2
        self.soapWaterLevel = 0.2
        self.washingDuration = 45.0
        self.spinningDuration = 10.0
        self.soapDuration = 0.1
        self.isWashing = False
        self.isSpinning = False
        self.isSoapValveOpened = False
        self.isColdWaterValveOpened = False
        self.isHotWaterValveOpened = False
        self.washingStartedTime = 0.0
        self.spinningStartedTime = 0.0
        self.soapStartedTime = 0.0

    def __str__(self):
        # Highly boilerplate code and very hard to keep in sync with actual class definition.
        # Is there a way to automatically generate a __str__ member function?
        return ("CottonState {{ " +
            "currentWaterLevel = {:.2f}, " +
            "desiredWaterLevel = {:.2f}, " +
            "soapWaterLevel = {:.2f}, " +
            "washingDuration = {:.2f}, " +
            "spinningDuration = {:.2f}, " +
            "soapDuration = {:.2f}, " +
            "isWashing = {}, " +
            "isSpinning = {}, " +
            "isSoapValveOpened = {}, " +
            "isColdWaterValveOpened = {}, " +
            "isHotWaterValveOpened = {}, " +
            "washingStartedTime = {:.2f}, " +
            "spinningStartedTime = {:.2f} " +
            "soapStartedTime = {:.2f} " +
            "}}").format(
            self.currentWaterLevel,
            self.desiredWaterLevel,
            self.soapWaterLevel,
            self.washingDuration,
            self.spinningDuration,
            self.soapDuration,
            self.isWashing,
            self.isSpinning,
            self.isSoapValveOpened,
            self.isColdWaterValveOpened,
            self.isHotWaterValveOpened,
            self.washingStartedTime,
            self.spinningStartedTime,
            self.soapStartedTime)

# Those input are represent as function that receive a state, some input informations and produce
# a new state corresponding to the responce of the system (e.g. if the desired water capacity is
# achieved, the function could trigger an output to stop the water valve and return a new state
# where we start to add soap.

def cottonButtonPushed(time, state):
    newState = CottonState()
    #print(newState)
    return newState

def startButtonPushed(time, state):
    newState = copy.deepcopy(state)
    newState.isColdWaterValveOpened = True
    newState.isHotWaterValveOpened = True
    print("{:.2f} ColdWaterValve opened".format(time))
    print("{:.2f} HotWaterValve opened".format(time))
    #print(newState)
    return newState

def waterLevelButtonPushed(time, state):
    newState = copy.deepcopy(state)

    if newState.desiredWaterLevel == 1.0:
        newState.desiredWaterLevel = 0.0

    newState.desiredWaterLevel += 0.2

    #print(newState)
    return newState

def waterLevelSensorLevel(time, state, level):
    newState = copy.deepcopy(state)
    newState.currentWaterLevel = float(level)

    if newState.soapStartedTime == 0.0 and newState.currentWaterLevel >= newState.soapWaterLevel:
        newState.isSoapValveOpened = True
        newState.soapStartedTime = time
        print("{:.2f} SoapValve opened".format(time))

    if newState.currentWaterLevel == newState.desiredWaterLevel:
        newState.isColdWaterValveOpened = False
        newState.isHotWaterValveOpened = False
        print("{:.2f} ColdWaterValve closed".format(time))
        print("{:.2f} HotWaterValve closed".format(time))
        newState.isWashing = True
        newState.washingStartedTime = time
        print("{:.2f} Washing started".format(time))

    #print(newState)
    return newState

def timePassed(time, state):
    newState = copy.deepcopy(state)

    if newState.isSoapValveOpened and time >= (state.soapStartedTime + state.soapDuration):
        newState.isSoapValveOpened = False
        print("{:.2f} SoapValve closed".format(time))

    if state.isWashing and time >= (state.washingStartedTime + state.washingDuration):
        newState.isWashing = False
        print("{:.2f} Washing ended".format(time))
        newState.isSpinning = True
        newState.spinningStartedTime = time
        print("{:.2f} Spinning started".format(time))
    elif state.isSpinning and time >= (state.spinningStartedTime + state.spinningDuration):
        newState.isSpinning = False
        print("{:.2f} Spinning ended".format(time))
        
    return newState

def finalStateMessage(state):
    #return state.__class__.__name__
    return state.__str__()

commands = {
    "cotton-button" : {
        "pushed" : cottonButtonPushed
    },
    "start-button" : {
        "pushed" : startButtonPushed
    },
    "water-level-button" : {
        "pushed" : waterLevelButtonPushed
    },
    "water-level-sensor" : {
        "level" : waterLevelSensorLevel
    },
}

def parseCommand(line):
    # Format is as follow:
    # <time-in-minutes :: Double> <component> <signal> <args0> <arg1> ... <argN>
    words = line.split()
    time = float(words[0])
    component = words[1]
    message = words[2]
    args = words[3:]
    command = lambda time, state: commands[component][message](time, state, *args)
    return (time, command)

def runWashingMachineWithTime(time, endTime, state):
    # We update the state every 0.25 minutes = 15 seconds until we reach the end time
    delta = 0.2
    if time + delta < endTime:
        return runWashingMachineWithTime(time + delta, endTime, timePassed(time, state))
    else:
        return state

def runWashingMachine(inputStream, time, state):
    line = inputStream.readline()
    if not line:
        # Run for 120 minutes after the last command to let any ongoing cycle terminate
        return runWashingMachineWithTime(time, time + 120.0, state)
    else:
        (commandTime,commandFunction) = parseCommand(line)

        # Run for the time between the two last commands
        tempState = runWashingMachineWithTime(time, commandTime, state)

        # Run the command
        newState = commandFunction(commandTime, tempState)
        return runWashingMachine(inputStream, commandTime, newState)

if len(sys.argv) != 2:
    print("Usage: washing-machine <test-file>")
else:
    endState = runWashingMachine(open(sys.argv[1]), 0.0, IddleState())
    print(finalStateMessage(endState))
