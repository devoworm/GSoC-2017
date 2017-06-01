import cv2
import edge
import numpy as np
import scipy.ndimage as nd
from thirdparty.chanvese.chanvese import chanvese

img = nd.imread('../data/interim/spim2/c97.jpg', flatten=True)
edgeShape = edge.edge(cv2.bilateralFilter(cv2.imread('../data/interim/spim2/c97.jpg', 0), 9,350,350))
k, dst = cv2.threshold(edgeShape, 4, 255, cv2.THRESH_BINARY)
dilate = cv2.erode(dst, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2)), iterations=1)
closing = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)),
                           iterations=1)
final = cv2.dilate(closing, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=1)
# cv2.imshow("final",final)
# cv2.waitKey(0)
_, contours, _ = cv2.findContours(final, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
mask = np.zeros(img.shape, np.uint8)
cv2.drawContours(mask, contours, 12, (255), -1)
cv2.imshow("final",mask)
mask[mask>0] = 1
cv2.waitKey(0)
chanvese(img, mask, max_its=1000, display=True, alpha=0.3)
