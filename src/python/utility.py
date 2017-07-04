import glob

import cv2
import matplotlib.pyplot as plt
import numpy as np


# utility function to show an image in a separate window
def sh(img, title="img"):
    cv2.imshow(title, img)
    cv2.waitKey(0)


# utility function for plotting a greyscale image inline
def plotG(img):
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB))


# utility function for plotting a binary(0,1) image inline
def plotB(img, title="plot"):
    plt.figure()
    img[img > 0] = 255
    img[img <= 0] = 0
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB))
    plt.title(title)


def getBinary(img):
    """
    Gives a binary image(consisting of 0 and 1) partitioned at 0
    :param img: A image
    :return: All elements less than equal to 0 are 0 and all +ve elements are one
    """
    img[img > 0] = 1
    img[img <= 0] = 0
    return img


def count(img):
    """
    Gives a count of number of pixels involved

    :param img: a binary image
    :return: a dictionary x:y. Where x is the pixel value and y is the count of it
    """
    unique, counts = np.unique(img, return_counts=True)
    return dict(zip(unique, counts))


def hinton(matrix, max_weight=None, ax=None):
    """Draw Hinton diagram for visualizing a weight matrix."""
    ax = ax if ax is not None else plt.gca()

    if not max_weight:
        max_weight = 2 ** np.ceil(np.log(np.abs(matrix).max()) / np.log(2))

    ax.patch.set_facecolor('gray')
    ax.set_aspect('equal', 'box')
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())

    for (x, y), w in np.ndenumerate(matrix):
        color = 'white' if w > 0 else 'black'
        size = np.sqrt(np.abs(w) / max_weight)
        rect = plt.Rectangle([x - size / 2, y - size / 2], size, size,
                             facecolor=color, edgecolor=color)
        ax.add_patch(rect)

    ax.autoscale_view()
    ax.invert_yaxis()


def folderToImages(folderpath):
    """
    Returns a list of binary images present in the folderpath. It is thresholded at 127 and getBinary is applied.

    :param folderpath: Path of the folder in which images are present
    :return: returns a list binary image (@getBinary) present in folder path
    """
    images = []
    for file in glob.glob(folderpath + "*"):
        ret, thresh = cv2.threshold(cv2.imread(file, 0), 127, 255, cv2.THRESH_BINARY)
        getBinary(thresh)
        images.append(thresh)
    return images
