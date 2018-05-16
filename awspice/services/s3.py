# -*- coding: utf-8 -*-
from awspice.services.base import AwsBase
from botocore.exceptions import ClientError

class S3Service(AwsBase):
    '''
    Class belonging to the S3 Storage service.
    '''

    def get_buckets(self):
        '''
        Get all buckets in S3

        Returns:
            Buckets (list): List of dictionaries with the buckets requested
        '''
        return self.inject_client_vars(self.client.list_buckets()['Buckets'])

    def get_public_buckets(self):
        '''
        Get all public readable or writable buckets in S3

        Returns:
            Buckets-ACL (list): List of dictionaries with the buckets requested
        '''
        buckets = []
        for bucket in self.get_buckets():

            try:
                bucket_acl = self.client.get_bucket_acl(Bucket=bucket['Name'])

                # https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html
                global_acl = 'http://acs.amazonaws.com/groups/global/AllUsers'
                permissions = ['READ', 'WRITE']
                public_bucket = {}

                for grant in bucket_acl['Grants']:
                    if grant.get('Permission') in permissions and grant['Grantee'].get('URI') == global_acl:
                        if public_bucket.get('Name'):
                            public_bucket['Permissions'].append(grant['Permission'])
                        else:
                            public_bucket['Name'] = bucket['Name']
                            public_bucket['Permissions'] = []
                            public_bucket['Permissions'].append(grant['Permission'])

                if public_bucket:
                    buckets.append(public_bucket)

            except ClientError:
                # Exception: Lack of permissions
                pass

        return self.inject_client_vars(buckets)

    def __init__(self):
        AwsBase.__init__(self, 's3')
