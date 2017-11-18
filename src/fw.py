#!/usr/bin/env python
''' fw.py '''

import sys
import string
import argparse

def create_rule(line):
    '''
    create a rule for each configuration line
    @param line: each line must have 4 to 5 items
    line format: <direction> <action> <ip> <port> [flag]
    '''


def read_configs(filename):
    '''
    read config file
    '''
    with open(filename) as file:
        for line in file:
            line = line.strip()
            line = line.split()
            
            create_rule(line)

    file.close()    
    print('Done reading config file: {}'.format(filename))

def parse_args():
    '''
    Handles parsing arguments and returning arugments list
    Reference: https://docs.python.org/3/library/argparse.h
    '''
    usage = 'python3 fw.py rules_filename'
    parser = argparse.ArgumentParser(usage=usage)

    parser.add_argument('rules_filename', 
                        help='firewall configuration file',
                        type=str)
    
    return parser.parse_args()

def main():
    args = parse_args()

if __name__ == '__main__':
    main()