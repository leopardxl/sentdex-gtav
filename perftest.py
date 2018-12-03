#from grabscreen import grab_screen
import numpy as np
from PIL import ImageGrab
import mss
import mss.tools
import time
import cv2

DEBUG = 1
SCREENS = {
    'gta-windowed': (0, 40, 800, 640),
    'ryancelcius': (30, 190, 670, 550)
}

def mss_grab_screen(region=None):
    with mss.mss() as sct:
        if region:
            monitor = {"left": region[0], "top": region[1], "width": region[2], "height": region[3]}
        else:
            monitor = {"top": 40, "left": 0, "width": 800, "height": 640}

        img = np.array(sct.grab(monitor))
        return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)


def run():
    global DEBUG
    dim = SCREENS['gta-windowed']
    #countdown()
    last_time = time.time()
    while True:
        cv_start_time = time.time()
        screen = np.array(ImageGrab.grab(bbox=(dim[0],dim[1], dim[2], dim[3])))
        cv_elapsed_time = time.time() - cv_start_time

        gs_start_time = time.time()
        #gscreen = grab_screen(region=dim)
        gs_elapsed_time = time.time() - gs_start_time

        mss_start_time = time.time()
        mscreen = mss_grab_screen(region=dim)
        mss_elapsed_time = time.time() - mss_start_time


        print("CV: ", cv_elapsed_time, "| WIN32: ", gs_elapsed_time,
            "| MSS: ", mss_elapsed_time)


        cv2.imshow('cv', screen)
        cv2.imshow('mss', mscreen)
        #cv2.imshow('window2', cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2RGB))




        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        if DEBUG > 0:
            print('loop took {} seconds'.format(time.time() - last_time))
        last_time = time.time()


if __name__ == '__main__':
    run()
