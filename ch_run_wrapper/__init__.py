#!/usr/bin/env python

import sys
import argparse
import tempfile
import subprocess

__author__ = 'Apuã Paquola'

class ChRunManager():
    """
    Context manager to call ch-run
    """

    def __init__(self, squashfs_image, mount_point):
        self.squashfs_image = squashfs_image
        self.mount_point = mount_point

    def __enter__(self):
        # mount image
        subprocess.run(['squashfuse', self.squashfs_image, self.mount_point],
                       check=True)
        return True

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # unmount image
        subprocess.run(['fusermount', '-u', self.mount_point])

        
def call_ch_run(args, ch_run_args):

    def new_ch_run_args(squashfs_image, ch_run_args):
        a = ch_run_args.copy()
        # assumes '--' is in args
        # will raise exception if '--' is not in args
        a.insert(a.index('--'), squashfs_image)
        return a
        
    #with tempfile.TemporaryDirectory() as tmpdirname:
    #    print('created temporary directory', tmpdirname)

    with ChRunManager(args.squashfs_image, args.mount):
        #raise Exception('testing')
        #subprocess.run(f'ls -1 "{args.mount}" | wc -l ', shell=True, check=True)
        subprocess.run(['ch-run'] + new_ch_run_args(args.mount, ch_run_args))

        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--squashfs-image', type=str, required=True)
    parser.add_argument('-m', '--mount', type=str)

    args, ch_run_args = parser.parse_known_args()

    #print(args)
    #print(ch_run_args)

    call_ch_run(args, ch_run_args)
    
if __name__ == '__main__':
    main()

