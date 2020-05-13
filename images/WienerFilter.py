import cv2 as cv
import numpy as np


def loadImage(file_name, image_format):
    image = cv.imread(file_name, image_format)
    return image


def saturate_cast(val):

    if val.any() < 0:
        return np.array([255, 255, 255])
    elif val.any() > 255:
        return np.array([255, 255, 255])
    return val


class WienerFilter():
    def __init__(self, input, filter_size):
        self.input = input
        self.filter_size = filter_size
        if input.ndim != 2:
            print("Image not 2d")
        if filter_size[0] % 2 != 1 or filter_size[1] % 2 != 1 or filter_size[0] <= 1 or filter_size[1] <= 1:
            print("Invalid filter dimension")

    def estimateOutput(self):
        means = cv.boxFilter(src=self.input, ddepth=cv.CV_64F, ksize=tuple(self.filter_size), anchor=(-1, 1),
                             normalize=True, borderType=cv.BORDER_REPLICATE)
        square_means = cv.sqrBoxFilter(src=self.input, ddepth=cv.CV_64F, ksize=tuple(self.filter_size), anchor=(-1, 1),
                                       normalize=True, borderType=cv.BORDER_REPLICATE)

        means2 = cv.multiply(means, means)

        # calculating the variance matrix
        variances = square_means - means2

        # estimating noise variance by finding projections across length and width
        avgVarianceMat = cv.reduce(variances, 1, cv.REDUCE_SUM, -1)
        avgVarianceMat = cv.reduce(avgVarianceMat, 0, cv.REDUCE_SUM, -1)

        noiseVar = (avgVarianceMat / self.input.shape[0] * self.input.shape[1]).item(0)
        print(noiseVar)
        print(variances[0][0])

        y = np.zeros(self.input.shape)
        for row in range(self.input.shape[0]):
            for col in range(self.input.shape[1]):
                y[row][col] = means[row][col] + max(0, variances[row][col] - noiseVar) * (
                        self.input[row][col] - means[row][col]) / max(variances[row][col], noiseVar)

        return y

    def estimateOutputColorised(self):
        # get all local means in
        means = cv.boxFilter(src=self.input, ddepth=cv.CV_64F, ksize=tuple(self.filter_size), anchor=(-1, 1),
                             normalize=True, borderType=cv.BORDER_REPLICATE)
        square_means = cv.sqrBoxFilter(src=self.input, ddepth=cv.CV_64F, ksize=tuple(self.filter_size), anchor=(-1, 1),
                                       normalize=True, borderType=cv.BORDER_REPLICATE)

        means2 = cv.multiply(means, means)
        variances = square_means - means2

        avgVariance = cv.reduce(variances, 0, cv.REDUCE_SUM, -1)
        avgVariance = cv.reduce(avgVariance, 1, cv.REDUCE_SUM, -1)

        noiseVar = avgVariance / self.input.shape[0] * self.input.shape[1] * self.input.shape[2]

        noiseVar = np.reshape(noiseVar, (1, 3))

        y = np.zeros(self.input.shape)

        for row in range(self.input.shape[0]):
            for col in range(self.input.shape[1]):
                y[row][col] = saturate_cast(
                    means[row][col] + np.maximum(np.zeros(noiseVar[0].shape), variances[row][col] - noiseVar[0]) * (
                            self.input[row][col] - means[row][col]) / np.maximum(variances[row][col], noiseVar[0]))

        return y
