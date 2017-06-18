import cv2
import numpy as np

"""
Edge detector
accepts a greyscale image
"""

# hedge increases the wiegit
def edge(img, hedge=1, vedge=1):
    # make a matrix of column matrix of (1,1). This matrix is applied as a kernel on the matrix of the photo
    kernelVertical = np.matrix('1  ;-1')
    # the kernel being applied on the image matrix. img-image on which kernel is to be applied
    verticalEdge = cv2.filter2D(img, -1, kernelVertical)
    kernelVertical1 = np.matrix('1  ; -1')
    verticalEdge1 = cv2.filter2D(img, -1, kernelVertical1)
    verticalEdgeFinal = cv2.add(verticalEdge, verticalEdge1);

    kernelHorizontal = np.matrix("1  -1")
    horizontalEdge = cv2.filter2D(img, -1, kernelHorizontal)
    kernelHorizontal1 = np.matrix("-1 1")
    horizontalEdge1 = cv2.filter2D(img, -1, kernelHorizontal1)
    horizontalEdgeFinal = cv2.add(horizontalEdge, horizontalEdge1)
    dst = (cv2.add((horizontalEdgeFinal) ^ hedge, (verticalEdgeFinal) * vedge))
    return dst


def canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    return edged

