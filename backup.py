#!/usr/bin/env python3

"""Back up my data and anime drives to the external HDD mounted at /media/external

Usage:
  backup.py [options]
  backup.py (-h | --help)
  backup.py --version

Options:
  -h --help            Show this screen.
  -d --delete          Delete files which no longer exist on the source
  -n --dry-run         Don't move or delete files, just show what will be moved or deleted. Implies -v
  -v --verbose         Show what steps will be taken.
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

def backup(source, target):
    delete = '-d' if arguments['--delete'] else ''
    dry_run = '-n' if arguments['--dry-run'] else ''
    verbose = '-v' if arguments['--verbose'] or dry_run else ''
    bak_file = os.path.join(target, '.log', strftime('%Y-%m-%d.backup.txt'))
    dif_file = os.path.join(target, '.log', strftime('%Y-%m-%d.delete.txt'))
    bak_command = "rsync -Pah {} {} --log-file={} {} {}".format(
        '-i' if verbose else '',
        '-n' if dry_run else '',
        bak_file,
        source,
        target)
    subprocess.call(bak_command, shell=True)
    #print(bak_command)

    if delete:
        dif_command = "rsync -Pah {} {} --delete {} {} | grep deleting >> {}".format(
            '-i' if verbose else '',
            '-n' if dry_run else '',
            source,
            target,
            dif_file)
        subprocess.call(dif_command, shell=True)
        #print(dif_command)    

def rename_all(target):
    for base, dirs, files in os.walk(target):
        for f in files:
            rename(f)
        for d in dirs:
            rename(d)

def rename(target):
    if ':' in target or '?' in target:
        newname = target.replace(':', ' -')
        newname = newname.replace('?', '_')
        path = os.path.join(base, target)
        newpath = os.path.join(base, target)
        if arguments['--verbose'] or arguments['--dry-run']:
            print("{} -> {}".format(target, newname))
        os.rename(path, newpath)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='backup 0.1')
    print(arguments)

    #bak_dir = "/media/external"
    bak_dir = "/run/media/jake/Seagate\ Expansion\ Drive"
    print("Starting backup to {}".format(bak_dir))
    sources = ["/media/anime/library"]
    for source in sources:
        print("Backing up {}...".format(source))
        backup(source, bak_dir)
#        rename_all(bak_dir) renaming will cause the backup to rewrite everything each time
    print("Backup complete.")
