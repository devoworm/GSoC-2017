import numpy as np


def img_as_points(img):
    # Takes a binary image and return coordinates of black pixels in the binary image
    #
    # Input
    #  img : binary image
    #
    # Output:
    #  D : [n x 2] rows are coordinates
    #
    I = img.flatten()
    # Convert to boolean array and invert the pixel values
    I = ~np.array(I, dtype=np.bool)
    # Create a new array of all the non-zero element coordinates
    D = np.array(I.nonzero()).T
    print("A")
    return D - D.mean(axis=0)


def modified_hausdorf_distance(img1, img2):
    # Modified Hausdorff Distance
    #
    # Input
    #  img1 : binary image 1
    #  img2 :binary image 2
    #
    #  M.-P. Dubuisson, A. K. Jain (1994). A modified hausdorff distance for object matching.
    #  International Conference on Pattern Recognition, pp. 566-568.
    #
    itemA = img_as_points(img1)
    itemB = img_as_points(img2)

    D = cdist(itemA, itemB)
    print("")
    mindist_A = D.min(axis=1)
    mindist_B = D.min(axis=0)
    mean_A = np.mean(mindist_A)
    mean_B = np.mean(mindist_B)
    return max(mean_A, mean_B)
