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
        self.washingDuration = 45.0
        self.spinningDuration = 10.0
        self.isStarted = False
        self.isColdWaterValveOpened = False
        self.isHotWaterValveOpened = False

    def __str__(self):
        # Highly boilerplate code and very hard to keep in sync with actual class definition.
        # Is there a way to automatically generate a __str__ member function?
        return ("CottonState {{ " +
            "currentWaterLevel = {:.1f}, " +
            "desiredWaterLevel = {:.1f}, " +
            "washingDuration = {:.1f}, " +
            "spinningDuration = {:.1f}, " +
            "isStarted = {}, " +
            "isColdWaterValveOpened = {}, " +
            "isHotWaterValveOpened = {} " +
            "}}").format(
            self.currentWaterLevel,
            self.desiredWaterLevel,
            self.washingDuration,
            self.spinningDuration,
            self.isStarted,
            self.isColdWaterValveOpened,
            self.isHotWaterValveOpened)

# Those input are represent as function that receive a state, some input informations and produce
# a new state corresponding to the responce of the system (e.g. if the desired water capacity is
# achieved, the function could trigger an output to stop the water valve and return a new state
# where we start to add soap.

def cottonButtonPushed(state):
    newState = CottonState()
    print(newState)
    return newState

def startButtonPushed(state):
    newState = copy.deepcopy(state)
    newState.isStarted = True
    newState.isColdWaterValveOpened = True
    newState.isHotWaterValveOpened = True
    print("ColdWaterValve opened")
    print("HotWaterValve opened")
    print(newState)
    return newState

def waterLevelButtonPushed(state):
    newState = copy.deepcopy(state)

    if newState.desiredWaterLevel == 1.0:
        newState.desiredWaterLevel = 0.0

    newState.desiredWaterLevel += 0.2

    print(newState)
    return newState

def waterLevelSensorLevel(state, level):
    newState = copy.deepcopy(state)
    newState.currentWaterLevel = float(level)

    if newState.currentWaterLevel == newState.desiredWaterLevel:
        newState.isColdWaterValveOpened = False
        newState.isHotWaterValveOpened = False
        print("ColdWaterValve closed")
        print("HotWaterValve closed")

    print(newState)
    return newState

def timePassed(state, time):
    # print("timePassed {}".format(time))
    return state

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
    command = lambda state: commands[component][message](state, *args)
    return (time, command)

def runWashingMachineWithTime(time, endTime, state):
    # We update the state every 0.25 minutes = 15 seconds until we reach the end time
    delta = 0.25
    if time + delta < endTime:
        return runWashingMachineWithTime(time + delta, endTime, timePassed(state, time))
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
        newState = commandFunction(tempState)
        return runWashingMachine(inputStream, commandTime, newState)

if len(sys.argv) != 2:
    print("Usage: washing-machine <test-file>")
else:
    endState = runWashingMachine(open(sys.argv[1]), 0.0, IddleState())
    print(finalStateMessage(endState))
