#!/usr/bin/env python
''' fw.py '''

import sys
import argparse

import utils

# list of dictionaries
rules = []
packets = []

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
                rules.append(utils.create_rule(items))
            except ValueError as e:
                utils.log(e)

    file.close()    
    utils.log('Done reading config file: {}'.format(filename))

def handle_packet(packet):
    '''
    handle packet based on rules
    '''
    packet_dic = {}
    global packets

    try:
        dir, ip, port, flag = packet.split()
    except ValueError:
        raise ValueError('Can\'t split packet.')

    verified = utils.verify_packet(dir, ip, port, flag)
    if not verified:
        raise ValueError('Error: invalid packet.')
    
    packet_dic['direction'] = dir
    packet_dic['ip'] = ip
    packet_dic['port'] = port
    packet_dic['flag'] = flag

    packets.append(packet_dic)
    
    # compare to rules and emit results
    res = utils.handle_packet(packet_dic, rules)
    print(res)

def read_packets():
    '''
    read packet file from stdin
    '''
    for line in sys.stdin:
        line = line.strip()
        try:
            handle_packet(line)
        except ValueError as e:
            utils.log('Error reading packets.' + str(e))
    utils.log('Done reading packets file.')

def parse_args():
    '''
    Handles parsing arguments and returning arguments list
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
    # utils.print_list(rules)
    read_packets()
    # utils.print_list(packets)
    # print(utils.compare_ips('136.159.5.6', '*'))


if __name__ == '__main__':
    main()