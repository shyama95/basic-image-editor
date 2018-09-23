# ---------------------------------------------------------------#
# __name__ = "BasicImageEditor_EE610_Assignment"
# __author__ = "Shyama P"
# __version__ = "1.0"
# __email__ = "183079031@iitb.ac.in"
# __status__ = "Development"
# ---------------------------------------------------------------#

# All array operations are performed using numpy library
import numpy as np
# OpenCV2 library is used for color space conversion only
import cv2

# This class defines the implementation of all image processing functions
class ImageProcessorClass(object):

    # compute negative of the image passed as ndarray
    def image_negative(self, image):
        # find no of rows and columns in the ndarray of image passed
        image_row = image.shape[0]
        image_column = image.shape[1]

        # convert image from HSV space to BGR space
        image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
        # create an array equivalent to image array with all values as 255
        output = np.uint8(255 * np.ones((image_row, image_column, 3)))
        # deduct image from the array of 255 i.e. each pixel is inverted
        output = output - image
        # convert image back to HSV from BGR
        output = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)

        #  return the computed image
        return output

    # compute histogram equalization of the image passed as ndarray
    def histogram_equalization(self, image):
        # find no of rows and columns in the ndarray of image passed
        image_row = image.shape[0]
        image_column = image.shape[1]

        # count the no of values corresponding to each value in the V channel of image
        # matrix give a minimum length of 256 to the counting to ensure all 256 pixel
        # values are covered or pixel values not available in image are set to zero
        pmf = np.bincount(image.ravel(), minlength=256)
        # compute pmf by dividing histogram by total no of pixels in image
        pmf = pmf / (image_row * image_column)
        # compute cdf as cumulative sum of pmf
        cdf = pmf.cumsum()
        # derive lookup for pixel values by multiplying cdf with 255 (max pixel value)
        # round the lookup to lower integer to avoid the pixel value 256
        pmf_lookup = np.uint8(np.floor(cdf * 255))

        # create a copy of input image
        output = image.copy()

        # for each pixel value replace the value with the corresponding value in
        # lookup generated
        for r in range(256):
            output[image == r] = pmf_lookup[r]

        #  return the computed image
        return output

    # compute gamma correction of the image passed as ndarray based on gamma value passed
    def gamma_correction(self, image, gamma):
        # to keep image pixel values in the range 0 to 255 define a
        # constant = 255/ (max value in gamma correction)
        normalization_const = 255.0 / np.float_power(255, gamma)

        # compute output = constant * in^gamma
        # float_power used to accommodate large values in in^gamma
        output = np.uint8(normalization_const * np.float_power(image, gamma))

        #  return the computed image
        return output

    # compute log transform of the image passed as ndarray
    def log_transform(self, image):
        # find no of rows and columns in the ndarray of image passed
        image_row = len(image)
        image_column = len(image[0])

        # to keep image pixel values in the range 0 to 255 define a
        # constant = 255/ (max value in log transform)
        normalization_const = 255 / (np.log2(256))

        # compute output = constant * log(input + 1)
        # 1 is added to input to avoid log(0)
        output = np.int8(normalization_const *
                         np.log2(image + np.ones((image_row, image_column))))

        #  return the computed image
        return output

    # compute blurred image for the image passed as ndarray based on
    # window size passed
    def blur(self, image, window_size):
        # define blur window as square matrix of all 1s with
        # matrix size = window size passed
        window = np.ones((window_size, window_size), dtype=np.uint8)
        # perform convolution of image and window
        output = self.convolution(image, window)
        #  return the computed image
        return output

    # compute sharpened image for the image passed as ndarray based on
    # sharpen constant passed
    def sharp(self, image, sharp_const):
        # define window as standard 3x3 Laplacian
        window = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
        # compute output as image - constant * correlation of image and window
        output = image - sharp_const * self.correlation(image, window)

        # keep output pixels in range 0 to 255
        # replace pixels with value < 0 in output with 0
        output[output < 0] = 0
        # replace pixels with value > 255 in output with 255
        output[output > 255] = 255

        #  return the computed image
        return output

    # compute edges of the image passed as ndarray
    def edge_detection(self, image):
        # define window as standard 3x3 Laplacian
        window = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
        # perform correlation of image and window
        output = self.correlation(image, window)

        # keep output pixels in range 0 to 255
        # replace pixels with value < 0 in output with 0
        output[output < 0] = 0
        # replace pixels with value > 255 in output with 255
        output[output > 255] = 255

        #  return the computed image
        return output

    # compute convolution operation on image and window passed as ndarray
    # also normalizes output values by dividing with sum of window elements
    def convolution(self, image, window):
        # to perform convolution, flip the window and compute correlation
        window = np.flipud(np.fliplr(window))
        output = self.correlation(image, window)
        # divide the output with sum of window elements
        output = np.uint8(output / window.sum())
        #  return the computed image
        return output

    # compute correlation operation on image and window passed as ndarray
    # does not normalize output values by dividing with sum of window elements
    def correlation(self, image, window):
        output = np.zeros_like(image)
        # find no of rows and columns in the ndarray of image passed
        image_row = image.shape[0]
        image_column = image.shape[1]

        # compute window size from window passed
        window_size = window.shape[0]
        # compute zero padding requirements and offset to be used during convolution
        zero_padding = window_size - 1
        offset = int(zero_padding / 2)

        # create the zero padded image
        image_zero_padded = \
            np.zeros((image_row + zero_padding, image_column + zero_padding))
        image_zero_padded[offset:(-1 * offset), offset:(-1 * offset)] = image

        # loop through the window elements
        # computes correlation as shifted sum of image elements by keeping
        # window stationary
        for r in range(window_size):
            for c in range(window_size):
                output = output + window[r][c] * \
                         image_zero_padded[r:r + image_row, c:c + image_column]

        #  return the computed image
        return output
