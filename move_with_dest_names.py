#!/usr/bin/env python3

"""Move all contents from one directory to another, keeping the destination names. the two directories must have an equal number of files

Usage:
  stripify.py [options] <source> <destination>
  stripify.py (-h | --help)
  stripify.py --version

Options:
  -h --help            Show this screen.
  -n                   Dry run: show steps, but do not move anything. Implies -v
  -v                   Verbose: show steps.
  --version            Show version.

"""
import os
import subprocess
from docopt import docopt

def move(source, dest):
    subprocess.call("mv \"{}\" \"{}\"".format(source, dest), shell=True)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='stripify 0.1')
    verbose = True if arguments["-v"] or arguments["-n"] else False

    dry_run = True if arguments["-n"] else False

    sourcedir = arguments["<source>"]
    destdir = arguments["<destination>"]

    source_files = os.listdir(sourcedir)
    source_files.sort()

    dest_files = os.listdir(destdir)
    dest_files.sort()

    if len(source_files) is not len(dest_files):
        raise Exception("directories are not equal")

    for i in range(len(source_files)):
        source = os.path.join(sourcedir, source_files[i])
        dest = os.path.join(destdir, dest_files[i])
        if verbose:
            print("{} -> {}".format(source, dest))
        if not dry_run:
            move(source, dest)
