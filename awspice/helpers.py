# -*- coding: utf-8 -*-
import json
import datetime
import socket
from time import mktime

class ClsEncoder(json.JSONEncoder):
    '''
    JSON encoder extension.

    Sometimes Boto3 returns a non-serializable result to JSON and we get the following error when dumping that result:
    `TypeError: datetime.datetime (2015, 12, 3, 21, 20, 17, 326000, tzinfo = tzutc ()) is not JSON serializable`
    Solve it using this class encoder in ``cls`` argument

    Examples:
        json.dumps(results, indent=4, cls=awspice.ClsEncoder)
    '''

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))

        return json.JSONEncoder.default(self, obj)


def ip_in_aws(ip):
    '''
    Check if an IP address is from AWS

    Arguments:
        ip: Address to check 

    Returns:
        bool
    '''
    return bool(dnsinfo_from_ip(ip))

def dnsinfo_from_ip(ip):
    '''
    Returns the DNS name of an IP address

    Arguments:
        ip: Address of the element.

    Examples:
        dns = get_dnsname_from_ip('8.8.8.8')

    Returns:
        dict: {'region': 'eu-west-1', 'service': 'ec2'}
    '''
    result = {}
    service_matchs = {'compute': 'ec2'}
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        if hostname.endswith('aws.com'):
            result['region'] = hostname.split('.')[1]
            service = hostname.split('.')[2]
            result['service'] = service_matchs[service] if service in service_matchs.keys() else service
    except socket.herror:
        pass
    return result
