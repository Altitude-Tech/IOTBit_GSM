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
        Time = str(Timeout)
        
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
    Usable only with firmware verison 1.5
    To test your firmare version use the function VersionCheck().        
    '''
    def sendATcmdUART_T(self, ATcmd, Timeout):
        self.VersionCheck()
        time.sleep(0.01)
        self.PassthroughPort.flushInput()
        self.PassthroughPort.flushOutput()
        
        # Modify the ATcmd so that it has the end of line character
        cmd = ATcmd + self.end
        Time = str(Timeout)
        
        # Wait for modem to be ready
        ready = ""
        ready = self.PassthroughPort.readline().decode("utf-8")
        T = 'P'
        if 'Modem Ready' in ready:
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
    Function to start the GPS in Standalone mode 
    Modes can be 0,1 and 2 for cold, hot or normal start.
    '''
    def StartGPS_S(self, mode):
        print (' Configuring ....')

        # Set the NMEA port to output GLNOass and GPRS data
        self.sendATcmdUART('AT+CGPSNMEA=3',100)
        if 'OK' in self.response:
            print ('NMEA Port configured')
        else:
            print (self.response)

        time.sleep(0.01)

        # Make sure the GPS is actually off
        self.sendATcmdUART('AT+CGPS=0',100)
        if 'OK' in self.response:
            print ('Resetting GPS')
        else:
            print (self.response)

        time.sleep(0.01)

        # Check which mode has been chosen to turn on GPS
        if mode == 0:
            self.sendATcmdUART('AT+CGPSCOLD',100)
            if 'OK' in self.response:
                print (' Cold starting GPS')
            else:
                print (self.response)
        elif mode == 1:
            self.sendATcmdUART('AT+CGPSHOT',100)
            if 'OK' in self.response:
                print (' Hot starting GPS')
            else:
                print (self.response)
        elif mode == 2:
            self.sendATcmdUART('AT+CGPS=1',100)
            if 'OK' in self.response:
                print (' Starting GPS')
            else:
                print (self.response)
        else:
            print ("Mode not set")

        time.sleep(0.01)

    '''
    Fuction to turn off the GPS
    '''
    def StopGPS(self):
        #Send ATcmd to device
        self.sendATcmdUART('AT+CGPS=0',1)
        #Check and display response
        if 'OK' in self.response:
                print (' Stopping GPS')
        else:
                print (self.response)
        time.sleep(0.01)

    '''
    Function to configure SMS 
    '''
    def SMSConfig(self, mem1,mem2,mem3):
        print ('Configuring Modem for SMS...')
        q = '"'
        c = ',' 
        self.sendATcmdUART('AT+CMGF=1',4000)
        time.sleep(0.01)
        
        cmd = 'AT+CPMS='
        cmd = cmd + q + mem1 + q + c + q + mem2 + q + c + q + mem3 + q
        self.sendATcmdUART(cmd,10)
        time.sleep(0.01)
        self.sendATcmdUART('AT+CNMI=2,1',4000)
        time.sleep(0.01)

        if 'OK' in self.response:
            print('Setup Complete')
        
    '''
    Function to Send an sms
    '''
    def SendSMS(self, number, message):
        print ('Sending SMS ...')
        q = '"'
        cmd = 'AT+CMGSO='
        cmd = cmd + q + number + q + ',' + q + message + q
        msg = self.sendATcmdUART(cmd,5000)
        if 'OK' in msg:
            print (' Sending successful')

        else:
            print (' Sending Unsuccessful')

    '''
    Function to read the command sent over sms
    '''         
    def ReadSMSCmd(self):
        self.ReadSMS(0)
        time.sleep(2)
            
        REC = '"REC READ"'
        CMGL = '+CMGL: '
        index = '0'
        counter = 0

        for i, _ in enumerate(self.response):
            if self.response[i:i + len(CMGL)] == CMGL:
                c_index = self.response[i + len(CMGL)]
                if c_index > index:
                    index = c_index
                     
        cmd = 'AT+CMGR=' 
        index = str(index)
        cmd = cmd + index
        self.sendATcmdUART(cmd,3000)
        
    '''
    Function to read the sms in storage, if index is 0 print all msgs
    '''
    def ReadSMS(self, index):
        if index == 0:
            self.content = self.sendATcmdUART('AT+CMGL="ALL"',1000)
        elif index > 0:
            cmd = 'AT+CMGR=' 
            index = str(index - 1)
            cmd = cmd + index
            self.content = self.sendATcmdUART(cmd,3000)
        return self.content
    
    '''
    Function to delete an sms in storeage, index refers to the position of the message
    '''
    def DeleteSMS(self, index):
        cmd = 'AT+CMGD='
        index = str(index)
        cmd = cmd + index
        print (cmd)
        self.content = self.sendATcmdUART(cmd,3000)
        return self.content    

    '''
    Function to make a call
    '''
    def MakeCall(self, number):
        cmd = 'ATD'
        cmd = cmd + number + ';'
        self.sendATcmdUART(cmd, 1)
        print ('Calling...')
        
    '''
    Function to hang up a call
    '''
    def Hangup(self):
        print (' Hanging up...')
        self.sendATcmdUART('ATH',1)

    '''
    Function to check signal quality
    '''
    def SignalCheck(self):
        '''See Signal Quality'''
        self.sendATcmdUART('AT+CSQ',1000)
        signal = self.response
        
        if (',' in self.response[8:10]):
            signal = signal.replace(',','')
            signal = int(signal[8:9])
        else:
            signal = int(self.response[8:10])
        
        if (signal < 10):
            signal = "Poor Signal"
        elif(signal > 10 and signal < 14):
            signal = "OK Signal"
        elif(signal > 14 and signal < 20):
            signal = "Good Signal"
        elif(signal >= 20 and signal < 99):
            signal = "Exceptional Signal"
        elif(signal >= 99):
            signal = "No Connection"
    
    '''
    Test if the modem is responding
    '''
    def Test(self):
        self.sendATcmdUART('AT',100)

    '''
    Check if the SIM is being detected
    '''
    def CheckSIM(self):
        msg = self.sendATcmdUART('AT+CPIN?',100)
        if 'OK' in msg:
            print ('SIM inserted')
        else:
            print ('SIM not inserted')
            
    '''
    Get GSM network status 
    '''
    def StatusGSM(self):
        self.sendATcmdUART('AT+MONI?',1000)

    '''
    GEt LTE network status
    '''
    def StatusLTE(self):
        self.sendATcmdUART('AT+CMGSI=4',1000)
        
    '''
    Soft Reset the modem
    '''    
    def ResetSIM(self):
        self.sendATcmdUART('AT+CRESET', 1000)
        
    '''
    Turn off the modem
    '''
    def PoweroffSIM(self):
        self.sendATcmdUART('AT+CPOF', 1000)        
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

           

