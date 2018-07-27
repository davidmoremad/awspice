# -*- coding: utf-8 -*-
from awspice.services.base import AwsBase
from botocore.exceptions import ClientError
import StringIO

class S3Service(AwsBase):
    '''
    Class belonging to the S3 Storage service.
    '''

    def upload_string_as_file(self, bucket_name, filepath, content):
        '''
        Upload string as a file to S3 bucket

        Args:
            bucket_name (str): Name of the S3 bucket
            filepath (str): File path which will be created. (i.e. 'folder1/folder2/filename.txt')
            content (str): File content in string format.

        Returns:
            None
        '''
        data = StringIO.StringIO(content)
        self.resource.Bucket(bucket_name).put_object(Key=filepath, Body=data)


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
