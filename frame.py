import glob
import os
import shutil
import subprocess
from PIL import Image

path = '/home/vvanhee/Pictures'
croppath = path + "/tmp"
frameWidth=480
frameHeight=264

def faceDetect(filename):
    unsplitfaces=[]
    result = subprocess.check_output("facedetect " + filename, shell=True)
    unsplitfaces=result.decode().rstrip('\n').split(sep="\n")
    faces=[]
    for face in unsplitfaces:
        face=face.split()
        faces.append(face)
    if faces==[[]]:
        faces=""
    return faces #X Y width height

def faceDetectBestYCenter(filename):
    result = subprocess.check_output("facedetect --biggest --center " + filename, stderr=subprocess.STDOUT, shell=True)
    result=result.decode().rstrip('\n').split()
    return int(result[1])

def avgYForFaces(faces):
    faceYCenters=[]
    for face in faces:
        faceYCenters.append(int(face[1])+int(face[3])/2)
    return sum(faceYCenters)/len(faceYCenters)

def maxYDifference(faces):
    topsAndBottoms = []
    for face in faces:
        topsAndBottoms.append(int(face[1]))
        topsAndBottoms.append(int(face[1])+int(face[3]))
    return max(topsAndBottoms)-min(topsAndBottoms)    

def getGravAndOffset(fraction, scaledHeight):
    offset="+0+0"
    gravity="center"
    if fraction < 0.2 and fraction >-0.5:
        gravity="north"
    elif fraction < 0.4:
        gravity="north"
        yOffset=0.1*scaledHeight
        offset="+0+" + str(int(yOffset))
    elif fraction < 0.6:
        offset="+0+0"
        gravity="center"        #no change
    elif fraction < 0.8:
        gravity="south"
        yOffset=0.1*scaledHeight
        offset="+0+" + str(int(yOffset))
    elif fraction <=1.0:
        gravity="south"
        # do nothing
    return [gravity,offset]

if os.path.isdir(croppath):
    shutil.rmtree(croppath)
os.mkdir(croppath)

for fname in glob.glob(path+"/*.png"):
    name=os.path.basename(fname)
    os.system('convert ' + fname + ' ' + path + '/' + name + ".jpg")

for fname in glob.glob(path+"/*.jpg"):
    name=os.path.basename(fname)
    cropfname=croppath+"/"+name
    subprocess.check_call('convert ' + fname + ' -auto-orient ' + cropfname, shell=True)
    gravity="center"
    offset="+0+0"
    faces = faceDetect(cropfname)
    numFaces=len(faces)
    print("Detected " + str(numFaces) + " face(s) in " + name + ". Cropping...")
    im=Image.open(cropfname)
    heightPic=im.size[1]
    widthPic=im.size[0]
    scaledHeight=heightPic/widthPic*frameWidth
    yCenter=-1.0
    if numFaces>1:
        maxYDiff=maxYDifference(faces)
        scaledYDiff=maxYDiff*scaledHeight/heightPic
        if scaledYDiff>frameHeight*1.1: # then facedetect largest face
            yCenter=faceDetectBestYCenter(cropfname)
        else: #take the average Y for centers of faces
            yCenter=avgYForFaces(faces)
    if numFaces==1:
        yCenter=faceDetectBestYCenter(cropfname)
    if numFaces>=1:
        fraction = yCenter/heightPic
        gravAndOffset=getGravAndOffset(fraction, scaledHeight)
        gravity=gravAndOffset[0]
        offset=gravAndOffset[1]
    #print(gravity+offset)
    os.system('mogrify ' + fname + ' -gravity ' + gravity + ' -resize ' + str(frameWidth) + ' -crop ' + str(frameWidth) + 'x' + str(frameHeight) + offset + ' +repage ' + cropfname)

import time
timestr = time.strftime("%Y-%m-%d-%H-%M-%S")
shutil.move(croppath,path+"/crops-"+timestr)


