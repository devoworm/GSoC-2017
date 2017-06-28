import sys

import cv2

sys.path.append('../')

file = '../data/raw/s7-3.avi'

cap = cv2.VideoCapture(file)
fgbg = cv2.createBackgroundSubtractorMOG2()
while (1):
    ret, frame = cap.read()

    fgmask = fgbg.apply((frame))

    # erode = edge.canny(cv2.erode(fgmask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2)), iterations=1))
    # closing = cv2.morphologyEx(erode, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)),
    #                            iterations=1)

    # erode = edge.edge(fgmask)
    cv2.imshow('frame', fgmask)
    k = cv2.waitKey(20) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
