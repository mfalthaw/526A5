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
    
    if len(items) in (4, 5):
        rule['direction'] = items[0].lower()
        rule['action'] = items[1].lower()
        rule['ip'] = items[2]
        rule['port'] = items[3]
        if len(items) == 5:
            # if flag used
            rule['flag'] = items[4]
        else:
            rule['flag'] = None
    # unsupported length
    else:
        raise ValueError('Error: line contains unexpected number of items: {}\nMust be 4 or 5.'.format(len(items)))
    
    # return new rule
    return rule

def read_configs(filename):
    '''
    read config file
    '''
    global rules

    with open(filename) as file:
        for line in file:
            line = line.strip()
            items = line.split()
            
            rules.append(create_rule(items))

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
    read_configs(args.rules_filename)

if __name__ == '__main__':
    main()