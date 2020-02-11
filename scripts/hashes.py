#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import sys
from lxml import etree
from io import StringIO

__author__ = "Pär Strindevall"
__date__ = "2020/02/06"

parser = argparse.ArgumentParser(description="generate hashes database")

parser.add_argument("-i", "--input",
            dest="discs_json",
            required=True,
            help="discs json path")

parser.add_argument("-d", "--datfile",
            dest="datfile",
            required=True,
            help="datfile path")            

ARGS = parser.parse_args()

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

def game_from_discs(name, disc, discs):
    game = {}
    game['name'] = name
    game['disc'] = {}
    if disc:
        game['disc']['number'] = disc
    else:
        game['disc']['number'] = 1
    if name in discs['games']:
        game['disc']['total'] = discs['games'][name]['discs']
    else:
        game['disc']['total'] = 1

    return game

with open(ARGS.discs_json) as input_file:
    discs = json.load(input_file)

    output = {}
    output['hashes'] = {}
    with open(os.path.abspath('hashes.json'), 'w') as output_file:
        # Load Datfil
        with open(ARGS.datfile) as datfile_file:
            xml = datfile_file.read()
            root = etree.fromstring(xml)
            game_name = None
            for element in root.getchildren():
                if element.tag == 'header':
                    for metatag in element.getchildren():
                        if metatag.tag == 'version':
                            output['version'] = metatag.text
                if element.tag == 'game':
                    game_name = element.attrib['name']
                    stripped_name = stripped_game_name(game_name)
                    disc_number = game_disc(game_name)
                    for rom in element.getchildren():
                        if 'name' in rom.attrib and 'md5' in rom.attrib:
                            if rom.attrib['name'].endswith('.cue'):
                                output['hashes'][rom.attrib['md5']] = game_from_discs(stripped_name, disc_number, discs)
        json.dump(output, output_file)
