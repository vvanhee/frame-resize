# frame-resize
Resize your photos for a digital frame -- detect and center faces.

This python script uses facedetect and imagemagick to resize images, centering on faces if they can be detected by facedetect. If all the faces don't fit in the frame, the script resizes so that the largest face is centered.

## Steps to install and run
1. Make sure imagemagick is installed.
2. Install python PIL (`sudo apt-get install python-imaging` in Ubuntu 16.04). 
3. Install facedetect using the instructions at https://www.thregr.org/~wavexx/software/facedetect/.
4. Change the `height` and `width` at the top of the python file to the max height and width of your digital frame.
5. Place your photos in their own directory. 
6. Change the name of the directory in the `path` variable at the top of the python file to the full name of the directory you placed the photos in.  
7. Run the python file (works in Python 3)
