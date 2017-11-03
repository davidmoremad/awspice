# -*- coding: utf-8 -*-
from base import AwsBase

class S3Service(AwsBase):

    def get_buckets(self):
        '''
        Get all buckets in S3 for a region

        Returns:
            List of arrays with all buckets
        '''
        return self.client.list_buckets()['Buckets']

    def __init__(self):
        AwsBase.__init__(self, 's3')
