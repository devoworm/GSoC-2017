from .utility import *


class Validation(object):
    """
    matrix that verifies true positive. I
    t contains one where x had a membrance marked and the labelled image had atleast one pixel of membrane within the kernel specified
    #
        What have I tried to do?
        I'm going to each black pixel of y(the labelled image) and checking if a x has a corresponding black pixel in the corrsponding pixel region.
        If yes(that means a pixel has been correctly classified or x has that feature in y), than we tickmark it; shown by np.bitwise_and(x_dilated,y1).
        y - correctly_classified_pixels
    """

    def __init__(self):
        pass

    def fit(self, prediction_pixels, truth_pixels):
        self.prediction_pixels = prediction_pixels
        self.truth_pixels = truth_pixels
        self.truth_pixels_liberal = cv2.erode(truth_pixels, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10)),
                                              iterations=1)
        self.truth_pixels_liberal = getBinary(self.truth_pixels_liberal)
        self.prediction_pixels_liberal = cv2.erode(prediction_pixels,
                                                   cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10)),
                                                   iterations=1)  # img is x. This kernel should be bigger
        self.prediction_pixels_liberal = getBinary(self.prediction_pixels_liberal)

        correctly_classified_pixels_1 = np.bitwise_or(self.prediction_pixels_liberal, truth_pixels)
        correctly_classified_pixels_2 = np.bitwise_or(self.truth_pixels_liberal, prediction_pixels)
        correctly_classified_pixels_1 = getBinary(correctly_classified_pixels_1)
        self.ccorrectly_classified_pixels_2 = correctly_classified_pixels_2 = getBinary(correctly_classified_pixels_2)

        fn = truth_pixels - correctly_classified_pixels_1  # fn implies the membrane are that haven't been detected
        self.fn_img = fn = getBinary(fn)

        fp = correctly_classified_pixels_2 - prediction_pixels  # fn imples the pixels that  falsly detected membrane area
        self.fp_img = fp = getBinary(fp)

        self.fp = np.count_nonzero(fp)
        self.fn = np.count_nonzero(fn)
        self.tp = int(
            (np.count_nonzero(correctly_classified_pixels_1) + np.count_nonzero(correctly_classified_pixels_2)) / 2)

    def get_precision(self):
        return float(self.tp) / float(self.tp + self.fp)

    def get_recall(self):
        return float(self.tp) / float(self.tp + self.fn)

    def get_f_score(self, alpha=0.5):
        return 1.0 / (
            (alpha / self.get_precision()) + ((1 - alpha) / self.get_recall()))

    def plot(self, big=False):
        plotB(self.fn_img, "Membrane that wasn't detected")
        plotB(self.fp_img, "This membrane doesn't exists")
        if (big):
            plotB(self.ccorrectly_classified_pixels_2, "Correctly classified pixels")
            plotB(self.prediction_pixels, "Prediction pixels")
            plotB(self.truth_pixels, "Truth Pixels")
