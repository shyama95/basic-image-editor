# Basic Image Editor application
## Abstract
The Basic Image Editor application implements few basic image processing operations in python. The application provides an easy to use GUI built on PyQt4 to perform these operations on grayscale and colour images, and is completely implemented in Python. The operations performed on color images were limited to the V channel in HSV format. 

The operations implemented are:
* Histogram computation
* Histogram equalization
* Gamma correction
* Log transform
* Image negative
* Blurring
* Sharpening
* Basic edge detection

## Dependencies
- python v3
- PyQt4
- python libraries : opencv (to read/ save images), numpy, matplotlib
## Instructions to run
~~~~
python3 main.py
~~~~
## Results
A screenshot of the application is given below.

![Basic Image EditorApplication Screenshot](https://github.com/shyama95/basic-image-editor/blob/master/application-screenshot.png)

A demo video of the application is available [here](https://drive.google.com/open?id=18prC7elV6siC_4wt78Md9Lqut46Hag8H).  
The complete report of the application is available [here](https://drive.google.com/open?id=1GwmJGeYGsuuTCjbiXZjWqqPP8mIHalDf).  
## References
[1] Gonzalez, Rafael C., and Woods, Richard E. "Digital image processing. 3E" (2008).  
[2] https://elementztechblog.wordpress.com/2015/04/14/getting-started-with-pycharm-and-qt-4-designer/  
[3] http://machinelearninguru.com/computer_vision/basics/convolution/image_convolution_1.html  
[4] https://docs.scipy.org/doc/numpy/reference/  
