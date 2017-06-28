import cv2

cap = cv2.VideoCapture('s7-3.avi')
i = 1
while (cap.isOpened()):
    ret, frame = cap.read()
    cv2.imwrite("../interim/s7_spim3/" + str(i) + ".jpg", frame)
    i = i + 1
    print(str(i))
