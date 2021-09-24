import struct
import smbus
bus=smbus.SMBus(1)
from smbus import SMBus
addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1
numb = 1
#print ("Enter Motor value")
from pynput import keyboard
while numb == 1:
    numb=2
    while numb == 2:
        register = int(input(">>Which motor>>   "))
       # register=0
        numb=3
    while numb == 3:
        with keyboard.Events() as events:
        # Block for as much as possible
        event = events.get(1e6)
        if event.key == keyboard.KeyCode.from_char('s'):
            print("YES")
        ledstate = int(input(">>>>   "))
        #ledstate = int(8888888)
        bytelist= struct.pack('=h',ledstate)
        intlist=[]
        for byteval in bytelist:
            intval=ord(byteval)
            intlist.append(intval)
        try:
            bus.write_block_data(addr, register,intlist)
        except IOError:
            print('IOerr')
        numb=1