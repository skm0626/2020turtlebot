import cv2
import numpy as np
from SlidingWindow2 import SlidingWindow


def region_of_interest(image, image_copy, width, height1, height2, roiw, roih):
    src = np.array([[width / 2 - 320, height1],
                    [width / 2 + 320, height1],
                    [width / 2 + 360, height2],
                    [width / 2 - 360, height2]], np.float32)

    for i in src:
        cv2.circle(image_copy, (i[0], i[1]), 5, (0,0,255),-1)

    dst = np.array([[0, 0], [roiw, 0], [roiw, roih], [0, roih]], np.float32)
    M = cv2.getPerspectiveTransform(src, dst)
    return cv2.warpPerspective(image, M, (roiw, roih))

# show image and return lpos, rpos
def process_image(frame):
    global Width

    # gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # blur
    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
    blur_gray = cv2.GaussianBlur(blur_gray, (kernel_size, kernel_size), 0)
    # canny edge
    # low_threshold = 45
    # high_threshold = 100
    low_threshold = 5  # 41
    high_threshold = 60  # 70
    edge_img = cv2.Canny(np.uint8(blur_gray), low_threshold, high_threshold)

    return edge_img

slidingwindow = SlidingWindow()

cap = cv2.VideoCapture('line_tracing.avi')

x_old = 320

setPoint = 320
error = 0
pTerm = 0.0
cw_cnt = 0
cw_sum_old = 0

PART = 1

while(cap.isOpened()):
    ret, image = cap.read()
    image = cv2.resize(image, (640,480))
    image_copy = image.copy()

    # image height
    h = image.shape[0]
    # image width
    w = image.shape[1]

    while not image.size == (h * w * 3):
        continue

    edge_img = process_image(image)

    # Bird Eyes View Image
    warp = region_of_interest(edge_img, image_copy, 640, 390, 420, 800, 448)

    out_img, x_location = slidingwindow.slidingwindow(warp)

    if x_location is None:
        cv2.circle(out_img, (x_old, 380), 5, (255, 0, 0), -1)
        # x_location = x_old - 200
        #x_location = -100
        x_location = x_location_old
    #elif x_location != None and PART == 3:
    #    if abs(x_location - x_location_old) > 45:
            #print('x_location - x_old:                                 ', abs(x_location - x_old))
     #       x_location = x_location_old
     #       cv2.circle(out_img, (x_location, 380), 5, (255, 0, 255), -1)
    else:
        cv2.circle(out_img, (x_location, 380), 5, (0, 0, 255), -1)
        x_location_old = int(x_location)


    cv2.imshow('result',out_img)
    if cv2.waitKey(30)&0xFF == ord('q'):
        break

cap.release()
cap.destroyAllWindows()
