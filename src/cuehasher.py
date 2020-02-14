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
__date__ = "2020/02/13"

parser = argparse.ArgumentParser(description="use a database to identify and organize files.")

parser.add_argument("-i", "--input",
            dest="source_directory",
            required=True,
            help="set source directory")

parser.add_argument("-d", "--discs",
            dest="discs_file",
            required=True,
            help="discs file")

ARGS = parser.parse_args()

# File Management

def md5(file):
    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Game Metadata

def stripped_game_name(input):
    return input.split('(Disc ')[0].rstrip()

def game_disc(input):
    split_input = input.split('(Disc ')
    if len(split_input) > 1:
        disc = split_input[1].split(')')[0]
        # Workaround for Sister Princess 2 - Premium Fan Disc (Japan) 
        if disc == 'A': return 1
        if disc == 'B': return 2
        return int(split_input[1].split(')')[0])

# Process
discs = {}
with open(ARGS.discs_file) as input_file:
    discs = json.load(input_file)

def process_directory(directory, games):
    for (path, directories, files) in os.walk(directory):
        for file in files:
            extension = os.path.splitext(file)[1]
            if extension == '.cue':
                hash = md5(os.path.abspath(path + '/' + file))
                name = stripped_game_name(file)
                disc = game_disc(file)
                total = discs['games'][name]['discs']
                games['hashes'][hash] = {}
                games['hashes'][hash]['name'] = name
                games['hashes'][hash]['disc'] = {}
                games['hashes'][hash]['disc']['number'] = disc
                games['hashes'][hash]['disc']['total'] = total
# Main

games = {}
games['hashes'] = {}
with open(os.path.abspath('hashes.json'), 'w') as output_file:
    directory_paths = list()
    for (path, directories, file_names) in os.walk(ARGS.source_directory):
        directory_paths = [os.path.join(path, directory) for directory in directories]
        for directory_path in directory_paths:
            process_directory(directory_path, games)
    json.dump(games, output_file)
