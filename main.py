import numpy as np
from PIL import ImageGrab
import cv2
import time
from grabscreen import grab_screen
from numpy import ones, vstack
from numpy.linalg import lstsq
from directkeys import PressKey, ReleaseKey, W, A, S, D
from statistics import mean
from draw_lanes import draw_lanes


DEBUG = 1
SCREENS = {
    'gta-windowed': (0, 40, 800, 640),
    'ryancelcius': (30, 190, 670, 550)
}


def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked


def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    #processed_img = original_image
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    #processed_img = cv2.GaussianBlur(processed_img, (5,5), 0 )

    vertices = np.array([[10,500], [10,300], [300,200], [500,200], [800,300], [800,500]])
    processed_img = region_of_interest(processed_img, [vertices])


    min_line_length = 20
    max_line_gap = 15
    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180, np.array([]), min_line_length, max_line_gap)
    m1 = 0
    m2 = 0

    try:
        lane_color = [0,255,0]
        l1, l2, m1, m2 = draw_lanes(original_image, lines)
        cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), lane_color, 30)
        cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), lane_color, 30)
    except Exception as e:
        print(str(e))
        pass
    try:
        for coords in lines:
            coords = coord[0]
            try:
                cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), lane_color, 30)
            except Exception as e:
                print(str(e))
    except Exception as e:
        pass
    if DEBUG > 100:
        print(lines)


    return processed_img, original_image, m1, m2


def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)


def left():
    PressKey(A)
    ReleaseKey(W)
    ReleaseKey(D)
    ReleaseKey(A)


def right():
    PressKey(D)
    ReleaseKey(A)
    ReleaseKey(W)
    ReleaseKey(D)

def slow():
    ReleaseKey(A)
    ReleaseKey(W)
    ReleaseKey(D)


def countdown():
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

def control_system(m1, m2):
    if m1 < 0 and m2 < 0:
        right()
    elif m1 > 0 and m2 > 0:
        left()
    else:
        straight()

def run():
    global DEBUG
    box = SCREENS['gta-windowed']
    #countdown()
    last_time = time.time()
    while True:
        #screen = np.array(ImageGrab.grab(bbox=(0,40, 800, 640)))
        screen = np.array(ImageGrab.grab(bbox=box))
        new_screen, original_image, m1, m2 = process_img(screen)
        cv2.imshow('window', new_screen)
        cv2.imshow('original', cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
        #cv2.imshow('window2', cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2RGB))


        control_system(m1, m2)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        if DEBUG > 0:
            print('loop took {} seconds'.format(time.time() - last_time))
        last_time = time.time()


if __name__ == '__main__':
    run()
