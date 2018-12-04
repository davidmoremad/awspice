# -*- coding: utf-8 -*-
from awspice.helpers import dnsinfo_from_ip
from threading import Lock

class FinderModule:
    '''
    This class makes it easy to search for components in AWS.

    Attributes:
        aws: awspice client

    '''

    def _filters_validation(self, filter_key, filter_value, regions):
        '''
        Check some previous test to filters before do the main action.

        Args:
            filter_key (str)
            filter_value (str)

        Return:
            bool: True if filters are validated
        '''
        result = True

        if filter_key == 'publicip':
            hostname = dnsinfo_from_ip(filter_value)
            result = bool(hostname) and self.aws.ec2.region_in_regions(hostname['region'], regions)

        return result

    def find_instance(self, filter_key, filter_value, profiles=[], regions=[]):
        '''
        Searches for an instance in different accounts and regions, using search filters.
        '''
        profiles = self.aws.ec2.parse_profiles(profiles)
        regions = self.aws.ec2.parse_regions(regions, True)
        if not self._filters_validation(filter_key, filter_value, regions):
            return None

        for account in profiles:
            self.aws.ec2.change_profile(account)
            instance = self.aws.ec2.get_instance_by(filter_key, filter_value, regions=regions)
            if instance: return instance
        return None

    def find_instances(self, filter_key=None, filter_value=None, profiles=[], regions=[]):
        '''
        Searches for a group of instances in different accounts and regions, using search filters.
        '''
        results = list()
        profiles = self.aws.ec2.parse_profiles(profiles)
        regions = self.aws.ec2.parse_regions(regions, True)


        for account in profiles:
            self.aws.ec2.change_profile(account)
            if filter_key and filter_value:
                results.extend(self.aws.ec2.get_instances_by(filter_key, filter_value, regions=regions))
            else:
                results.extend(self.aws.ec2.get_instances(regions=regions))
        return results

    def find_volume(self, filter_key, filter_value, profiles=[], regions=[]):
        '''
        Searches for an volume in different accounts and regions, using search filters.
        '''
        profiles = self.aws.ec2.parse_profiles(profiles)
        regions = self.aws.ec2.parse_regions(regions, True)

        for account in profiles:
            self.aws.ec2.change_profile(account)
            volume = self.aws.ec2.get_volume_by(filter_key, filter_value, regions=regions)
            if volume: return volume
        return None

    def find_volumes(self, filter_key=None, filter_value=None, profiles=[], regions=[]):
        '''
        Searches for a group of volumes in different accounts and regions, using search filters.
        '''
        results = list()
        profiles = self.aws.ec2.parse_profiles(profiles)
        regions = self.aws.ec2.parse_regions(regions, True)

        for account in profiles:
            self.aws.ec2.change_profile(account)
            if filter_key and filter_value:
                results.extend(self.aws.ec2.get_volumes_by(filter_key, filter_value, regions=regions))
            else:
                results.extend(self.aws.ec2.get_volumes(regions=regions))
        return results


    def find_loadbalancer(self, filter_key, filter_value, profiles=[], regions=[]):
        '''
        Searches for a load balancer in different accounts and regions, using search filters.
        '''
        profiles = self.aws.elb.parse_profiles(profiles)
        regions = self.aws.elb.parse_regions(regions, True)

        for account in profiles:
            self.aws.elb.change_profile(account)
            elb = self.aws.elb.get_loadbalancer_by(filter_key, filter_value, regions=regions)
            if elb: return elb
        return None


    def find_loadbalancers(self, filter_key=None, filter_value=None, profiles=[], regions=[]):
        '''
        Searches for a load balancers in different accounts and regions, using search filters.
        '''
        results = list()
        profiles = self.aws.elb.parse_profiles(profiles)
        regions = self.aws.elb.parse_regions(regions, True)

        for account in profiles:
            self.aws.elb.change_profile(account)
            if filter_key and filter_value:
                results.extend([self.aws.elb.get_loadbalancer_by(filter_key, filter_value, regions=regions)])
            else:
                results.extend(self.aws.elb.get_loadbalancers(regions=regions))
        return results
        
    def find_users(self, profiles=[]):
        '''
        Search IAM users in different accounts.
        '''
        results = list()
        profiles = self.aws.iam.parse_profiles(profiles)
        lock = Lock()

        def worker(profile):
            lock.acquire()
            self.aws.iam.change_profile(profile)
            lock.release()

            results.extend(self.aws.iam.get_users())

        for profile in profiles: self.aws.iam.pool.add_task(worker, profile)
        self.aws.iam.pool.wait_completion()

        return results


    def find_inactive_users(self, profiles=[]):
        results = []
        profiles = self.aws.iam.parse_profiles(profiles)

        for profile in profiles:
            self.aws.iam.change_profile(profile)
            results.extend(self.aws.iam.get_inactive_users())

        return results



    def find_buckets(self, profiles=[]):
        '''
        Search S3 buckets in different accounts.
        '''
        results = list()
        profiles = self.aws.s3.parse_profiles(profiles)
        lock = Lock()

        def worker(profile):
            lock.acquire()
            self.aws.s3.change_profile(profile)
            lock.release()
            results.extend(self.aws.s3.get_buckets())

        for profile in profiles: self.aws.s3.pool.add_task(worker, profile)
        self.aws.s3.pool.wait_completion()

        return results


    def __init__(self, aws):
        self.aws = aws
