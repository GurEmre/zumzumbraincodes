import struct
import smbus
bus=smbus.SMBus(1)

#def parse_data(address, register, num_bytes):
   #    """

     #  Parse multiple bytes long message by using I2C
    #   """
#    try:
 #       read_block = bus.read_i2c_block_data(address, register, num_bytes)
 #   except IOError:
 #       print("IOerr")
 #       return None
            # If message have error use the last value
 #   byte_list = ''
 #   for byte in read_block:
 #       byte_list += chr(byte)
        # reverse ordering of incoming data
  #      byte_list = byte_list[::-1]
  #   try:
            # unpack value obtained according to the struct_type
            # the result of unpack is a tuple get the first item
   #     val = struct.unpack("=h", byte_list)[0]
   #  except struct.error
            # If message have error se the last value
  #      print("I2C value Error")
  #      return None

  #return val
# bus.write_byte(8, 255)
#print(parse_data(8, 255, 2))
import struct
from smbus import SMBus
addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1
bus=smbus.SMBus(1)

numb = 1
#print ("Enter Motor value")

while numb == 1:
    numb=2
    while numb == 2:
        register = int(input(">>>>   "))
       # register=0
        numb=3
    while numb == 3:
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