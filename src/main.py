#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from binmerge import binmerge
import glob
import hashlib
import json
import os
import shutil
import sys
import zipfile

__author__ = "Pär Strindevall"
__date__ = "2020/02/02"

parser = argparse.ArgumentParser(description="use a database to identify and organize files.")

parser.add_argument("-i", "--input",
            dest="source_directory",
            required=True,
            help="set source directory")

parser.add_argument("-o", "--output",
            dest="output_directory",
            required=True,
            help="set output directory")

parser.add_argument("-m", "--hashes",
            dest="hashes_file",
            required=True,
            help="path to hashes file")

parser.add_argument("-d", "--discs",
            dest="discs_file",
            required=True,
            help="path to discs file")

ARGS = parser.parse_args()

# Initialize Hash Game Map

hashes = {}
with open(os.path.abspath(ARGS.hashes_file), 'r') as file:
    hashes = json.load(file)

# File Management

def md5(file):
    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def copy_file(source, destination):
    try:
        shutil.copyfile(source, destination)
    except FileNotFoundError:
        # Windows' default API is limited to paths of 260 characters
        fixed_destination = u'\\\\?\\' + os.path.abspath(destination)
        shutil.copyfile(source, fixed_destination)

# Process

def formatted_file_name(game, file):
    try:
        return game['title'] + ' (Disc ' + str(game['disc']['number']) + ')' + os.path.splitext(file)[1]
    except KeyError:
        return game['title'] + os.path.splitext(file)[1]    

def process_cover(path, serial):
    cover_source_path = os.path.abspath('../covers/' + serial + '.bmp')
    cover_destination_path = os.path.abspath(path + '/COVER.BMP')
    if os.path.exists(cover_source_path) and not os.path.exists(cover_destination_path):
        copy_file(cover_source_path, cover_destination_path)

def multidisc_for_game(game, extension):
    try: 
        total = game['disc']['total']
        multidisc = game['title'] + ' (Disc 1)' + extension + '\n'
        for number in range(2, total + 1):
            multidisc = multidisc + game['title'] + ' (Disc ' + str(number) + ')' + extension + '\n'
        return multidisc
    except KeyError:
        return None

def process_multidisc(path, game, extension):
    multidisk_destination_path = os.path.abspath(path + '/MULTIDISC.LST')
    if not os.path.exists(multidisk_destination_path):
        if extension == '.bin' or extension == '.iso' or extension == '.img':
            multidisc = multidisc_for_game(game, os.path.splitext(file)[1])
            if not multidisc == None:
                with open(multidisk_destination_path, 'w') as multidisc_file:
                    multidisc_file.write(multidisc)
                    multidisc_file.close()

def file_name_without_extension(hash):
    if hash in hashes['hashes']:
        game = hashes['hashes'][hash]
        if game['disc']['total'] > 1:
            return game['name'] + ' (Disc ' + str(game['disc']['number']) + ')'
        return game['name']


def process_directory(directory):
    for (path, directories, files) in os.walk(directory):
        for file in files:
            extension = os.path.splitext(file)[1]
            if extension == '.cue':
                hash = md5(os.path.abspath(path + '/' + file))
                if hash in hashes['hashes']:
                    game = hashes['hashes'][hash]
                    output_path = os.path.abspath(ARGS.output_directory + '/' + game['name'])
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    binmerge(os.path.abspath(directory + '/' + file), file_name_without_extension(hash), output_path)
# Main

directory_paths = list()
for (path, directories, file_names) in os.walk(ARGS.source_directory):
    directory_paths = [os.path.join(path, directory) for directory in directories]
    for directory_path in directory_paths:
        process_directory(directory_path)

# Todo:
# - Use cue2cu2
# - Generate multidisc
# - Cover
