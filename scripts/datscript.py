#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import sys
from lxml import etree
from io import StringIO

__author__ = "Pär Strindevall"
__date__ = "2020/02/11"

parser = argparse.ArgumentParser(description="generate hashes database")

parser.add_argument("-i", "--input",
            dest="datfile_path",
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

discs = {}
discs['games'] = {}
# Open Output
with open(os.path.abspath('discs.json'), 'w') as output_file:
    # Load Datfile
    with open(ARGS.datfile_path) as fobj:
        xml = fobj.read()

    root = etree.fromstring(xml)
    game_name = None
    for element in root.getchildren():
        if element.tag == 'header':
            for metatag in element.getchildren():
                if metatag.tag == 'version':
                    discs['version'] = metatag.text
        if element.tag == 'game':
            game_name = element.attrib['name']
            stripped_name = stripped_game_name(game_name)
            if not stripped_name in discs['games']:
                discs['games'][stripped_name] = {}
            for rom in element.getchildren():
                disc_number = game_disc(game_name)
                if disc_number:
                    if not 'discs' in discs['games'][stripped_name]:
                        discs['games'][stripped_name]['discs'] = int(disc_number)
                    else:
                        previous_total = discs['games'][stripped_name]['discs']
                        if int(disc_number) > previous_total:
                            discs['games'][stripped_name]['discs'] = int(disc_number)
                else:
                    if not 'discs' in discs['games'][stripped_name]:
                        discs['games'][stripped_name]['discs'] = 1
    json.dump(discs, output_file)
