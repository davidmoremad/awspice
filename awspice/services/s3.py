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
        results = []
        for bucket in self.get_buckets():
            # Lack of permissions
            try:
                bucket_acl_response = self.client.get_bucket_acl(Bucket=bucket['Name'])

                public_bucket = {}
                permissions_checked = ['READ', 'WRITE']
                # https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html
                global_acl = 'http://acs.amazonaws.com/groups/global/AllUsers'

                for grant in bucket_acl_response['Grants']:
                    for (gkeys, gvalues) in grant.iteritems():
                        if gkeys == 'Permission' and any(perm in gvalues for perm in permissions_checked):
                            for grantee_keys in grant['Grantee'].keys():
                                if 'URI' in grantee_keys and grant['Grantee']['URI'] == global_acl:
                                    if public_bucket.get('Name'):
                                        public_bucket['Permissions'].append(gvalues)
                                    else:
                                        public_bucket['Name'] = bucket['Name']
                                        public_bucket['Permissions'] = []
                                        public_bucket['Permissions'].append(gvalues)

                if public_bucket: results.append(public_bucket)
            except ClientError:
                pass
        return self.inject_client_vars(results)

    def __init__(self):
        AwsBase.__init__(self, 's3')
