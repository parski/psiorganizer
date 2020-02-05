#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
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

parser.add_argument("-s", "--strict",
            dest="halt_on_missing",
            required=False,
            help="halts process if unable to match a file")

ARGS = parser.parse_args()

# Initialize Hash Serial Map

serials = {}
with open(os.path.abspath('../lib/hashes.json'), 'r') as hashes_json:
    serials = json.load(hashes_json)

# Initialize Serial Game Map

games = {}
with open(os.path.abspath('../lib/games.json'), 'r') as games_json:
    games = json.load(games_json)

# File Management

def hash(file):
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

def process(file):
    try:
        serial = serials[hash(file)]
        try: 
            game = games[serial]
            print('Importing ' + file + ' as ' + game['title'] + ' [' + serial + ']')
            path = os.path.abspath(ARGS.output_directory + '/' + game['title'] + ' (' + game['region'] + ')')

            if not os.path.exists(path):
                os.makedirs(path)

            # Copy file to proper location
            file_destination_path = os.path.abspath(path + '/' + formatted_file_name(game, file))
            if not os.path.exists(file_destination_path):
                copy_file(file, file_destination_path)

            process_cover(path, serial)
            process_multidisc(path, game, os.path.splitext(file)[1])
        except KeyError:
            print('Error: No entry found for serial ' + serial + ' \nFile ' + file + '\nFeel free to add the missing entry and contribute on GitHub: https://github.com/parski/psiorganizer')
            if ARGS.halt_on_missing:
                exit(1)
    except KeyError:
        print('Error: No entry found for hash ' + hash(file) + ' \nFile ' + file + '\nFeel free to add the missing entry and contribute on GitHub: https://github.com/parski/psiorganizer')
        if ARGS.halt_on_missing:
            exit(1)

# Main

file_paths = list()
for (path, directories, file_names) in os.walk(ARGS.source_directory):
    file_paths += [os.path.join(path, file) for file in file_names]

for file_path in file_paths:
    file = os.path.abspath(file_path)
    if file.endswith('.bin') or file.endswith('.cue') or file.endswith('.iso') or file.endswith('.img'):
        process(file)
        continue
    else:
        continue

# Todo:
# - Lowercase/uppercase a lot of things
# - Use os.path on all paths so they work on Windows???
# - Use cue2cu2
