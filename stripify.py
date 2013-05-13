#!/usr/bin/env python3

"""Represent an mkv file with mean-coloured stripes

Usage:
  stripify.py <input>
  stripify.py (-h | --help)
  stripify.py --version

Options:
  -h --help            Show this screen.
  --version            Show version.

"""
from docopt import docopt
import os
import subprocess
import math
from shlex import quote
from tempfile import mkdtemp
from shutil import rmtree
import struct
from time import strftime

stripe_width = 4
image_height = 200

def readBitmapHeader(f):
"""Reads a bitmap header file. Increments the file pointer past the header and returns the width and height of the image"""
    # TODO: find out actual header size dynamically
    if(f.read(2) is not b'\x42\x4d'):
        raise Exception("corrupt bitmap image")
    f.read(4) # the size of the BMP file in bytes
    f.read(2) # reserved
    f.read(2) # reserved
    f.read(4) # the offset, i.e. starting address, of the byte where the bitmap image data (pixel array) can be found.
    f.read(4) # the size of this header (40 bytes)
    width = f.read(4) # the bitmap width in pixels (signed integer)
    height = f.read(4) # the bitmap height in pixels (signed integer)
    f.read(2) # the number of color planes being used. Must be set to 1.
    f.read(4) # the compression method being used.
    f.read(4) # the image size. This is the size of the raw bitmap data, and should not be confused with the file size.
    f.read(4) # the horizontal resolution of the image. (pixel per meter, signed integer)
    f.read(4) # the verticalal resolution of the image. (pixel per meter, signed integer)
    f.read(4) # the number of colors in the color palette, or 0 to default to 2^n
    f.read(4) # the number of important colors used, or 0 when every color is important; generally ignored
    return (struct.unpack('<i', width), struct.unpack('<i', height))

def average(frame, resolution="640x360"):
    f = open(frame, 'rb')
    (width, height) = readBitmapHeader(f)

    reds = 0
    greens = 0
    blues = 0

    while True:
        red = f.read(1)
        green = f.read(1)
        blue = f.read(1)
        if not (red and green and blue):
            break 

        reds += int(red[0])
        greens += int(green[0])
        blues += int(blue[0])

    mean_red = math.floor(reds / (width * height))
    mean_green = math.floor(greens / (width * height))
    mean_blue = math.floor(blues / (width * height))
    f.close()
    return (mean_red, mean_green, mean_blue)
    
def extractFrames(video_file, frame_rate="1/10", resolution="640x360"):
"""Extracts frames from a video file, stores them in a temp directory, and returns a path to that directory"""
    tmpdir = mkdtemp()
    frames = os.path.join(tmpdir, "%05d.bmp")
    subprocess.call("ffmpeg -i {} -r {} -s {} {}".format(video_file, frame_rate, resolution, frames), shell=True)
    return tmpdir

def analyseFrames(frame_dir):
    stripes = []
    ls = os.listdir(frame_dir)
    ls.sort()
    for frame in ls:
        print("{}: Analysing {}".format(strftime('%H:%M:%S'), frame))
        frame = os.path.join(frame_dir, frame)
        stripes.append(average(frame))
    return stripes

def drawStripes(stripes, output_filename="stripes.bmp"):
    out = open(output_filename, 'wb')
    out.write(b'\x42\x4d') #BM marks start of bitmap image
    out.write(struct.pack('<i', len(stripes)*stripe_width*image_height + 36)) #size of file
    out.write(b'\x00\x00\x00\x00') #reserved
    out.write(b'\x36\x00\x00\x00') #image offset
    out.write(b'\x28\x00\x00\x00') #header size (40)
    out.write(struct.pack('<i', len(stripes) * stripe_width)) #width
    out.write(struct.pack('<i', image_height)) #height
    out.write(b'\x01\x00\x18\x00\x00\x00\x00\x00')
    out.write(struct.pack('<i', len(stripes) * 3)) #image size
    out.write(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    for row in range(image_height):
        for stripe in stripes:
            for i in range(stripe_width):
                out.write(struct.pack('<B', stripe[0]))
                out.write(struct.pack('<B', stripe[1]))
                out.write(struct.pack('<B', stripe[2]))
    
    out.close()
    

if __name__ == '__main__':
    arguments = docopt(__doc__, version='stripify 0.1')

    frame_dir = extractFrames(arguments['<input>'])
    stripes = analyseFrames(frame_dir)
    drawImage(stripes, arguments['<input>'] + "_out.bmp")
    rmtree(frame_dir)
