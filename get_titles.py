#!/usr/bin/env python3

"""
Consolidates episode titles into a text file

Usage:
  get_titles.py [options]
  get_titles.py (-h | --help)
  get_titles.py --version

Options:
  -h --help            Show this screen.
  -n                   Dry run: show steps, but do not move anything. Implies -v
  -v                   Verbose: show steps.
  -f <file>            Specify titles file
  --version            Show version.

"""
import os
import subprocess
from docopt import docopt
from move_with_dest_names import *

if __name__ == '__main__':
    arguments = docopt(__doc__, version='get_titles 0.1')
    titles_file = arguments['-f'] if arguments['-f'] else 'titles.txt'

    # get list of unprocessed filenames 
    files = os.listdir('.')

    # sort them into the correct order
    #files = episodeOrder(files)
    files.sort()

    with open(titles_file, 'w') as titles:
        for name in files:
            title = name.partition(':')[2].strip()
            titles.write(title + '\n')
