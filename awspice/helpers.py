# -*- coding: utf-8 -*-
from threading import Thread
from Queue import Queue
from time import mktime
import json
import datetime
import socket

class Worker(Thread):
    """
    Thread executing tasks from a given tasks queue
    http://code.activestate.com/recipes/577187-python-thread-pool/
    """
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try: func(*args, **kargs)
            except Exception, e: print e
            self.tasks.task_done()

class ThreadPool:
    """
    Pool of threads consuming tasks from a queue
    http://code.activestate.com/recipes/577187-python-thread-pool/
    """
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()


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


def extract_region_from_ip(ip):
    '''Get the region where a IP is located and if it's on AWS

    Args:
        ip (str): IP address 
    
    Returns:
        (bool, str): It's in AWS / Region where the IP is located
    '''
    hostname = dnsinfo_from_ip(ip)

    if hostname:
        region = hostname['region']
        return (True, region) if region else (True, '')
    else:
        return (False, None)



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
        host = socket.gethostbyaddr(ip)[0]
        if host.endswith('aws.com'):
            # ELASTIC IPs > name.service.aws.com (4)
            # AUTOASSIGNED IPs > name.region.service.aws.com (5)
            service = host.split('.')[2]
            if service in service_matchs.keys():
                service = service_matchs[service]

            if len(host.split('.')) == 5:
                region = host.split('.')[1]
            else:
                region = None
            
            result = {'region': region, 'service': service}
        return result
    except socket.herror:
        pass
    except socket.gaierror:
        pass
    return result
