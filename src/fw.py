#!/usr/bin/env python
''' fw.py '''

import sys
import string
import argparse

# list of dictinaries
rules = []

DEBUG = True

def create_rule(items):
    '''
    create a rule for each configuration line
    @param items: each line must have 4 to 5 items
    line format: <direction> <action> <ip> <port> [flag]
    '''
    rule = {}

    if len(items) in (4, 5):
        # direction
        direction = items[0].lower()
        if direction in ('in', 'out'):
            rule['direction'] = direction
        else:
            raise ValueError('Error: direction unrecogonized.')
        
        # action
        action = items[1].lower()
        if action in ('accept', 'reject', 'drop'):
            rule['action'] = action
        else:
            raise ValueError('Error: action unrecogonized.')
        
        # ip
        ip = items[2]
        if (ip == '*') \
            or (ip.count('.') == 3) \
            or (ip.count('.') == 3  and ip.count('/') == 1):
            rule['ip'] = ip
        else:
            raise ValueError('Error: invalid ip.')

        # port
        port = items[3]
        multi_port = port.split(',')
        if len(multi_port) == 1:
            if (port == '*') or (int(port) in range(0, 65536)):
                rule['port'] = port
            else:
                raise ValueError('Error: invalid port.')
        elif len(multi_port) > 1:
            ports = []
            for p in multi_port:
                p = int(p)
                if p in range(0, 65536):
                    ports.append(p)
            rule['port'] = ports
        else:
            print('port: {}'.format(multi_port))
            raise ValueError('Error: invalid port.')

        if len(items) == 5:
            # if flag used
            flag = items[4].lower()
            if flag == 'established':
                rule['flag'] = flag
            else:
                raise ValueError('Error: invalid flag.')
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
            try:
                rules.append(create_rule(items))
            except ValueError as e:
                if DEBUG:
                    print(e)

    file.close()    
    print('Done reading config file: {}'.format(filename))

def validate_ip(ip):
    '''
    validate ipv4
    source: https://stackoverflow.com/questions/3462784/check-if-a-string-matches-an-ip-address-pattern-in-python
    '''
    addr = ip.split('.')
    if len(addr) != 4:
        return False
    for a in addr:
        if not a.isdigit():
            return False
        if not (0 <= int(a) <= 255):
            return False
    
    return True

def verify_packet(dir, ip, port, flag):
    # dir
    if dir not in ('in', 'out'):
        return False
    
    # ip
    return validate_ip()
    
    # port
    # flag

    retrun True

def handle_packet(packet):
    '''
    handle packet based on rules
    '''
    try:
        dir, ip, port, flag = packet.split()
    except ValueError:
        raise ValueError('Can\'t split packet.')
    
    verified = verify_packet(dir, ip, port, flag)
    if not verified:
        raise ValueError('Error: invalid packet.')
    
    # compare to rules and emit resuls

def read_packets():
    '''
    read packet file from stdin
    '''
    for line in sys.stdin:
        line = line.strip()
        try:
            handle_packet(line)
        except ValueError, e:
            print('Error reading packets.' + e)

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

def print_rules():
    for rule in rules:
        print(rule)

def main():
    args = parse_args()
    read_configs(args.rules_filename)
    # print_rules()
    read_packets()

if __name__ == '__main__':
    main()