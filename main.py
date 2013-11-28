#!/usr/bin/python3

import copy
import sys
from time import sleep

# 0x200 = 2 * (8 bits + 1 newline) = 18
def offsetOfMemoryAddress(address):
    return (address >> 8) * 9

def readMemoryAddress(address):
    memory = open("memory", "r")
    memory.seek(offsetOfMemoryAddress(address));
    return int(memory.read(8), 2)

def writeMemoryAddress(address, byte):
    memory = open("memory", "r+")
    memory.seek(offsetOfMemoryAddress(address));
    memory.write("{:0>8b}".format(byte));

# The main concept of the application is a state object that contain the current state of the
# machine: be it idle or currently washing.

class IddleState:
    pass

class WashingState:
    def __init__(self):
        self.currentWaterLevel = 0.0
        self.desiredWaterLevel = 0.2
        self.soapWaterLevel = 0.2
        self.bleachWaterLevel = 1.0
        self.fabricSoftenerWashingDelta = -5.0
        self.washingDuration = 45.0
        self.spinningDuration = 10.0
        self.soapDuration = 0.1
        self.bleachDuration = 0.1
        self.fabricSoftenerDuration = 0.1
        self.isWashing = False
        self.isSpinning = False
        self.isSoapValveOpened = False
        self.isBleachValveOpened = False
        self.isFabricSoftenerValveOpened = False
        self.isColdWaterValveOpened = False
        self.isHotWaterValveOpened = False
        self.washingStartedTime = 0.0
        self.spinningStartedTime = 0.0
        self.soapStartedTime = 0.0
        self.bleachStartedTime = 0.0
        self.fabricSoftenerStartedTime = 0.0

    def __str__(self):
        # Highly boilerplate code and very hard to keep in sync with actual class definition.
        # Is there a way to automatically generate a __str__ member function?
        return ("WashingState {{ " +
            "currentWaterLevel = {:.2f}, " +
            "desiredWaterLevel = {:.2f}, " +
            "soapWaterLevel = {:.2f}, " +
            "bleachWaterLevel = {:.2f}, " +
            "fabricSoftenerWashingDelta = {:.2f}, " +
            "washingDuration = {:.2f}, " +
            "spinningDuration = {:.2f}, " +
            "soapDuration = {:.2f}, " +
            "bleachDuration = {:.2f}, " +
            "fabricSoftenerDuration = {:.2f}, " +
            "isWashing = {}, " +
            "isSpinning = {}, " +
            "isSoapValveOpened = {}, " +
            "isBleachValveOpened = {}, " +
            "isFabricSoftenerValveOpened = {}, " +
            "isColdWaterValveOpened = {}, " +
            "isHotWaterValveOpened = {}, " +
            "washingStartedTime = {:.2f}, " +
            "spinningStartedTime = {:.2f} " +
            "soapStartedTime = {:.2f} " +
            "bleachStartedTime = {:.2f} " +
            "fabricSoftenerStartedTime = {:.2f} " +
            "}}").format(
            self.currentWaterLevel,
            self.desiredWaterLevel,
            self.soapWaterLevel,
            self.bleachWaterLevel,
            self.fabricSoftenerWashingDelta,
            self.washingDuration,
            self.spinningDuration,
            self.soapDuration,
            self.bleachDuration,
            self.fabricSoftenerDuration,
            self.isWashing,
            self.isSpinning,
            self.isSoapValveOpened,
            self.isBleachValveOpened,
            self.isFabricSoftenerValveOpened,
            self.isColdWaterValveOpened,
            self.isHotWaterValveOpened,
            self.washingStartedTime,
            self.spinningStartedTime,
            self.soapStartedTime,
            self.bleachStartedTime,
            self.fabricSoftenerStartedTime)

# Those input are represent as function that receive a state, some input informations and produce
# a new state corresponding to the responce of the system (e.g. if the desired water capacity is
# achieved, the function could trigger an output to stop the water valve and return a new state
# where we start to add soap.

def cottonButtonPushed(time, state):
    writeMemoryAddress(0x0200, readMemoryAddress(0x0200) | 0b00100000)
    newState = WashingState()
    newState.washingDuration = 45.0
    newState.spinningDuration = 10.0
    return newState

def disinfectionButtonPushed(time, state):
    writeMemoryAddress(0x0700, readMemoryAddress(0x0700) | 0b00000001)
    newState = WashingState()
    newState.washingDuration = 45.0
    newState.spinningDuration = 10.0
    newState.desiredWaterLevel = 0.5
    return newState

def roughButtonPushed(time, state):
    writeMemoryAddress(0x0200, readMemoryAddress(0x0200) | 0b10000000)
    newState = WashingState()
    newState.washingDuration = 45.0
    newState.spinningDuration = 10.0
    return newState

def soakingSpinningButtonPushed(time, state):
    writeMemoryAddress(0x0700, readMemoryAddress(0x0700) | 0b00100000)
    newState = WashingState()
    newState.washingDuration = 10.0
    newState.spinningDuration = 15.0
    newState.soapStartedTime = -1.0
    newState.bleachStartedTime = -1.0
    newState.fabricSoftenerStartedTime = -1.0
    newState.desiredWaterLevel = 1.0
    return newState

def syntheticButtonPushed(time, state):
    writeMemoryAddress(0x0200, readMemoryAddress(0x0200) | 0b01000000)
    newState = WashingState()
    newState.washingDuration = 30.0
    newState.spinningDuration = 5.0
    return newState

def startButtonPushed(time, state):
    writeMemoryAddress(0x0200, readMemoryAddress(0x0200) | 0b00010000);
    newState = copy.deepcopy(state)

    newState.isColdWaterValveOpened = True
    writeMemoryAddress(0x0100, readMemoryAddress(0x0100) | 0b00000100);
    print("{:.2f} ColdWaterValve opened".format(time))

    newState.isHotWaterValveOpened = True
    writeMemoryAddress(0x0100, readMemoryAddress(0x0100) | 0b00001000);
    print("{:.2f} HotWaterValve opened".format(time))

    return newState

def waterLevelButtonPushed(time, state):
    newState = copy.deepcopy(state)

    if newState.desiredWaterLevel == 1.0:
        newState.desiredWaterLevel = 0.0

    newState.desiredWaterLevel += 0.2

    writeMemoryAddress(0x0200, (readMemoryAddress(0x0200) & 0b11110000) | int(newState.desiredWaterLevel * 10));

    return newState

def waterLevelSensorLevel(time, state, level):
    newState = copy.deepcopy(state)
    newState.currentWaterLevel = float(level)
    # A water level of 0.5 is translate in the following way:
    # (0b???????? & 0b11100001) | (int(0.5 * 10) << 1)
    # (0b???????? & 0b11100001) | (int(5.0) << 1)
    # (0b???????? & 0b11100001) | (5 << 1)
    # (0b???????? & 0b11100001) | (0b00000101 << 1)
    # (0b???????? & 0b11100001) | 0b00001010
    # 0b???0000? | 0b00001010
    # 0b???1010?
    writeMemoryAddress(0x0700, (readMemoryAddress(0x0700) & 0b11100001) | (int(newState.currentWaterLevel * 10) << 1));

    if newState.soapStartedTime == 0.0 and newState.currentWaterLevel >= newState.soapWaterLevel:
        newState.isSoapValveOpened = True
        newState.soapStartedTime = time
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) | 0b00010000);
        print("{:.2f} SoapValve opened".format(time))
        sleep(2.5)

    if newState.bleachStartedTime == 0.0 and newState.currentWaterLevel >= newState.bleachWaterLevel:
        newState.isBleachValveOpened = True
        newState.bleachStartedTime = time
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) | 0b00100000);
        print("{:.2f} BleachValve opened".format(time))
        sleep(2.5)

    if newState.currentWaterLevel == newState.desiredWaterLevel:
        newState.isColdWaterValveOpened = False
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) & 0b11111011);
        print("{:.2f} ColdWaterValve closed".format(time))

        newState.isHotWaterValveOpened = False
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) & 0b11110111);
        print("{:.2f} HotWaterValve closed".format(time))
        newState.isWashing = True

        newState.washingStartedTime = time
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) | 0b00000001);
        print("{:.2f} Washing started".format(time))

    return newState

def timePassed(time, state):
    newState = copy.deepcopy(state)

    if newState.isSoapValveOpened and time >= (newState.soapStartedTime + newState.soapDuration):
        newState.isSoapValveOpened = False
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) & 0b11101111);
        print("{:.2f} SoapValve closed".format(time))

    if newState.isBleachValveOpened and time >= (newState.bleachStartedTime + newState.bleachDuration):
        newState.isBleachValveOpened = False
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) & 0b11011111);
        print("{:.2f} BleachValve closed".format(time))

    if newState.isFabricSoftenerValveOpened and time >= (newState.fabricSoftenerStartedTime + newState.fabricSoftenerDuration):
        newState.isFabricSoftenerValveOpened = False
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) & 0b10111111);
        print("{:.2f} FabricSoftener closed".format(time))

    if newState.isWashing and newState.fabricSoftenerStartedTime == 0.0:
        if newState.fabricSoftenerWashingDelta >= 0.0:
            t = newState.washingStartedTime + newState.fabricSoftenerWashingDelta
        else:
            t = (newState.washingStartedTime + newState.washingDuration) + newState.fabricSoftenerWashingDelta

        if time >= t:
            newState.isFabricSoftenerValveOpened = True
            newState.fabricSoftenerStartedTime = time
            writeMemoryAddress(0x0100, readMemoryAddress(0x0100) | 0b01000000);
            print("{:.2f} FabricSoftener opened".format(time))
            sleep(2.5)

    if state.isWashing and time >= (newState.washingStartedTime + newState.washingDuration):
        newState.isWashing = False
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) | 0b00000010);
        print("{:.2f} Washing ended".format(time))
        newState.isSpinning = True
        newState.spinningStartedTime = time
        print("{:.2f} Spinning started".format(time))
    elif state.isSpinning and time >= (newState.spinningStartedTime + newState.spinningDuration):
        newState.isSpinning = False
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) & 0b11111110);
        print("{:.2f} Spinning ended".format(time))
        
    return newState

def finalStateMessage(state):
    #return state.__class__.__name__
    return state.__str__()

commands = {
    "cotton-button" : {
        "pushed" : cottonButtonPushed
    },
    "disinfection-button" : {
        "pushed" : disinfectionButtonPushed
    },
    "rough-button" : {
        "pushed" : roughButtonPushed
    },
    "soaking-spinning-button" : {
        "pushed" : soakingSpinningButtonPushed
    },
    "synthetic-button" : {
        "pushed" : syntheticButtonPushed
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
    delta = 0.1
    while time + delta < endTime:
        sleep(0.05)
        time += delta
        state = timePassed(time, state)
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
