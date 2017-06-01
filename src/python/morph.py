import cv2
import edge
import numpy as np
import thirdparty.morphsnakes.morphsnakes as mh
from matplotlib import pyplot as ppl


def circle_levelset(shape, center, sqradius, scalerow=1.0):
    """Build a binary function with a circle as the 0.5-levelset."""
    grid = np.mgrid[list(map(slice, shape))].T - center
    phi = sqradius - np.sqrt(np.sum((grid.T)**2, 0))
    u = np.float_(phi > 0)
    return u

img = cv2.imread('../data/interim/spim2/c97.jpg',0)

filtered = cv2.bilateralFilter(img, 9,350,350)
edgeShape = edge.edge(filtered)
k, dst = cv2.threshold(edgeShape, 4, 255, cv2.THRESH_BINARY)
dilate = cv2.erode(dst, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2)), iterations=1)
closing = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)),iterations=1)
final = cv2.dilate(closing, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=1)
_ , contours, _ = cv2.findContours(final, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


gI = mh.gborders(img, alpha=1000, sigma=5.48)
cv2.imshow("gI",gI)
#cv2.waitKey(0)

mgac = mh.MorphGAC(gI, smoothing=1, threshold=0.31, balloon=-1)
#mgac = mh.MorphACWE(img, smoothing=1, lambda1=1, lambda2=3)

for cnt in [12, 13, 14, 15, 16, 17, 18]:
    mask = np.zeros(img.shape, np.uint8)
    cv2.drawContours(mask, contours, cnt, (255), -1)
    mask[mask > 0] = 1
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)), iterations=1)
    mgac.levelset = mask
    cv2.imshow("levelset",mgac.levelset)
    cv2.waitKey(0)
    ppl.figure()
    mh.evolve_visual(mgac, num_iters=300, background=img)
    print("done")
    ppl.show()
