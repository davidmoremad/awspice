# -*- coding: utf-8 -*-
from awspice.helpers import extract_region_from_ip
from threading import Lock

class FinderModule:
    '''
    This class makes it easy to search for components in AWS.

    Attributes:
        aws: awspice client

    '''

    def find_instance(self, filter_key, filter_value, profiles=[], regions=[]):
        '''
        Get an instance in different accounts and regions, using search filters.
        '''
        profiles = self.aws.ec2.parse_profiles(profiles)
        regions = self.aws.ec2.parse_regions(regions, True)

        # CODE SNIPPET from aws.service.ec2.instances.get_instance_by
        if filter_key == "publicip":
            ip_in_aws, ip_region = extract_region_from_ip(filter_value)
            if not ip_in_aws: return {}
            if regions and (ip_region in regions or ip_region in regions.keys()):
                regions = ip_region

        for account in profiles:
            self.aws.ec2.change_profile(account)
            instance = self.aws.ec2.get_instance_by(filter_key, filter_value, regions=regions)
            if instance: return instance
                
        return {}

    def find_instances(self, filter_key=None, filter_value=None, profiles=[], regions=[]):
        '''
        Get instances in different accounts and regions, using search filters.
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
        Get a volume in different accounts and regions, using search filters.
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
        Get group of volumes in different accounts and regions, using search filters.
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
        Get a load balancer in different accounts and regions, using search filters.
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
        Get load balancers in different accounts and regions, using search filters.
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
        Get IAM users in different accounts.
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
        '''
        Get inactive users in different accounts
        '''


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
