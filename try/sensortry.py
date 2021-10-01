import time
import struct
import smbus
bus=smbus.SMBus(1)

def parse_data(address, register, num_bytes):
        """
        Parse multiple bytes long message by using I2C
        """
        try:
            read_block = bus.read_i2c_block_data(address, register, num_bytes)
        except IOError:
            print("IOerr")
            return None
            # If message have error use the last value
        byte_list = ''
        for byte in read_block:
            byte_list += chr(byte)
        # reverse ordering of incoming data
        byte_list = byte_list[::-1]
        try:
            # unpack value obtained according to the struct_type
            # the result of unpack is a tuple get the first item
            val = struct.unpack("=h", byte_list)[0]
        except struct.error:
            # If message have error use the last value
            print("I2C value Error")
            return None
        return val
# bus.write_byte(8, 255)
while(1):
     print ("\n-----------------------------------------------------\n")
     print ("255:\n")
     print(parse_data(8, 255, 2))
     print ("254:\n")
     print(parse_data(8, 254, 2))
     print ("253:\n")
     print(parse_data(8, 253, 2))
     print ("252:\n")
     print(parse_data(8, 252, 2))
     time.sleep(1)