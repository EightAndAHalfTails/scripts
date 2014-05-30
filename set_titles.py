#!/usr/bin/env python3

"""
Names all files in the current directory according to the following format:
The name of the containing folder
the episode number, taken by its position when the files are ordered alphabetically
the episode titles, taken from a newline-delimited text file in the directory

Usage:
  set_titles.py [options]
  set_titles.py (-h | --help)
  set_titles.py --version

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

def pad(number, places=2):
    return str(number).zfill(places)

def listEmptyStrings(n):
    l = []
    for i in range(n):
        l.append('')
    return l

def name_anime(files, titles=None):
    # get name of current directory
    anime_title = os.path.basename(os.getcwd())

    episode_numbers = map(pad, range(1, len(files)+1))

    if not titles:
        titles = listEmptyStrings(len(files))
    for old_file, no, title in zip(files, episode_numbers, titles):
        title = title.strip('\n')
        if title:
            new_file = "{} - {}: {}".format(anime_title, no, title)
        else:
            new_file = "{} - {}".format(anime_title, no)
        if verbose:
            print("{} -> {}".format(old_file, new_file))
        if not (old_file == new_file) and not dry_run:
            move(old_file, new_file)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='set_titles 0.1')
    verbose = True if arguments["-v"] or arguments["-n"] else False
    dry_run = True if arguments["-n"] else False
    if arguments['-f']:
        titles_file = arguments['-f']
    elif os.path.exists('titles.txt'):
        titles_file = 'titles.txt'
    else:
        titles_file = None

    # get list of unprocessed files 
    files = os.listdir('.')

    # sort them into the correct order
    #files = episodeOrder(files)
    files.sort()

    if titles_file:
        try:
            files.remove(titles_file)
            with open(titles_file) as titles:
                print("Naming according to {}".format(titles_file))
                name_anime(files, titles)
#            if not dry_run:
#                os.remove(titles_file)
        except (ValueError, IOError):
            print("file {} does not exist".format(titles_file))
            exit(1)
    else:
        name_anime(files)
