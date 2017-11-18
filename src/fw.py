#!/usr/bin/env python
''' fw.py '''

import sys
import string
import argparse

# list of dictinaries
rules = []

def create_rule(items):
    '''
    create a rule for each configuration line
    @param items: each line must have 4 to 5 items
    line format: <direction> <action> <ip> <port> [flag]
    '''
    rule = {}

    # no flag used
    if len(items) == 4:
        pass
    # flag used    
    elif len(items) == 5:
        pass
    # unsupported length
    else:
        raise ValueError('Error: line contains unexpected number of items: {}\nMust be 4 or 5.'.format(len(items)))

def read_configs(filename):
    '''
    read config file
    '''
    with open(filename) as file:
        for line in file:
            line = line.strip()
            items = line.split()
            
            create_rule(items)

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