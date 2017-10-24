# -*- coding: utf-8 -*-
from base import AwsBase

class RdsManager(AwsBase):

    def get_rdss(self):
        '''
        Get all RDS for a region

        Returns:
            List of arrays with all RDS instances
        '''
        return self.client.describe_db_instances()['DBInstances']

    def __init__(self, access_key, secret_key, profile):
        AwsBase.__init__(self, 'rds', access_key, secret_key, profile)
