#!/usr/bin/env python3

"""Turns symlinks into hard links

Usage:
  harden_links.py [options] <input>...
  harden_links.py (-h | --help)
  harden_links.py --version

Options:
  -r                   Operate on directories recursively.
  -h --help            Show this screen.
  --version            Show version.

"""

import os
from docopt import docopt 


class Link:
    def __init__(self, name, dest):
        self.name = name
        self.dest = dest
    name = ""
    dest = ""

def harden_dir(directory, recursive):
    if recursive and os.path.isdir(directory):
        harden_files([ os.path.join(directory, filename) for filename in os.listdir(directory) ], recursive)

def harden_files(filenames, recursive):
    for filename in filenames:
        if os.path.isdir(filename):
            harden_dir(filename, recursive)
        else:
            harden(filename)

def harden(filename):
    #print("Checking " + filename)
    if not os.path.islink(filename):
        return 1
    print("Hardening " + filename)
    link = Link(os.path.basename(filename), os.readlink(filename))
    #os.remove(filename)
    #os.link(link.dest, link.name)
    print(link.dest, link.name)
    return 0

def main():
    arguments = docopt(__doc__, version='harden_links 0.1')
    #print(arguments)

    inputs = arguments['<input>']

    for root, dirs, files in os.walk('.'):
        for f in files:
            path = os.path.join(root, f)
            if os.path.islink(path):
                dest = os.path.join(root, os.readlink(path))
                while os.path.islink(dest):
                    dest = os.path.join(os.path.dirname(dest), os.readlink(dest))
                print(path + " -> " + dest)
                #remove old symlink
                os.remove(path)
                #make hardlink
                os.link(dest, path)

if __name__ == '__main__':
    main()
