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

    def new_ch_run_args(mountpoint, ch_run_args):
        a = ch_run_args.copy()
        # assumes '--' is in args
        # will raise exception if '--' is not in args
        a.insert(a.index('--'), mountpoint)
        return a

    def call_chr_run_impl(mountpoint):
        with ChRunManager(args.squashfs_image, mountpoint):
            subprocess.run(['ch-run'] + new_ch_run_args(mountpoint, ch_run_args))

    if args.mount is not None:
        # if there is a user-supplied mountpoint for squashfs image via --mount arg,
        # call ch-run using this mountpoint
        call_chr_run_impl(args.mount)
    else:
        # if not, create a temporary directory and use it as a mountpoint and remove
        # the temporary directory afterwards
        with tempfile.TemporaryDirectory() as mountpoint:
           call_chr_run_impl(mountpoint)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--squashfs-image', type=str, required=True)
    parser.add_argument('-m', '--mount', type=str)

    args, ch_run_args = parser.parse_known_args()

    call_ch_run(args, ch_run_args)
    
if __name__ == '__main__':
    main()

