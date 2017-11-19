#!/usr/bin/env python
''' utils.py '''

import sys

DEBUG = True

def print_list(list):
    i = 1
    for item in list:
        print('{}: {}'.format(i, item))
        i += 1

def log(msg):
    if DEBUG:
        print(msg, file=sys.stderr)

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
    if not validate_ip(ip):
        return False
    # port
    if int(port) not in range(0, 65536):
        return False
    # flag
    if flag not in ('1', '0'):
        return False

    return True

def ip_2_int(ip):
    '''
    convert ip to int
    source: https://stackoverflow.com/questions/5619685/conversion-from-ip-string-to-integer-and-backward-in-python
    '''
    chucks = list(map(int, ip.split('.')))
    result = (16777216 * chucks[0]) + (65536 * chucks[1]) + (256 * chucks[2]) + chucks[3]
    
    return result

def compare_ips(packet_ip, rule_ip, mask):
    '''
    checks packet_ip is in rule_ip
    source: https://gist.github.com/chuangbo/3338813
    '''
    MASK = (1 << 32) - 1
    
    packet_ip = ip_2_int(packet_ip)
    mask = MASK << mask
    cidr = packet_ip & mask

    return ip_2_int(rule_ip) & cidr == cidr


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
            raise ValueError('Error: direction unrecognized.')
        
        # action
        action = items[1].lower()
        if action in ('accept', 'reject', 'drop'):
            rule['action'] = action
        else:
            raise ValueError('Error: action unrecognized.')
        
        # ip
        ip = items[2]
        if ip == '*':
            rule['ip'] = ip
        elif ip.count('/') == 1:
            addr, mask = ip.split('/')
            if validate_ip(addr):
                # TODO handle mask
                rule['ip'] = ip
            else:
                raise ValueError('Error: invalid ip.')
        else:
            raise ValueError('Error: invalid ip.')

        # port
        port = items[3]
        multi_port = port.split(',')
        rule['port'] = []
        if len(multi_port) == 1:
            if (port == '*') or (int(port) in range(0, 65536)):
                rule['port'].append(port)
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
