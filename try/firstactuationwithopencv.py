from __future__ import division
import os
import cv2.aruco as aruco
import numpy as np
import cv2
import sys
import time
import struct
import smbus

import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

pwm.set_pwm_freq(60)
bus=smbus.SMBus(1)
# import util_funcs as uf


def get_aruco(frame):
    """
    Get aruco IDs , rvec and tvec from
    camera frame use a debug img. with axes drawn
    """
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    aruco_params = aruco.DetectorParameters_create()
    marker_len = 0.05 # m
    camera_matrix=[[496.7823800915991, 0.0, 324.1279636602913]
        ,[0.0, 496.55172525873394, 250.3952308419727]
        ,[0.0, 0.0, 1.0]]
    dist_coeffs=[0.17329499537224216, -0.38275429309256476, 0.003487398733261259, -0.0043057697616395735, 0.21908013027217219]
    camera_matrix = np.array(camera_matrix)
    dist_coeffs = np.array(dist_coeffs)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # crop image in vertical axis for min. computation
    h, w = gray.shape
    # cropped_h = int(h / 6)
    x = 0
    # y = int((h - cropped_h) / 2)
    y = 0
    gray = gray[y:y+h, x:x+w]

    corners, ids, rejectedImgPoints = aruco.detectMarkers(
        gray, aruco_dict, parameters=aruco_params)

    tvecs = []
    aruco_ids = []
    if ids is not None:
        for indx, corner in enumerate(corners):
            # aruco detected
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(
                corner, marker_len, camera_matrix, dist_coeffs)
            # in rads
            rvec = rvec[0][0]
            # in meters
            tvec = tvec[0][0]
            # rospy.loginfo("x : {}, y : {}, z : {}".format(tvec[0], tvec[1], tvec[2]))
            aruco_id = ids[indx]
            if aruco_id < 10:
                # only ids larger than 10 are robots
                continue
            tvecs.append([tvec[0], tvec[1], tvec[2], aruco_id[0]])
            aruco_ids.append(aruco_id)
            # get image with axes drawn on aruco

            gray = aruco.drawAxis(gray, camera_matrix, dist_coeffs, rvec, tvec, marker_len)


        # publish img with all aruco axes drawn
        # cv2.circle(gray,(int(1920/2)+ 100,int(1080/2)+100), 300, (0,0,255), 1)
    return tvecs,aruco_ids

def start(args):

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        print(frame.shape[:2])
        start_time = time.time()
        tvecs,aruco_ids = get_aruco(frame)
        print(aruco_ids)
        if (aruco_ids != []):
            print(tvecs)
            for tvec in tvecs:
                print("distance:")
                print(tvec[2])
                if (tvec[2]>0.09):
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
                            register = int(input(0))
                        # register=0
                            numb=3
                        while numb == 3:
                            ledstate = int(input(100))
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
                            ledstate=0
                            register=0
                            break
                else:
                    print('Moving servo on channel 0, press Ctrl-C to quit...')
                    while True:
                        status = int(input(">>>>   "))
                        if(status == 0):
                            pwm.set_pwm(0, 0, 600)
                            pwm.set_pwm(1, 0, 100)
                            pwm.set_pwm(2, 0, 600)
                        if(status == 1):
                            pwm.set_pwm(0, 0, 600)
                            pwm.set_pwm(1, 0, 100)
                            pwm.set_pwm(2, 0, 400)
                        if(status == 2):
                            pwm.set_pwm(0, 0, 600)
                            pwm.set_pwm(1, 0, 100)
                            pwm.set_pwm(2, 0, 600)
                        if(status == 3):
                            pwm.set_pwm(0, 0, 100)
                            pwm.set_pwm(1, 0, 600)
                            pwm.set_pwm(2, 0, 600)        
        print(time.time() - start_time)
        time.sleep(1)
    cap.release()
    # frame = cv2.imread('test.jpeg')
    # gray, tvecs = get_aruco(frame)
    # cv2.imshow("aruco_det", gray)
    # # waits for user to press any key
    # # (this is necessary to avoid Python kernel form crashing)
    # cv2.waitKey(0)
    # # closing all open windows
    # cv2.destroyAllWindows()

    print(tvecs)
    # for tvec in tvecs:
    #     if tvec[2] == 43:
    #         center = tvec[0:2]
    #     elif tvec[2] == 40:
    #         radius = uf.euclidian_dist(center, tvec[0:2])
    # print("Radius of cue{}".format(radius))
    # print("Center of cue{}".format(center))
if __name__ == '__main__':
        start(sys.argv)
