#!/usr/bin/python3

import copy
import sys
import time
import threading
from time import sleep
from tkinter import *

# 0x200 = 2 * (8 bits + 1 newline) = 18
def offsetOfMemoryAddress(address, offset = 0):
    return (address >> 8) * 9 + offset

def readMemoryAddress(address, numBits = 8, offset = 0):
    memory = open("memory", "r")
<<<<<<< HEAD
    memory.seek(offsetOfMemoryAddress(address))
    return int(memory.read(8), 2)
=======
    memory.seek(offsetOfMemoryAddress(address, offset))
    return int(memory.read(numBits), 2)
>>>>>>> f9215af... Final commit

def writeMemoryAddress(address, byte):
    memory = open("memory", "r+")
    memory.seek(offsetOfMemoryAddress(address))
    memory.write("{:0>8b}".format(byte))
    memory.close()

<<<<<<< HEAD
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
      
class Interface():
        def __init__(self, file):
            self.createInputStream(file)
            
            self.master = Tk()    
            self.master.wm_title("Machine à laver ACME")        
            self.createInterface()            
            
            self.stateStarted = False
            
            self.master.mainloop()
            
        def createInterface(self):            
            self.mainFrame = Frame(self.master) #Frame de login
            self.mainFrame.pack()
            
            self.informationScreen = Text(self.mainFrame, height=5)
            self.informationScreen.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
            
            self.cottonButton = Button(self.mainFrame, text="Coton", width=15, command=lambda: self.cottonButtonPushed()).grid(row=1, column=0, sticky=W+E+N+S)            
            self.syntheticButton = Button(self.mainFrame, text="Synthétique", width=15, command=lambda: self.syntheticButtonPushed()).grid(row=1, column=1, sticky=W+E+N+S)     
            self.roughButton = Button(self.mainFrame, text="Rugueux", width=15, command=lambda: self.roughButtonPushed()).grid(row=1, column=2, sticky=W+E+N+S)
            self.soakingSpinningButton = Button(self.mainFrame, text="Trempage / Essorage", width=15, command=lambda: self.soakingSpinningButtonPushed()).grid(row=1, column=3, sticky=W+E+N+S)            
            self.disinfectionButton = Button(self.mainFrame, text="Désinfection", width=15, command=lambda: self.disinfectionButtonPushed()).grid(row=1, column=4, sticky=W+E+N+S)
            
            self.waterLevelButton = Button(self.mainFrame, text="Niveau d'eau", width=15, command=lambda: self.waterLevelButtonPushed()).grid(row=2, column=1, sticky=W+E+N+S, pady=(5,0))
            self.startButton = Button(self.mainFrame, text="Départ", width=15, command=lambda: self.startButtonPushed()).grid(row=2, column=2, sticky=W+E+N+S, pady=(5,0))            
            self.stopButton = Button(self.mainFrame, text="Arrêt", width=15, command=lambda: self.stopButtonPushed()).grid(row=2, column=3, sticky=W+E+N+S, pady=(5,0))
            
            self.lightsLabel = Label(self.mainFrame, bg="red")
            self.lightsLabel.grid(row=2, column=4, sticky=W+E+N+S, pady=(5,0))
        
=======
def writeMemoryAddressForState(state):
    # Reset all the states before setting the new state
    writeMemoryAddress(0x0200, readMemoryAddress(0x0200) & 0b11111000)
    writeMemoryAddress(0x0700, readMemoryAddress(0x0700) & 0b01111011)
    
    if state == "coton":
        writeMemoryAddress(0x0200, readMemoryAddress(0x0200) | 0b00000100)
    elif state == "synthétique":
        writeMemoryAddress(0x0200, readMemoryAddress(0x0200) | 0b00000010)
    elif state == "rugueux":
        writeMemoryAddress(0x0200, readMemoryAddress(0x0200) | 0b00000001)
    elif state == "désinfection":
        writeMemoryAddress(0x0700, readMemoryAddress(0x0700) | 0b10000000)
    elif state == "trempage/essorage":
        writeMemoryAddress(0x0700, readMemoryAddress(0x0700) | 0b00000100)
    else:
        print("Cycle invalide!")

def writeDesiredWaterLevel(waterLevel):
    desiredWaterLevel = '{0:04b}'.format(waterLevel).ljust(8,'0')
    
    #Reset the desired water level to zero
    writeMemoryAddress(0x0200, readMemoryAddress(0x0200) & 0b00001111)    
    writeMemoryAddress(0x0200, readMemoryAddress(0x0200) | int(desiredWaterLevel, 2))

def writeCurrentWaterLevel(waterLevel):
    desiredWaterLevel = '{0:05b}'.format(waterLevel).ljust(8,'0')
    
    #Reset the current water level to zero
    writeMemoryAddress(0x0700, readMemoryAddress(0x0700) & 0b10000111)    
    writeMemoryAddress(0x0700, readMemoryAddress(0x0700) | int(desiredWaterLevel, 2))
    
class WashingState:
    def __init__(self, interface):
        self.interface = interface
        
        self.isStarted = False;
        
        self.soapWaterLevel = 2
        self.soapDuration = 1
        
        self.bleachWaterLevel = 10
        self.bleachDuration = 1
        
        self.fabricSoftenerWashingDelta = -5
        self.fabricSoftenerDuration = 1
        
        self.emptyingDuration = 2                   
        
        self.soapValveCloseTime = -1
        self.bleachValveCloseTime = -1
        self.fabricSoftenerValveCloseTime = -1
        self.totalTimeRunning = 0
        
    def run(self):
        self.fill()
        self.wash()
        self.empty()
        self.spin()
            
        self.totalTimeRunning += 1
        
        if self.isStarted and self.totalTimeRunning < (self.getSoakingDuration() + self.getWashingDuration() + self.emptyingDuration + self.getSpinningDuration()):        
            threading.Timer(secondsPerMinute, self.run).start()
        elif self.isStarted:
            self.interface.appendInformationScreenText("Essorage terminé" + self.getProgress())
            self.stopSpinning()
            self.interface.lightsLabel.config(bg="red")
            self.resetValues()
        else:
            self.stopSpinning()
            self.resetValues()
    
    def fill(self):
        if self.totalTimeRunning < self.getSoakingDuration() and self.getCurrentWaterLevel() < self.getDesiredWaterLevel():
            if not self.isFilling():
                self.interface.setInformationScreenText("Remplissage débuté" + self.getProgress())
                self.startFilling()
                
            self.incrementCurrentWaterLevel()
            self.interface.appendInformationScreenText("Cuve remplie à " + str(self.getCurrentWaterLevel() * 10) + "% sur " + str(self.getDesiredWaterLevel() * 10) + "% désirés" + self.getProgress())
            
            if self.getCurrentWaterLevel() == self.soapWaterLevel and not self.isSoapValveOpened():
                self.openSoapValve()
                self.soapValveCloseTime = self.totalTimeRunning + self.soapDuration
                self.interface.appendInformationScreenText("Valve à savon ouverte" + self.getProgress())    
            elif self.getCurrentWaterLevel() == self.bleachWaterLevel and not self.isBleachValveOpened():
                self.openBleachValve()
                self.bleachValveCloseTime = self.totalTimeRunning + self.bleachDuration
                self.interface.appendInformationScreenText("Valve à javellisant ouverte" + self.getProgress())                
        elif self.isFilling():
            self.interface.appendInformationScreenText("Remplissage terminé" + self.getProgress())
            self.stopFilling()
        
        if self.isSoapValveOpened() and self.totalTimeRunning >= self.soapValveCloseTime:
                self.closeSoapValve()
                self.interface.appendInformationScreenText("Valve à savon fermée" + self.getProgress())
        if self.isBleachValveOpened() and self.totalTimeRunning >= self.bleachValveCloseTime:
            self.closeBleachValve()
            self.interface.appendInformationScreenText("Valve à javellisant fermée" + self.getProgress())
            
    def wash(self):
        if self.totalTimeRunning >= self.getSoakingDuration() and self.totalTimeRunning < (self.getSoakingDuration() + self.getWashingDuration()):
            if not self.isAgitating():
                self.interface.appendInformationScreenText("Lavage débuté" + self.getProgress())
                self.startAgitating()
                
            if self.getSoakingDuration() + self.getWashingDuration() + self.fabricSoftenerWashingDelta == self.totalTimeRunning:
                self.openFabricSoftenerValve()
                self.fabricSoftenerValveCloseTime = self.totalTimeRunning + self.fabricSoftenerDuration
                self.interface.appendInformationScreenText("Valve à assouplissant ouverte" + self.getProgress())
                
            if self.isFabricSoftenerValveOpened() and self.totalTimeRunning >= self.fabricSoftenerValveCloseTime:
                self.closeFabricSoftenerValve()
                self.interface.appendInformationScreenText("Valve à assouplissant fermée" + self.getProgress())
        elif self.isAgitating():
            self.interface.appendInformationScreenText("Lavage terminé" + self.getProgress())
            self.stopAgitating()
    
    def empty(self):
        if self.totalTimeRunning >= (self.getSoakingDuration() + self.getWashingDuration()) and self.totalTimeRunning < (self.getSoakingDuration() + self.getWashingDuration() + self.emptyingDuration):
            if not self.isEmptying():
                self.interface.appendInformationScreenText("Vidange de l'eau débutée" + self.getProgress())
                self.startEmptying()
        elif self.isEmptying():
            self.interface.appendInformationScreenText("Vidange de l'eau terminée" + self.getProgress())
            self.stopEmptying()
          
    def spin(self):
        if self.totalTimeRunning >= (self.getSoakingDuration() + self.getWashingDuration() + self.emptyingDuration) and self.totalTimeRunning < (self.getSoakingDuration() + self.getWashingDuration() + self.emptyingDuration + self.getSpinningDuration()):
            if not self.isSpinning():
                self.interface.appendInformationScreenText("Essorage débuté" + self.getProgress())
                self.startSpinning()
          
    def getProgress(self):
        return " -- Minute " + str(self.totalTimeRunning) + " sur " + str(self.getTotalMinutes())
        
    def getTotalMinutes(self):
        return (self.getSoakingDuration() + self.getWashingDuration() + self.emptyingDuration + self.getSpinningDuration())
          
    def getSelectedState(self):
        if readMemoryAddress(0x0200, 1, 5) == 1:
            return "coton"
        elif readMemoryAddress(0x0200, 1, 6) == 1:
            return "synthétique"
        elif readMemoryAddress(0x0200, 1, 7) == 1:
            return "rugueux"
        elif readMemoryAddress(0x0700, 1) == 1:
            return "désinfection"
        else:
            return "trempage/essorage" 
        
    def getWashingDuration(self):
        selectedState = self.getSelectedState()
        
        if selectedState == "coton":
            return 45
        elif selectedState == "synthétique":
            return 30
        elif selectedState == "rugueux":
            return 45
        elif selectedState == "désinfection":
            return 45
        else:
            return 0
            
    def getSpinningDuration(self):
        selectedState = self.getSelectedState()
        
        if selectedState == "coton":
            return 10
        elif selectedState == "synthétique":
            return 5
        elif selectedState == "rugueux":
            return 10
        elif selectedState == "désinfection":
            return 10
        else:
            return 15
    
    def getSoakingDuration(self):
        if self.getSelectedState() == "trempage/essorage":
            return 10
        else:
            return 30
        
    def isWaterLevelFixed(self):
        selectedState = self.getSelectedState()      
        return selectedState == "trempage/essorage" or selectedState == "désinfection"
    
    def isColdWaterValveOpened(self):
        return readMemoryAddress(0x0100, 1, 2) == 1
    
    def isHotWaterValveOpened(self):
        return readMemoryAddress(0x0100, 1, 3) == 1
    
    def isFabricSoftenerValveOpened(self):
        return readMemoryAddress(0x0100, 1, 6) == 1
    
    def openFabricSoftenerValve(self):
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) | 0b00000010)
    
    def closeFabricSoftenerValve(self):
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) & 0b11111101)
        
    def isSoapValveOpened(self):
        return readMemoryAddress(0x0100, 1, 4) == 1
    
    def openSoapValve(self):
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) | 0b00001000)
    
    def closeSoapValve(self):
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) & 0b11110111)
            
    def isBleachValveOpened(self):
        return readMemoryAddress(0x0100, 1, 5) == 0
    
    def openBleachValve(self):
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) & 0b111111011)
    
    def closeBleachValve(self):
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) | 0b00000100)
        
    def getColdWaterValveRequired(self):
        return self.getSelectedState() != "trempage/essorage"
    
    def isFilling(self):
        return readMemoryAddress(0x0100, 1, 3) == 1
    
    def startFilling(self):
        if self.getColdWaterValveRequired():
            self.openColdWaterValve()
        
        self.openHotWaterValve() 
    
    def openColdWaterValve(self):
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) | 0b00100000)
    
    def openHotWaterValve(self):
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) | 0b00010000)
    
    def stopFilling(self):
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) & 0b11001111)
       
    def isAgitating(self):
        return readMemoryAddress(0x0100, 1) == 1
    
    def startAgitating(self):
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) | 0b10000000)
    
    def stopAgitating(self):
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) & 0b01111111)
     
    def isEmptying(self):
        return readMemoryAddress(0x0100, 1, 1) == 0
    
    def startEmptying(self):
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) & 0b10111111)
    
    def stopEmptying(self):
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) | 0b01000000)
    
    def isSpinning(self):
        return readMemoryAddress(0x0100, 1, 7) == 1
    
    def startSpinning(self):
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) | 0b00000001)
    
    def stopSpinning(self):
        writeMemoryAddress(0x0100, readMemoryAddress(0x0100) & 0b11111110)
    
    def getCurrentWaterLevel(self):
        return readMemoryAddress(0x0700, 4, 1)
    
    def incrementCurrentWaterLevel(self):        
        writeCurrentWaterLevel(self.getCurrentWaterLevel() + 1)
        
    def getDesiredWaterLevel(self):
        return readMemoryAddress(0x0200, 4)
    
    def resetValues(self):
        self.isStarted = False
        self.totalTimeRunning = 0
        self.soapValveCloseTime = -1
        self.bleachValveCloseTime = -1
        self.fabricSoftenerValveCloseTime = -1
        writeMemoryAddress(0x0100, 0b01000100)
        writeMemoryAddress(0x0200, readMemoryAddress(0x0200) & 0b11110111)
        writeMemoryAddress(0x0700, readMemoryAddress(0x0700) & 0b10000100)
          
class Interface():
        def __init__(self):
            self.master = Tk()            
            self.master.wm_title("Machine à laver ACME")
            self.master.protocol("WM_DELETE_WINDOW", self.clearInformationAndClose)
                   
            self.createInterface()            
            
            self.selectedState = None
            writeDesiredWaterLevel(2) #Default value
            self.master.mainloop()
            
        def createInterface(self):            
            self.mainFrame = Frame(self.master)
            self.mainFrame.pack()
            
            self.informationScreen = Text(self.mainFrame, height=25)
            self.informationScreen.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
            
            self.cottonButton = Button(self.mainFrame, text="Coton", width=15, command=lambda: self.cottonButtonPushed())
            self.cottonButton.grid(row=1, column=0, sticky=W+E+N+S)
            
            self.syntheticButton = Button(self.mainFrame, text="Synthétique", width=15, command=lambda: self.syntheticButtonPushed())
            self.syntheticButton.grid(row=1, column=1, sticky=W+E+N+S)
            
            self.roughButton = Button(self.mainFrame, text="Rugueux", width=15, command=lambda: self.roughButtonPushed())
            self.roughButton.grid(row=1, column=2, sticky=W+E+N+S)
            
            self.soakingSpinningButton = Button(self.mainFrame, text="Trempage / Essorage", width=15, command=lambda: self.soakingSpinningButtonPushed())
            self.soakingSpinningButton.grid(row=1, column=3, sticky=W+E+N+S)
            
            self.disinfectionButton = Button(self.mainFrame, text="Désinfection", width=15, command=lambda: self.disinfectionButtonPushed())
            self.disinfectionButton.grid(row=1, column=4, sticky=W+E+N+S)            
            
            Button(self.mainFrame, text="Niveau d'eau", width=15, command=lambda: self.waterLevelButtonPushed()).grid(row=2, column=1, sticky=W+E+N+S, pady=(5,0))
            Button(self.mainFrame, text="Départ", width=15, command=lambda: self.startButtonPushed()).grid(row=2, column=2, sticky=W+E+N+S, pady=(5,0))            
            Button(self.mainFrame, text="Arrêt", width=15, command=lambda: self.stopButtonPushed()).grid(row=2, column=3, sticky=W+E+N+S, pady=(5,0))
            
            self.lightsLabel = Label(self.mainFrame, bg="red")
            self.lightsLabel.grid(row=2, column=4, sticky=W+E+N+S, pady=(5,0))
            
            self.labelWaterLevel = Label(self.mainFrame, text="20%")
            self.labelWaterLevel.grid(row=3, column=0, columnspan=5, sticky=W+E+N+S, pady=(5,0)) 
        
        def clearInformationAndClose(self):
            writeMemoryAddress(0x0100, 0b01000100)
            writeMemoryAddress(0x0200, 0b00000000)
            writeMemoryAddress(0x0700, 0b00000000)
            
            if self.selectedState != None:
                self.selectedState.isStarted = False
            
            try:
                self.master.destroy()
            except:
                pass
            
>>>>>>> f9215af... Final commit
        def setInformationScreenText(self, text):          
            self.informationScreen.delete(1.0, END)
            self.informationScreen.insert(END, text)
            self.informationScreen.see(END)
        
<<<<<<< HEAD
        def appendInformationScreenTextOnNewLine(self, text):
=======
        def appendInformationScreenText(self, text):
>>>>>>> f9215af... Final commit
            # The get method in the text widget always returns one more character than what is displayed
            if len(self.informationScreen.get(1.0, END)) > 1:
                self.informationScreen.insert(END, "\n")
                
            self.informationScreen.insert(END, text)
<<<<<<< HEAD
            self.informationScreen.see(END)       
             
        # Those input are represent as function that receive a state, some input informations and produce
        # a new state corresponding to the responce of the system (e.g. if the desired water capacity is
        # achieved, the function could trigger an output to stop the water valve and return a new state
        # where we start to add soap.
        
        def setStateChangedMessage(self, stateName):
            if self.stateStarted:
                self.setInformationScreenText("Veuillez arrêter le cycle en cours pour changer de cycle")
            else:
                self.setInformationScreenText("Cycle {} sélectionné".format(stateName))
                
        def cottonButtonPushed(self):
            self.setStateChangedMessage("coton")
                
            writeMemoryAddress(0x0200, readMemoryAddress(0x0200) | 0b00100000)
            self.newState = WashingState()
            self.newState.washingDuration = 45.0
            self.newState.spinningDuration = 10.0
        
        def disinfectionButtonPushed(self):
            self.setStateChangedMessage("désinfection")
            writeMemoryAddress(0x0700, readMemoryAddress(0x0700) | 0b00000001)
            self.newState = WashingState()
            self.newState.washingDuration = 45.0
            self.newState.spinningDuration = 10.0
            self.newState.desiredWaterLevel = 0.5
        
        def roughButtonPushed(self):
            self.setStateChangedMessage("rugueux")
            writeMemoryAddress(0x0200, readMemoryAddress(0x0200) | 0b10000000)
            self.newState = WashingState()
            self.newState.washingDuration = 45.0
            self.newState.spinningDuration = 10.0
        
        def soakingSpinningButtonPushed(self):
            self.setStateChangedMessage("trempage/essorage")
            writeMemoryAddress(0x0700, readMemoryAddress(0x0700) | 0b00100000)
            self.newState = WashingState()
            self.newState.washingDuration = 10.0
            self.newState.spinningDuration = 15.0
            self.newState.soapStartedTime = -1.0
            self.newState.bleachStartedTime = -1.0
            self.newState.fabricSoftenerStartedTime = -1.0
            self.newState.desiredWaterLevel = 1.0
        
        def syntheticButtonPushed(self):
            self.setStateChangedMessage("synthétique")
            writeMemoryAddress(0x0200, readMemoryAddress(0x0200) | 0b01000000)
            self.newState = WashingState()
            self.newState.washingDuration = 30.0
            self.newState.spinningDuration = 5.0
        
        def startButtonPushed(self):
            self.stateStarted = True
            self.lightsLabel.config(bg="green")
            # TODO: Specify which state is being started
            self.setInformationScreenText("Cycle démarré")
#             writeMemoryAddress(0x0200, readMemoryAddress(0x0200) | 0b00010000);
#             newState = copy.deepcopy(state)
#         
#             newState.isColdWaterValveOpened = True
#             writeMemoryAddress(0x0100, readMemoryAddress(0x0100) | 0b00000100);
#             print("{:.2f} ColdWaterValve opened".format(time))
#         
#             newState.isHotWaterValveOpened = True
#             writeMemoryAddress(0x0100, readMemoryAddress(0x0100) | 0b00001000);
#             print("{:.2f} HotWaterValve opened".format(time))
#         
#             return newState
        
        def stopButtonPushed(self):
            self.stateStarted = False
            self.lightsLabel.config(bg="red")
            # TODO: Specify which state is being stopped
            self.setInformationScreenText("Cycle arrêté")
        
        def waterLevelButtonPushed(self):
            pass
#             newState = copy.deepcopy(state)
#         
#             if newState.desiredWaterLevel == 1.0:
#                 newState.desiredWaterLevel = 0.0
#         
#             newState.desiredWaterLevel += 0.2
#         
#             writeMemoryAddress(0x0200, (readMemoryAddress(0x0200) & 0b11110000) | int(0.2 * 10));
#         
#             return newState
        
        def waterLevelSensorLevel(self, time, state, level):
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
        
        def timePassed(self, time, state):
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
        
        def finalStateMessage(self, state):
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
        
        def parseCommand(self, line):
            # Format is as follow:
            # <time-in-minutes :: Double> <component> <signal> <args0> <arg1> ... <argN>
            words = line.split()
            time = float(words[0])
            component = words[1]
            message = words[2]
            args = words[3:]
            command = lambda time, state: self.commands[component][message](time, state, *args)
            return (time, command)
        
        def runWashingMachineWithTime(self, time, endTime, state):
            # We update the state every 0.25 minutes = 15 seconds until we reach the end time
            delta = 0.1
            while time + delta < endTime:
                sleep(0.05)
                time += delta
                state = self.timePassed(time, state)
            return state
        
        def runWashingMachine(self, time, state):
            line = self.inputStream.readline()
            if not line:
                # Run for 120 minutes after the last command to let any ongoing cycle terminate
                return self.runWashingMachineWithTime(time, time + 120.0, state)
            else:
                (commandTime,commandFunction) = self.parseCommand(line)
        
                # Run for the time between the two last commands
                tempState = self.runWashingMachineWithTime(time, commandTime, state)
        
                # Run the command
                newState = commandFunction(commandTime, tempState)
                return self.runWashingMachine(commandTime, newState)
        
        def createInputStream(self, file):
            self.inputStream = open(sys.argv[1])
            
if __name__ == "__main__":    
    if len(sys.argv) != 2:
        print("Usage: washing-machine <test-file>")
    else:
        interface = Interface(sys.argv[1])
        #endState = interface.runWashingMachine(0.0, IddleState())
        #print(interface.finalStateMessage(endState))
=======
            self.informationScreen.see(END)     
              
        def changeState(self, stateName):
            if self.selectedState != None and self.selectedState.isStarted:
                self.setInformationScreenText("Veuillez arrêter le cycle en cours avant de changer de cycle")
            else:                
                writeMemoryAddressForState(stateName)
                self.setInformationScreenText("Cycle {} sélectionné".format(stateName))
        
        def pressButton(self, button):
            self.cottonButton.config(relief=RAISED)
            self.disinfectionButton.config(relief=RAISED)
            self.roughButton.config(relief=RAISED)
            self.soakingSpinningButton.config(relief=RAISED)
            self.syntheticButton.config(relief=RAISED)
            
            button.config(relief=SUNKEN)
                    
        def cottonButtonPushed(self):
            self.pressButton(self.cottonButton)            
            self.changeState("coton")            
            self.selectedState = WashingState(self)
        
        def disinfectionButtonPushed(self):
            self.pressButton(self.disinfectionButton)            
            self.changeState("désinfection")            
            self.selectedState = WashingState(self)
            writeDesiredWaterLevel(5)
            self.labelWaterLevel.config(text="50%")
        
        def roughButtonPushed(self):
            self.pressButton(self.roughButton)            
            self.changeState("rugueux")            
            self.selectedState = WashingState(self)
        
        def soakingSpinningButtonPushed(self):
            self.pressButton(self.soakingSpinningButton)            
            self.changeState("trempage/essorage")            
            self.selectedState = WashingState(self)
            writeDesiredWaterLevel(10)
            self.labelWaterLevel.config(text="100%")
        
        def syntheticButtonPushed(self):
            self.pressButton(self.syntheticButton)            
            self.changeState("synthétique")            
            self.selectedState = WashingState(self)
        
        def startButtonPushed(self):
            if self.selectedState != None and not self.selectedState.isStarted:
                self.selectedState.isStarted = True
                self.lightsLabel.config(bg="green")
                self.setInformationScreenText("Cycle démarré")
                
                writeMemoryAddress(0x0200, readMemoryAddress(0x0200) | 0b00001000);
                
                self.selectedState.run()
                
            elif self.selectedState == None:
                self.setInformationScreenText("Veuillez choisir un cycle avant de démarrer la laveuse.")
            else:
                self.setInformationScreenText("La laveuse est déjà en cours de fonctionnement.")
        
        def stopButtonPushed(self):
            self.selectedState.isStarted = False
            self.lightsLabel.config(bg="red")
            self.setInformationScreenText("Cycle arrêté par l'usager.")
            
            writeMemoryAddress(0x0200, readMemoryAddress(0x0200) & 0b11110111);
        
        def waterLevelButtonPushed(self):
            if self.selectedState != None and self.selectedState.isWaterLevelFixed():
                self.setInformationScreenText("Le niveau de l'eau est fixe pour ce type de cycle.")
            else:
                desiredWaterLevel = readMemoryAddress(0x0200, 4)
                
                if desiredWaterLevel == 10:
                    desiredWaterLevel = 0
             
                desiredWaterLevel += 1                     
                self.labelWaterLevel.config(text=str(desiredWaterLevel * 10)+"%")
                                    
                writeDesiredWaterLevel(desiredWaterLevel)                
        
        def finalStateMessage(self, state):
            return state.__str__()
            
if __name__ == "__main__":
    secondsPerMinute = 0.3
    Interface()
>>>>>>> f9215af... Final commit
