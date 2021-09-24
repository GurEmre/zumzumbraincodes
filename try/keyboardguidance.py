import struct
import smbus
import sys, select
bus=smbus.SMBus(1)
from smbus import SMBus
addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1
numb = 1
#print ("Enter Motor value")

while numb == 1:
    numb=2
    while numb == 2:
        register = int(input(">>Which motor>>   "))
       # register=0
        numb=3
    while numb == 3:
        print "You have ten seconds to answer!"
        w, a, d = select.select( [sys.stdin], [], [], 3 )
        if (w):
            #print "You said", sys.stdin.readline().strip()
            ledstate = int(100) #int(input(">>>>   "))
        else:
            print "You said nothing!"
        
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