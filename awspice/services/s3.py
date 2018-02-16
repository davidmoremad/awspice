# -*- coding: utf-8 -*-
from base import AwsBase

class S3Service(AwsBase):

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
                permissions_to_check = ['READ', 'WRITE']
                public_acl_indicator = 'http://acs.amazonaws.com/groups/global/AllUsers' # https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html

                for grant in bucket_acl_response['Grants']:
                    for (k, v) in grant.iteritems():
                        if k == 'Permission' and any(permission in v for permission in permissions_to_check):
                            for (grantee_attrib_k, grantee_attrib_v) in grant['Grantee'].iteritems():
                                if 'URI' in grantee_attrib_k and grant['Grantee']['URI'] == public_acl_indicator:
                                    if public_bucket.get('Name'):
                                        public_bucket['Permissions'].append(v)
                                    else:
                                        public_bucket['Name'] = bucket['Name']
                                        public_bucket['Permissions'] = []
                                        public_bucket['Permissions'].append(v)

                if public_bucket: results.append(public_bucket)
            except:
                pass
        return self.inject_client_vars(results)

    def __init__(self):
        AwsBase.__init__(self, 's3')
