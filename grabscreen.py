#from grabscreen import grab_screen
import numpy as np
import mss
import mss.tools
import cv2


def grab_screen(region=None):
    with mss.mss() as sct:
        if region:
            monitor = {"left": region[0], "top": region[1], "width": region[2], "height": region[3]}
        else:
            monitor = {"top": 40, "left": 0, "width": 800, "height": 640}

        img = np.array(sct.grab(monitor))
        return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
