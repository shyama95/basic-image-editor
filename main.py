# ---------------------------------------------------------------#
# __name__ = "BasicImageEditor_EE610_Assignment"
# __author__ = "Shyama P"
# __version__ = "1.0"
# __email__ = "183079031@iitb.ac.in"
# __status__ = "Development"
# ---------------------------------------------------------------#

# main.py contains the code for initializing and running the code for GUI
import sys
# PyQt4 libraries are used for GUI
from PyQt4.QtGui import *
from PyQt4.QtCore import *
# OpenCV2 library is used for reading/ writing of images and color space
# conversion only
import cv2
# All array operations are performed using numpy library
import numpy as np
# Matplotlib library is used for histogram plots
import  matplotlib.pyplot as plt

# The GUI structure definition is provided in gui.py
from gui import *
# Image processing logic is defined in imageProcessingFns.py
import imageProcessingFns as ip

# class ImageEditorClass implements the GUI main window class
class ImageEditorClass(QMainWindow):

    # stores a copy of original image for use in Undo All functionality
    originalImage = [0]
    # stores the current image being displayed/ processed
    currentImage = [0]
    # stores the previous image for use in Undo operation
    previousImage = [0]

    # stores a copy of image being blurred
    imageBlur = [0]
    # stores a copy of image being sharpened
    imageSharpen = [0]

    # stores current image height and width
    imageWidth = 0
    imageHeight = 0

    # initializes an object of ImageProcessorClass from imageProcessingFns.py
    imageLib = ip.ImageProcessorClass()

    # stores code of current operation
    currentOperationCode = -1

    # ------------------------------#
    # Histogram Equalization => 0   #
    # Gamma Correction => 1         #
    # Log Transform => 2            #
    # Negative => 3                 #
    # Blur => 4                     #
    # Sharpen => 5                  #
    # Edge detection => 6           #
    # ------------------------------#

    # GUI initialization
    def __init__(self, parent=None):
        super(ImageEditorClass, self).__init__()
        QWidget.__init__(self, parent)
        self.ui = ImageEditorGuiClass()
        self.ui.setupUi(self)

        # Assigning functions to be called on all button clicked events and
        # slider value changed events
        self.ui.openImageButton.clicked.connect(lambda: self.open_image())
        self.ui.saveImageButton.clicked.connect(lambda: self.save_image())

        self.ui.histogramEqualizationButton.clicked.connect\
            (lambda: self.histogram_equalization())
        self.ui.logTransformButton.clicked.connect(lambda: self.log_transform())
        self.ui.gammaCorrectionButton.clicked.connect(lambda: self.gamma_correction())
        self.ui.negativeButton.clicked.connect(lambda: self.image_negative())

        self.ui.blurExtendInputSlider.valueChanged.connect(lambda: self.blur())
        self.ui.sharpenExtendInputSlider.valueChanged.connect(lambda: self.sharpen())

        self.ui.undoButton.clicked.connect(lambda: self.undo())
        self.ui.undoAllButton.clicked.connect(lambda: self.undoAll())

        self.ui.viewHistogramButton.clicked.connect(lambda: self.view_histogram())
        self.ui.detectEdgeButton.clicked.connect(lambda: self.edge_detection())

        # initiaize and input dialog box gui for input of gamma value
        self.newDialog = InputDialogGuiClass(self)

    # called when Open button is clicked
    def open_image(self):
        # set_default_slider function resets blur and sharpen sliders to initial
        # position
        self.set_default_slider()

        # open a new Open Image dialog box and capture path of file selected
        open_image_window = QFileDialog()
        image_path = QFileDialog.getOpenFileName\
            (open_image_window, 'Open Image', '/')

        # check if image path is not null or empty
        if image_path:
            # initialize class variables
            self.currentImage = [0]
            self.currentOperationCode = -1

            # read image at selected path to a numpy ndarray object as color image
            self.currentImage = cv2.imread(image_path, 1)
            # convert the image read to HSV format from default BGR format
            self.currentImage = cv2.cvtColor(self.currentImage, cv2.COLOR_BGR2HSV)

            # set image specific class variables based on current image
            self.imageWidth = self.currentImage.shape[1]
            self.imageHeight = self.currentImage.shape[0]

            self.originalImage = self.currentImage.copy()
            self.previousImage = self.currentImage.copy()

            # displayImage converts current image from ndarry format to
            # pixmap and assigns it to image display label
            self.displayImage()
            # enable_options enable all buttons and sliders in the window.
            # Only Open button is enabled on start
            self.enable_options()

    # called when Save button is clicked
    def save_image(self):
        # configure the save image dialog box to use .jpg extension for image if
        # not provided in file name
        dialog = QFileDialog()
        dialog.setDefaultSuffix('jpg')
        dialog.setAcceptMode(QFileDialog.AcceptSave)

        # open the save dialog box and wait until user clicks 'Save'
        # button in the dialog box
        if dialog.exec_() == QDialog.Accepted:
            # select the first path in the selected files list as image save
            # location
            save_image_filename = dialog.selectedFiles()[0]
            # write current image to the file path selected by user
            cv2.imwrite(save_image_filename,
                        cv2.cvtColor(self.currentImage, cv2.COLOR_HSV2BGR))

    # called when Histogram Equalization button is clicked
    def histogram_equalization(self):
        # updatePreviousImage function updates the previous image class variable
        #  with current image
        self.updatePreviousImage()
        # update current operation code class variable
        self.currentOperationCode = 0
        # set_default_slider function resets blur and sharpen sliders to initial
        #  position
        self.set_default_slider()

        # update V channel of the current image with histogram equallized matrix
        self.currentImage[:, :, 2] = self.imageLib.histogram_equalization\
            (self.currentImage[:, :, 2])
        # displayImage converts current image from ndarry format to pixmap
        # and assigns it to image display label
        self.displayImage()

    def gamma_correction(self):
        # updatePreviousImage function updates the previous image class
        # variable with current image
        self.updatePreviousImage()
        # update current operation code class variable
        self.currentOperationCode = 1
        # set_default_slider function resets blur and sharpen sliders to
        # initial position
        self.set_default_slider()

        # open gamma input dialog box and wait for dialog box to exit
        if self.newDialog.exec() == 0:
            # read gamma value from gamma input dialog box class
            gamma_value = self.newDialog.gamma
            # reset the value of gamma in gamma input dialog box to 1
            self.newDialog.gammaInput.setText('1.00')
            self.newDialog.gamma = 1.0
            # perform gamma correction for positive gamma values
            # gamma range is restricted to 0 to 10 in the gamma input
            # dialog box
            if gamma_value > 0:
                # update V channel of the current image with gamma corrected
                # matrix
                self.currentImage[:, :, 2] = self.imageLib.gamma_correction\
                    (self.currentImage[:, :, 2], gamma_value)

        # displayImage converts current image from ndarry format to pixmap
        # and assigns it to image display label
        self.displayImage()

    def log_transform(self):
        # updatePreviousImage function updates the previous image class
        # variable with current image
        self.updatePreviousImage()
        # update current operation code class variable
        self.currentOperationCode = 2
        # set_default_slider function resets blur and sharpen sliders to
        # initial position
        self.set_default_slider()

        # update V channel of the current image with log transformed matrix
        self.currentImage[:, :, 2] = \
            self.imageLib.log_transform(self.currentImage[:, :, 2])

        # displayImage converts current image from ndarry format to
        # pixmap and assigns it to image display label
        self.displayImage()

    def image_negative(self):
        # updatePreviousImage function updates the previous image class
        # variable with current image
        self.updatePreviousImage()
        # update current operation code class variable
        self.currentOperationCode = 3
        # set_default_slider function resets blur and sharpen sliders to
        # initial position
        self.set_default_slider()

        # update current image with negative of current image
        self.currentImage = self.imageLib.image_negative(self.currentImage)

        # displayImage converts current image from ndarry format to pixmap
        # and assigns it to image display label
        self.displayImage()

    def blur(self):
        # updatePreviousImage function updates the previous image class
        # variable with current image
        self.updatePreviousImage()

        # disconnect, initialize and reconnect the sharpen slider value
        # changed event
        # this is to avoid calling of sharpen function when sharpen slider
        # value is reset
        self.ui.sharpenExtendInputSlider.valueChanged.disconnect()
        self.ui.sharpenExtendInputSlider.setValue(0)
        self.ui.sharpenExtendInputSlider.valueChanged.connect(lambda:
                                                              self.sharpen())
        self.ui.sharpenValueLabel.setText('0')

        # read current blur value from slider and compute blur window size as
        # (2 * slider value + 1)
        blur_value = int(np.floor(self.ui.blurExtendInputSlider.value()))
        blur_window_size = (blur_value * 2) + 1

        # if the operation being performed currently is blur, use initial image
        # passed to blur function
        # else set current image as initial image for blur
        if self.currentOperationCode == 4:
            self.currentImage = self.imageBlur.copy()
        else:
            self.imageBlur = self.currentImage.copy()

        if blur_value > 0:
            # enable undo button
            self.ui.undoButton.setEnabled(True)
            # update V channel of the current image with blurred V matrix
            self.currentImage[:, :, 2] = \
                self.imageLib.blur(self.currentImage[:, :, 2], blur_window_size)

        # update current operation code class variable
        self.currentOperationCode = 4

        self.ui.blurValueLabel.setText(str(blur_value))
        # displayImage converts current image from ndarry format to pixmap and
        # assigns it to image display label
        self.displayImage()

    def sharpen(self):
        # updatePreviousImage function updates the previous image class variable
        # with current image
        self.updatePreviousImage()

        # disconnect, initialize and reconnect the blur slider value changed event
        # this is to avoid calling of blur function when blur slider value is reset
        self.ui.blurExtendInputSlider.valueChanged.disconnect()
        self.ui.blurExtendInputSlider.setValue(0)
        self.ui.blurExtendInputSlider.valueChanged.\
            connect(lambda: self.blur())
        self.ui.blurValueLabel.setText('0')

        # read current sharpen value from slider and compute
        # sharpen constant as (slider value/10)
        sharpen_value = self.ui.sharpenExtendInputSlider.value()
        sharpen_const = sharpen_value / 10.0

        # if the operation being performed currently is sharpen, use
        # initial image passed to sharpen function
        # else set current image as initial image for sharpen
        if self.currentOperationCode == 5:
            self.currentImage = self.imageSharpen.copy()
        else:
            self.imageSharpen = self.currentImage.copy()

        if sharpen_const > 0:
            # enable undo button
            self.ui.undoButton.setEnabled(True)
            # update V channel of the current image with sharpened V
            # channel matrix
            self.currentImage[:, :, 2] = \
                np.uint8(self.imageLib.sharp(self.currentImage[:, :, 2], sharpen_const))

        # update current operation code class variable
        self.currentOperationCode = 5

        self.ui.sharpenValueLabel.setText(str(sharpen_value))
        # displayImage converts current image from ndarry format to
        # pixmap and assigns it to image display label
        self.displayImage()

    def undo(self):
        self.ui.undoButton.setEnabled(False)
        self.currentImage = self.previousImage.copy()
        # displayImage converts current image from ndarry format to pixmap and
        # assigns it to image display label
        self.displayImage()

    def undoAll(self):
        # set_default_slider function resets blur and sharpen sliders to initial
        # position
        self.set_default_slider()
        self.currentImage = self.originalImage.copy()
        # displayImage converts current image from ndarry format to pixmap and
        # assigns it to image display label
        self.displayImage()
        self.ui.undoButton.setEnabled(False)

    def view_histogram(self):
        # count the no of values corresponding to each value in the V channel of
        # image matrix give a minimum length of 256 to the counting to ensure all 256 pixel
        # values are covered or pixel values not available in image are set to zero
        histogram = np.bincount(self.currentImage[:, :, 2].ravel(), minlength=256)
        # start a new figure to show histogram - assign title and axes label
        plt.figure(num='Image Histogram')
        # assign a discrete plot of histogram to figure
        plt.stem(histogram)
        plt.xlabel('Intensity levels')
        plt.ylabel('No. of pixels')
        # show the stem plot
        plt.show()

    def edge_detection(self):
        # updatePreviousImage function updates the previous image class variable with
        # current image
        self.updatePreviousImage()
        # update current operation code class variable
        self.currentOperationCode = 6
        # set_default_slider function resets blur and sharpen sliders to initial
        # position
        self.set_default_slider()

        # update V channel of the current image with edge detected V channel matrix
        self.currentImage[:, :, 2] \
            = self.imageLib.edge_detection(self.currentImage[:, :, 2])

        # displayImage converts current image from ndarry format to
        # pixmap and assigns it to image display label
        self.displayImage()

    # displayImage converts current image from ndarry format to pixmap and
    # assigns it to image display label
    def displayImage(self):
        # set display size to size of the image display label
        display_size = self.ui.imageDisplayLabel.size()
        # copy current image to temporary variable for processing pixmap
        image = np.array(self.currentImage.copy())
        zero = np.array([0])

        # display image if image is not [0] array
        if not np.array_equal(image, zero):
            # convert HSV image to RGB format for display in label
            image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)
            # ndarray cannot be directly converted to QPixmap format required
            # by image display label
            # so ndarray is first converted to QImage and then QImage to QPixmap
            # convert image ndarray to QImage format
            qImage = QImage(image, self.imageWidth, self.imageHeight,
                            self.imageWidth * 3, QImage.Format_RGB888)

            # convert QImage to QPixmap for loading in image display label
            pixmap = QPixmap()
            QPixmap.convertFromImage(pixmap, qImage)
            pixmap = pixmap.scaled(display_size, Qt.KeepAspectRatio,
                                   Qt.SmoothTransformation)
            # set pixmap to image display label in GUI
            self.ui.imageDisplayLabel.setPixmap(pixmap)

    # enable_options enable all buttons and sliders in the window. Only
    # Open button is enabled on start
    # Undo button remains disabled until an operation is performed
    def enable_options(self):
        self.ui.histogramEqualizationButton.setEnabled(True)
        self.ui.gammaCorrectionButton.setEnabled(True)
        self.ui.logTransformButton.setEnabled(True)
        self.ui.negativeButton.setEnabled(True)

        self.ui.blurExtendInputSlider.setEnabled(True)
        self.ui.sharpenExtendInputSlider.setEnabled(True)

        self.ui.saveImageButton.setEnabled(True)
        self.ui.undoAllButton.setEnabled(True)
        self.ui.undoButton.setEnabled(False)

        self.ui.viewHistogramButton.setEnabled(True)
        self.ui.detectEdgeButton.setEnabled(True)

    # set_default_slider function resets blur and sharpen sliders to initial
    # position
    def set_default_slider(self):
        # disconnect the value changed event of sliders from the functions
        # assigned this prevents calling the blur and sharpen function on
        # resetting of sliders
        self.ui.sharpenExtendInputSlider.valueChanged.disconnect()
        self.ui.blurExtendInputSlider.valueChanged.disconnect()

        # update slider values to initial position i.e. 0
        # update slider value labels to 0
        self.ui.blurExtendInputSlider.setValue(0)
        self.ui.blurValueLabel.setText('0')
        self.ui.sharpenExtendInputSlider.setValue(0)
        self.ui.sharpenValueLabel.setText('0')

        # reconnect the value changed event of sliders to blur and sharpen
        # functions
        self.ui.blurExtendInputSlider.valueChanged.connect(lambda: self.blur())
        self.ui.sharpenExtendInputSlider.valueChanged.connect(
            lambda: self.sharpen())

        # reset values of blur and sharpen image class variables
        self.imageBlur = [0]
        self.imageSharpen = [0]

        # enable Undo button only if an operation was performed previosly
        # i.e. current operation code is a valid code
        if (self.currentOperationCode >= 0) and \
                not self.ui.undoButton.isEnabled():
            self.ui.undoButton.setEnabled(True)

    # updatePreviousImage function updates the previous image class variable
    # with current image
    def updatePreviousImage(self):
        self.previousImage = self.currentImage.copy()

# initialize the ImageEditorClass and run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = ImageEditorClass()
    myapp.showMaximized()
    sys.exit(app.exec_())

