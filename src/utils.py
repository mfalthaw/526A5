#!/usr/bin/env python
''' utils.py '''

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