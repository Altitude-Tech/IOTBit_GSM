### Need the IOTBit_Library_V1 file to run IOTBit cmds
from IOTBit_Library_GSM_Variant import Modem

import time

APN= 'everywhere' # YOUR APN HERE
GSM = Modem(APN,'GSM')



GSM.sendATcmdUART('AT+CPIN?',1000)   #check SIM

print (GSM.response)
