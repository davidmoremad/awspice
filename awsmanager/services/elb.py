# -*- coding: utf-8 -*-
from base import AwsBase

class ElbService(AwsBase):

    def get_elbs(self):
        '''
        Get all Elastic Load Balancers for a region

        Returns:
            List of arrays with all ELBs
        '''
        return self.client.describe_load_balancers()['LoadBalancerDescriptions']

    def get_all_elbs(self):
        '''
        Get all Elastic Load Balancers for all regions

        Returns:
            List of arrays with all ELBs.
        '''
        elb_list = []
        for region in self.get_regions():
            self.set_client('elb', region['RegionName'])
            for elb in self.get_elbs():
                elb_list.append(elb)

        return elb_list

    def __init__(self):
        AwsBase.__init__(self, 'elb')
