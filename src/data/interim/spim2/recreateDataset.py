import cv2
import glob
k = glob.glob("../img/*.jpg")
n = 0
x = int(1344 / 3)
for file in k:
    im = cv2.imread(file)
    a = im[0:688, 0:x]
    b = im[0:688, x:2 * x]
    c = im[0:688, 2 * x:3 * x]
    cv2.imwrite("a" + str(n) + ".jpg", a)
    cv2.imwrite("b" + str(n) + ".jpg", b)
    cv2.imwrite("c" + str(n) + ".jpg", c)
    print(n)
    n=n+1
