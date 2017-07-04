from .utility import *


def f1_get_score(prediction_pixels, truth_pixels, visualize=False, mini=False):
    truth_pixels_liberal = cv2.erode(truth_pixels, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10)), iterations=1)
    truth_pixels_liberal = getBinary(truth_pixels_liberal)
    prediction_pixels_liberal = cv2.erode(prediction_pixels, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10)),
                                          iterations=1)  # img is x. This kernel should be bigger
    prediction_pixels_liberal = getBinary(prediction_pixels_liberal)
    # if the kernel is applied to x, then tp stores the number of pixels that y have in that kernal.
    # #this img is x
    # we performed dilation in the above case

    if (visualize):
        plotB(prediction_pixels_liberal, "Dilated predicted pixels")
        plotB(truth_pixels_liberal, "Dilated ground truth pixels")

    """
    matrix that verifies true positive. I
    t contains one where x had a membrance marked and the labelled image had atleast one pixel of membrane within the kernel specified
    #
        What have I tried to do?
        I'm going to each black pixel of y(the labelled image) and checking if a x has a corresponding black pixel in the corrsponding pixel region.
        If yes(that means a pixel has been correctly classified or x has that feature in y), than we tickmark it; shown by np.bitwise_and(x_dilated,y1).
        y - correctly_classified_pixels
    """

    correctly_classified_pixels_1 = np.bitwise_or(prediction_pixels_liberal, truth_pixels)
    correctly_classified_pixels_2 = np.bitwise_or(truth_pixels_liberal, prediction_pixels)
    correctly_classified_pixels_1 = getBinary(correctly_classified_pixels_1)
    correctly_classified_pixels_2 = getBinary(correctly_classified_pixels_2)

    fn = truth_pixels - correctly_classified_pixels_1  # fn implies the membrane are that haven't been detected
    fn = getBinary(fn)

    fp = correctly_classified_pixels_2 - prediction_pixels  # fn imples the pixels that  falsly detected membrane area
    fp = getBinary(fp)

    if (visualize):
        plotB(correctly_classified_pixels_1, "Correctly classified")
        plotB(fn, "The membrane that wasn't detected")
        plotB(fp, "The extra membrance detected ")
    if (mini):
        plotB(fn, "The membrane that wasn't detected")
        plotB(fp, "The extra membrance detected ")

    fp_pixel_count = np.count_nonzero(fp)
    fn_pixel_count = np.count_nonzero(fn)
    tp_pixel_count = int(
        (np.count_nonzero(correctly_classified_pixels_1) + np.count_nonzero(correctly_classified_pixels_2)) / 2)

    precision = float(tp_pixel_count) / float(tp_pixel_count + fp_pixel_count)
    recall = float(tp_pixel_count) / float(tp_pixel_count + fn_pixel_count)

    f1_score = (2 * precision * recall) / (precision + recall)
    return f1_score


def get_precision(tp, fp):
    return float(tp) / float(tp + fp)


def get_recall(tp, fn):
    return float(tp) / float(tp + fn)
