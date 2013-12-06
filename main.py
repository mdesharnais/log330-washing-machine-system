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
    memory.seek(offsetOfMemoryAddress(address, offset))
    return int(memory.read(numBits), 2)

def writeMemoryAddress(address, byte):
    memory = open("memory", "r+")
    memory.seek(offsetOfMemoryAddress(address))
    memory.write("{:0>8b}".format(byte))
    memory.close()

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
            
        def setInformationScreenText(self, text):          
            self.informationScreen.delete(1.0, END)
            self.informationScreen.insert(END, text)
            self.informationScreen.see(END)
        
        def appendInformationScreenText(self, text):
            # The get method in the text widget always returns one more character than what is displayed
            if len(self.informationScreen.get(1.0, END)) > 1:
                self.informationScreen.insert(END, "\n")
                
            self.informationScreen.insert(END, text)
            self.informationScreen.see(END)     
              
        def changeState(self, stateName):
            if self.selectedState != None and self.selectedState.isStarted:
                self.appendInformationScreenText("Veuillez arrêter le cycle en cours avant de changer de cycle")
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
            self.appendInformationScreenText("Cycle arrêté par l'usager.")
            
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
