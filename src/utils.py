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

def handle_packet(packet, rules):
    '''
    handle packet based on rules
    packet format: <direction> <ip> <port> <flag> 
    '''
    counter = 0
    for rule in rules:
        counter += 1
        # eleminate not matched scenarios
        if rule == 'None':
            continue
        if packet['flag'] == '0' and rule['flag'] == '1':
            continue
        if packet['direction'] != rule['direction']:
            continue
        if not compare_ports(packet['port'], rule['port']):
            continue
        if not compare_ips(packet['ip'], rule['ip']):
            continue
        
        return '{}({}) {} {} {} {}'.format(rule['action'], counter, packet['direction'], packet['ip'], packet['port'], packet['flag'])
    # no matching rules
    return 'drop() {} {} {} {}'.format(packet['direction'], packet['ip'], packet['port'], packet['flag'])

def validate_ip(ip):
    '''
    validate ipv4
    source: https://stackoverflow.com/questions/3462784
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

def compare_ports(packet_port, rule_ports):
    if ('*' in rule_ports) or (packet_port in rule_ports):
        return True
    return False

def ip_to_int(ip):
    '''
    convert ip to int
    source: https://stackoverflow.com/questions/5619685
    '''
    chuncks = list(map(int, ip.split('.')))
    result = (16777216 * chuncks[0]) + (65536 * chuncks[1]) + (256 * chuncks[2]) + chuncks[3]
    
    return result

def ip_to_bin(ip):
    '''
    convert ip in dotten notaiton to binary
    source: https://stackoverflow.com/questions/2733788
    '''
    return ''.join([bin(int(x)+256)[3:] for x in ip.split('.')])

def compare_ips(packet_ip, rule_ip):
    '''
    checks packet_ip is in rule_ip
    source: https://gist.github.com/chuangbo/3338813
    '''
    if rule_ip == '*':
        return True

    full_ip = rule_ip.split('/')
    if len(full_ip) == 2:
        # MASK = (1 << 32) - 1
        # subnet = 32 - int(full_ip[1])
        # rule_ip = ip_to_int(full_ip[0])
       
        # subnet = MASK << subnet
        # cidr = rule_ip & subnet

        # return (ip_to_int(packet_ip) & cidr) == cidr

        rule_ip = ip_to_bin(full_ip[0])
        packet_ip = ip_to_bin(packet_ip)
        subnet = full_ip[1]
        mask = rule_ip[0:int(subnet)]
        
        return packet_ip.startswith(mask)
    elif len(full_ip) == 1:
        return packet_ip == rule_ip
    else:
        raise ValueError('Error: invalid ip.')


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
            log('Warning: direction unrecognized.')
            return 'None'
        
        # action
        action = items[1].lower()
        if action in ('accept', 'reject', 'drop'):
            rule['action'] = action
        else:
            log('Warning: action unrecognized.')
            return 'None'
        
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
                log('Warning: invalid ip.')
                return 'None'
        else:
            log('Warning: invalid ip.')
            return 'None'

        # port
        port = items[3]
        multi_port = port.split(',')
        rule['port'] = []
        if len(multi_port) == 1:
            if (port == '*') or (int(port) in range(0, 65536)):
                rule['port'].append(port)
            else:
                log('Warning: invalid port.')
                return 'None'
        elif len(multi_port) > 1:
            ports = []
            for p in multi_port:
                if int(p) in range(0, 65536):
                    ports.append(p)
            rule['port'] = ports
        else:
            log('Warning: invalid port.')
            return 'None'

        if len(items) == 5:
            # if flag used
            flag = items[4].lower()
            if flag == 'established':
                # store as 1 for easiness
                rule['flag'] = '1'
            else:
                log('Error: invalid flag.')
                return 'None'
        else:
            rule['flag'] = None
    # unsupported length
    else:
        log('Warning: line contains unexpected number of items: {}Must be 4 or 5.'.format(len(items)))
        return 'None'
    
    # return new rule
    return rule
