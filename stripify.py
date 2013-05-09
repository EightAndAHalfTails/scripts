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
rowcount = 200

def average(frame):
    f = open(frame, 'rb')
    f.read(36)

    reds = 0
    greens = 0
    blues = 0

    finished = False
    while not finished:
        red = f.read(1)
        green = f.read(1)
        blue = f.read(1)
        if not (red and green and blue):
            break 

        reds += int(red[0])
        greens += int(green[0])
        blues += int(blue[0])

    mean_red = math.floor(reds / (640 * 360))
    mean_green = math.floor(greens / (640 * 360))
    mean_blue = math.floor(blues / (640 * 360))
    
    #print(mean_red, mean_green, mean_blue)
    #print("{0:x}{1:x}{2:x}".format(mean_red,mean_green,mean_blue))
    f.close()
    return (mean_red, mean_green, mean_blue)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='stripify 0.1')
    #print(arguments)
    
    tmpdir = mkdtemp()
    frames = os.path.join(tmpdir, "%05d.bmp")
    subprocess.call("ffmpeg -i {} -r 1/10 -s 640x360 {}".format(arguments['<input>'], frames), shell=True)
    
    #subs = os.path.join(tmpdir, "subs.ass")
    #mp4 = os.path.join(tmpdir, "tmp.mp4")

    stripes = []
    ls = os.listdir(tmpdir)
    ls.sort()
    for frame in ls:
        #print(frame)
        print("{}: Analysing {}".format(strftime('%H:%M:%S'), frame))
        frame = os.path.join(tmpdir, frame)
        stripes.append(average(frame))

    out = open("stripes.bmp", 'wb')
    out.write(b'\x42\x4d') #BM marks start of bitmap image
    out.write(struct.pack('<i', len(stripes)*stripe_width*rowcount + 36)) #size of file
    out.write(b'\x00\x00\x00\x00') #reserved
    out.write(b'\x36\x00\x00\x00') #image offset
    out.write(b'\x28\x00\x00\x00') #header size (40)
    out.write(struct.pack('<i', len(stripes) * stripe_width)) #width
    out.write(struct.pack('<i', rowcount)) #height
    out.write(b'\x01\x00\x18\x00\x00\x00\x00\x00')
    out.write(struct.pack('<i', len(stripes) * 3)) #image size
    out.write(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    for row in range(rowcount):
        for stripe in stripes:
            for i in range(stripe_width):
                out.write(struct.pack('<B', stripe[0]))
                out.write(struct.pack('<B', stripe[1]))
                out.write(struct.pack('<B', stripe[2]))
    
    out.close()
    rmtree(tmpdir)
