#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import hashlib
import argparse
import zipfile

__author__ = "Pär Strindevall"
__date__ = "2020/02/02"

 __name__ == '__main__':
    """
    Parse arguments from command line.
    """
    parser = argparse.ArgumentParser(description="use a database to identify and organize files.")

    parser.add_argument("-i", "--input",
                        dest="source_directory",
                        required=True,
                        help="set source directory")

    parser.add_argument("-o", "--output",
                        dest="output_directory",
                        required=True,
                        help="set output directory")

    ARGS = parser.parse_args()

def copy_file(source, dest):
    try:
        shutil.copyfile(source, dest)
    except FileNotFoundError:
        # Windows' default API is limited to paths of 260 characters
        fixed_dest = u'\\\\?\\' + os.path.abspath(dest)
        shutil.copyfile(source, fixed_dest)


def extract_file(filename, entry, method, dest):
    if method == 'zip':
        try:
            zipfile.ZipFile(filename).extract(entry, os.path.dirname(dest))
            filename = os.path.join(os.path.dirname(dest), entry)
            if filename != dest:
                os.replace(filename, dest)
        except FileNotFoundError:
            # Windows' default API is limited to paths of 260 characters
            fixed_dest = u'\\\\?\\' + os.path.abspath(dest)
            zipfile.ZipFile(filename).extract(entry, os.path.dirname(fixed_dest))
