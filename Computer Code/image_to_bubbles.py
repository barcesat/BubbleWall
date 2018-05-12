#!/usr/bin/python

import numpy as np
import cv2
import time
from serial import Serial
import sys
import glob

num_pumps = 35
num_rows = num_pumps
cmd_barker = '<'
cmd_sig = '>'
on_cmd = ''.join([cmd_barker, '1' * num_pumps, cmd_sig])
off_cmd = ''.join([cmd_barker, '0' * num_pumps, cmd_sig])
pump_on_time = 0.1
pump_off_time = 3
time_between_pumps = pump_on_time + pump_off_time

def load_and_convert_img(path):
    # Load image in grayscale
    im_gray = cv2.imread(path, 0)

    # Resize image according to the number of pumps
    resized_im = cv2.resize(im_gray, (num_rows, num_pumps))

    # Convert image to black and white
    (thresh, im_bw) = cv2.threshold(resized_im, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    return im_bw

def dbg_play_bubbles(img):
    for row in xrange(num_rows):
        for col in xrange(num_pumps):
            if img[row][col]:
                print ' ',
            else:
                print '*',
        print ''
        time.sleep(0.1)

def play_bubbles(img):
    # Find usb-serial interface
    if sys.platform.startswith('linux'):
        usb_ser_list = glob.glob ('/dev/ttyACM[0-9]')
    else:
        raise Exception("Only Linux is supported")

    if len(usb_ser_list) < 1:
        raise Exception("No serial interface to connect to")

    serial_port = usb_ser_list[0]
    print "Connecting to", serial_port

    with Serial(serial_port, 115200) as s:
        s.reset_input_buffer()
        for row in xrange(num_rows):
            cmd = ''
            for col in xrange(num_pumps):
                if img[row][col]:
                    cmd += '0'
                else:
                    cmd += '1'
            cmd = ''.join([cmd_barker, cmd, cmd_sig])

            # Send command to turn on relevant pumps for row
            s.write(cmd)
            s.flushOutput()
            print cmd
            #time.sleep(pump_on_time)
            time.sleep(time_between_pumps)

            # Send command to turn off all pumps
            #s.write(off_cmd)
            #s.flushOutput()
            #time.sleep(pump_off_time)

            # Clear input buffer from serial, don't care about replies
            s.reset_input_buffer()

if __name__ == "__main__":
    img_path = 'image.png'
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
    img = load_and_convert_img(img_path)
    play_bubbles(img)





