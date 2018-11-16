'''

Name: IOTBit Library
Purpose: Library to interface with the IOTBit HAT on the Raspberry Pi, 
tested on the latest version of Raspbian using a Raspberry Pi 3b.

'''

import serial
import time


import serial.tools.list_ports 
import RPi.GPIO as GP
from datetime import datetime
from threading import Condition
import io
#from tkinter import *



'''
Gets the current time in milliseconds. Required for timeout implementation
'''
def Getmills():
    mills = int(round(time.time()*1000))
    return mills


class Modem:

    '''
    Set up the system only works if no other ttyUSB ports are on board
    '''
    def __init__(self, APN, Device = '4G'):
        self.APN = APN
        self.end = '\r'
        
        USB_ports = list(serial.tools.list_ports.comports())

        if Device == '4G':
            GPS = USB_ports[3].device
            AT = USB_ports[2].device
            PPP = USB_ports[1].device
            Audio = USB_ports[0].device

            self.GPSPort = serial.Serial(GPS, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1, rtscts=True, dsrdtr=True)
            self.ATPort = serial.Serial(AT, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1, rtscts=True, dsrdtr=True)
            self.PPPPort = serial.Serial(PPP, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1, rtscts=True, dsrdtr=True)
            self.AudioPort = serial.Serial(Audio, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1, rtscts=True, dsrdtr=True)
            
        elif Device == '3G':
            GPS = USB_ports[2].device
            AT = USB_ports[1].device
            PPP = USB_ports[0].device

            self.GPSPort = serial.Serial(GPS, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1, rtscts=True, dsrdtr=True)
            self.ATPort = serial.Serial(AT, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1, rtscts=True, dsrdtr=True)
            self.PPPPort = serial.Serial(PPP, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1, rtscts=True, dsrdtr=True)
            
        elif Device == 'GSM':
            UARTPort = '/dev/serial0' # Serial Port for Raspbian Strech and higher
            self.PassthroughPort = serial.Serial(UARTPort, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1, rtscts=True, dsrdtr=True)
        

        
    '''
    Function to Send commands via the serial interface. 
    Waits for a response and returns the respons if there is one.
    '''
    def sendATcmd(self, ATcmd, Timeout):
        # Modify the ATcmd so that it has the end of line character 
        cmd = ATcmd + self.end
        # Send the cmd to the device 
        self.ATPort.write(cmd.encode())
        time.sleep(0.01)

        # Check the serial buffer to see if there is a response waiting  
        bytestoread = self.ATPort.inWaiting()

        # While timeout not reached keep checking buffer    
        if (bytestoread == 0):
            curtime = Getmills()

            while (bytestoread == 0) and ((Getmills()-curtime)<Timeout):
                bytestoread = self.ATPort.inWaiting()
                
            # Store the response 
            self.response = self.ATPort.read(bytestoread).decode("utf-8")

        else:
            self.response = self.ATPort.read(bytestoread).decode("utf-8")

    
    '''
    Function to read the a port to see if there data is waiting to be read.
    '''
    def ReadPort(self, Port, Timeout):
        # Check the serial buffer to see if there is a response waiting  
        bytestoread = Port.inWaiting()
        # While timeout not reached keep checking buffer 
        if (bytestoread == 0):
            curtime = Getmills()
            while (bytestoread == 0) and ((Getmills()-curt
                                           )<Timeout):
                bytestoread = Port.inWaiting()

            # Store the response 
            response = Port.read(bytestoread)
        else:
            response = Port.read(bytestoread)
        return response

  
    '''
    Function to read the a port to see if there data is waiting to be read.
    '''
    def ReadPortUART(self, Port, Timeout):
        self.VersionCheck()
        time.sleep(0.01)
        self.PassthroughPort.flushInput()
        self.PassthroughPort.flushOutput()
        
        # Modify the ATcmd so that it has the end of line character
        cmd = ATcmd + self.end
        
        # Wait for modem to be ready
        ready = ""
        ready = self.PassthroughPort.readline().decode("utf-8")
        T = 'D'
        if 'Modem Ready' in ready:
            self.PassthroughPort.write(T.encode())
            # Check the serial buffer to see if there is a response waiting  
            bytestoread = PassthroughPort.inWaiting()
            # While timeout not reached keep checking buffer 
            if (bytestoread == 0):
                curtime = Getmills()
                while (bytestoread == 0) and ((Getmills()-curt
                                               )<Timeout):
                    bytestoread = PassthroughPort.inWaiting()

                # Store the response 
                response = Port.read(bytestoread)
            else:
                response = Port.read(bytestoread)
        return response        
    '''
    Function to Send commands via the serial interface
    Waits for a response and returns the response if there is one.
    Timeout length is variable.
    Usable only with firmware verison 1.5 and above
    To test your firmare version use the function VersionCheck().        
    '''
    def sendATcmdUART(self, ATcmd, Timeout):
        self.VersionCheck()
        time.sleep(0.01)
        self.PassthroughPort.flushInput()
        self.PassthroughPort.flushOutput()
        
        # Modify the ATcmd so that it has the end of line character
        cmd = ATcmd + self.end
        Time = str(Timeout)
        
        # Wait for modem to be ready
        ready = ""
        ready = self.PassthroughPort.readline().decode("utf-8"
        if 'Modem Ready' in ready:
            T = 'P'
            self.PassthroughPort.write(T.encode())
            SendTimeout = ""
            SendTimeout = self.PassthroughPort.readline().decode("utf-8")
            
            #print ( 'Timeout str: {0}, Time: {1}'.format(SendTimeout,Time))
            if 'Send Timeout' in SendTimeout:
                self.PassthroughPort.write(Time.encode())
                Sendcmd = ""
                Sendcmd = self.PassthroughPort.readline().decode("utf-8")
                
                if 'Send CMD' in Sendcmd:            
                    # Send the cmd to the device 
                    self.PassthroughPort.write(cmd.encode())

                    # Check the serial buffer to see if there is a response waiting        
                    bytestoread = self.PassthroughPort.inWaiting()
                    
                    # While timeout not reached keep checking buffer    
                    if (bytestoread == 0):
                        #time.sleep((Timeout+500)/1000)
                        curtime = Getmills()
                        
                        while (bytestoread == 0) or ((Getmills()-curtime)<Timeout):
                            bytestoread = self.PassthroughPort.inWaiting()
                            time.sleep(0.01)
                        '''
                        while (bytestoread == 0) and ((Getmills()-curtime)<Timeout):
                            bytestoread = self.PassthroughPort.inWaiting()
                            time.sleep(1)
                        while (bytestoread == 0) and ((Getmills()-curtime)<Timeout):
                            bytestoread = self.PassthroughPort.inWaiting()
                            time.sleep(1)
                            '''
                        # Store the response
                        print(bytestoread)
                        #self.response = self.PassthroughPort.readline().decode("utf-8")
                        self.response = self.PassthroughPort.read(bytestoread).decode("utf-8")
                        
                    else:      
                        self.response = self.PassthroughPort.readline().decode("utf-8")
                else:
                    print ('Cmd not sent')
            else:
                print('Timout not sent')
        else:
            print ('Modem not ready')
    
            
    '''
    Hard reset the modem, usable only with firmware verison 1.5
    '''
    def ResetModem(self):
    # Wait for modem to be ready
        ready = ""
        ready = self.PassthroughPort.readline()
        print (ready)
        if 'Modem Ready' in ready:
            self.PassthroughPort.write('R')
            time.sleep(15)
            bytestoread = self.PassthroughPort.inWaiting()
            # While timeout not reached keep checking buffer    
            if (bytestoread == 0):
                curtime = Getmills()
                while (bytestoread == 0) & ((Getmills()-curtime)<1000):
                    bytestoread = self.PassthroughPort.inWaiting()
                    time.sleep(0.15)
                # Store the response 
                self.response = self.PassthroughPort.read(bytestoread)
                print (bytestoread)
                        
            else:      
                self.response = self.PassthroughPort.readline()     

                      
    '''
    Reset the IOTBit
    '''
    def ResetAll(self):
        # Wait for modem to be ready
        ready = ""
        ready = self.PassthroughPort.readline()
        if 'Modem Ready' in ready:
            self.PassthroughPort.write('S')

    '''
    Check the firmware version if you get no response this means
    the firmware version is older than 1.5
    '''
    def VersionCheck(self):
        # Wait for modem to be ready
        ready = ""
        ready = self.PassthroughPort.readline()
        if 'Modem Ready' in ready:
            self.PassthroughPort.write('V')
            self.response = self.PassthroughPort.readline()

           

