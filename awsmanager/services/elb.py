# -*- coding: utf-8 -*-
from base import AwsBase

class ElbService(AwsBase):

    def get_elbs(self, region_switch=False):
        '''
        Get all Elastic Load Balancers for a region

        Returns:
            List of arrays with all ELBs
        '''
        results = list()
        regions = self.get_regions() if region_switch else [{'RegionName': AwsBase.region}]
        for region in regions:
            self.change_region(region['RegionName'])
            elbs = self.client.describe_load_balancers()['LoadBalancerDescriptions']
            results.extend(self.inject_client_vars(elbs))

        return results

    def __init__(self):
        AwsBase.__init__(self, 'elb')
