# -*- coding: utf-8 -*-
from base import AwsBase

class VpcManager(AwsBase):

    def get_vpcs(self):
        '''
        Get all VPCs for a region

        Returns:
            List of arrays with all VPCs
        '''
        return self.client.describe_vpcs()['Vpcs']

    def __init__(self, access_key, secret_key, profile):
        AwsBase.__init__(self, 'ec2', access_key, secret_key, profile)
