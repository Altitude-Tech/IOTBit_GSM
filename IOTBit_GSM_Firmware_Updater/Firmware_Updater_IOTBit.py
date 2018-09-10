#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import os



Boot0 = 5
RST = 6
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM) ## Use board numbering
GPIO.setup(Boot0, GPIO.OUT) ## Set up GPIO Pin 31 to output
GPIO.setup(RST, GPIO.OUT) ## Set up GPIO Pin 29 to output

def Bootloader_Mode_On():
    GPIO.output(Boot0, GPIO.HIGH) ## Set GPIO Pin 29 to low
    print "Boot 0 set high"
    GPIO.output(RST, GPIO.LOW) ## Set GPIO Pin 31 to low
    print "Resetting"
    time.sleep(1)
    GPIO.output(RST, GPIO.HIGH) ## Set GPIO Pin 31 to low

def Bootloader_Mode_Off():
    GPIO.output(Boot0, GPIO.LOW) ## Set GPIO Pin 29 to low
    print "Boot 0 set low"
    GPIO.output(RST, GPIO.LOW) ## Set GPIO Pin 31 to low
    print "Resetting"
    time.sleep(1)
    GPIO.output(RST, GPIO.HIGH) ## Set GPIO Pin 31 to low

try:

    #Set the board to bootloader mode
    Bootloader_Mode_On()
    time.sleep(1)

    # Get UART Port

    port = raw_input("Please enter your UART port, for RPI 2 its /dev/ttyAMA0 and for RPI 3 its /dev/ttyS0 or /dev/serial0: ")

    # Get Filename of binary file to be uploaded

    #filename = raw_input("Please enter the firmware filename, including path: ")

    # Run stm32loader to upload new firmware
    output = "python stm32loader.py -e -w -v -p " + port + " -b 115200 IOTBitFirmware_GSM_V1.02.bin"
    
    os.system(output)

    time.sleep(1)

    # Turn Bootloader mode off 
    Bootloader_Mode_Off()

    time.sleep(1)

except KeyboardInterrupt:
    print " Exiting"

finally:
    GPIO.cleanup()
