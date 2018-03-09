# -*- coding: utf-8 -*-
from base import AwsBase

class RdsService(AwsBase):
    '''
    Class belonging to the Remote Database system service.
    '''

    def get_rdss(self):
        '''
        Get all RDS for a region

        Returns:
            List of arrays with all RDS instances
        '''
        return self.inject_client_vars(self.client.describe_db_instances()['DBInstances'])

    def __init__(self):
        AwsBase.__init__(self, 'rds')
