#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
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

ARGS = parser.parse_args()

# Initialize Hash Identifier Map

identifiers = {}
with open('../lib/hashes.json') as hashes_json:
    identifiers = json.load(hashes_json)

# Initialize Identifier Game Map

games = {}
with open('../lib/games.json') as games_json:
    games = json.load(games_json)

#

def identifier_for_hash(hash):
    return identifiers[hash]

def game_for_identifier(identifier):
    return games[identifier]

def path_for_game(game):
    return os.path.abspath(ARGS.output_directory + '/' + game['region'] + '/' + game['title'] )

def cover_for_identifier(identifier):
    return os.path.abspath('../covers/' + identifier + '.bmp')

# def multidisc(game):

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

# Process

def process(file):
    identifier = identifier_for_hash(hash(file))

    game = game_for_identifier(identifier)
    print('Importing ' + game["title"] + ' [' + identifier + ']')


    cover = cover_for_identifier(identifier)


    path = path_for_game(game)

    if not os.path.exists(path):
        os.makedirs(path)

    destination_path = path + '/' + game['title'] + os.path.splitext(file)[1]
    copy_file(file, destination_path)

    # copy_file(file, path, game)

# Main

process(ARGS.source_directory)