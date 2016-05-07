#!/usr/bin/python3

from random import randint, choice
from sys import argv
from argparse import ArgumentParser, FileType

parser = ArgumentParser(description='Process some integers.')

parser.add_argument('-l', '--lines', type=int)
parser.add_argument('-s', '--syllables', type=int)
parser.add_argument('-o', '--output-file', type=FileType('w'))

f = open('syllables','r')

output = parser.parse_args().output_file
lines = parser.parse_args().lines
syllables = parser.parse_args().syllables
sounds = f.read().splitlines()

output_str = ""

for i in range(lines):
    output_str += str(i).zfill(3) + " "
    for j in range(syllables-1):
        output_str += choice(sounds)
        output_str += "_"

    output_str += choice(sounds)
    output_str += "\n\n"

output.write(output_str)
