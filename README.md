# frame-resize
Resize your photos for a digital frame -- detect and center faces.

This python script uses facedetect and imagemagick to resize images, centering on faces if they can be detected by facedetect. If all the faces don't fit in the frame, the script resizes so that the largest face is centered.

## Steps to install and run
1. Make sure imagemagick is installed.
1. Install python PIL (`sudo apt-get install python-imaging` in Ubuntu 16.04). 
1. Install facedetect using the instructions at https://www.thregr.org/~wavexx/software/facedetect/.
1. Change the `height` and `width` at the top of the python file to the max height and width of your digital frame.
1. Place your photos in their own directory. 
1. Change the name of the directory in the `path` variable at the top of the python file to the full name of the directory you placed the photos in.  
1. Run the python file (works in Python 3)
1. Cropped images will be placed in a subdirectory of your path called `crop-datetime`. Upload/transfer these to your frame, and you're done!
