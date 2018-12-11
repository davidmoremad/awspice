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
        config = self.get_client_vars()
        buckets = self.client.list_buckets()['Buckets']
        return self.inject_client_vars(buckets, config)


    def get_public_buckets(self):
        '''Get all public buckets and its permissions
        
        This method returns all buckets in an AWS Account which
        have public permissions to read, write, read acl, write acl or
        even full control.

        Returns:
            Buckets-ACL (list): List of dictionaries with the buckets requested
        '''
        results = []

        # https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html
        global_acl = 'http://acs.amazonaws.com/groups/global/AllUsers'

        def worker(bucket):
            try:
                bucket_result = {}
                bucket_acl = self.client.get_bucket_acl(Bucket=bucket['Name'])

                for grant in bucket_acl['Grants']:
                    if bucket['Name'] == 'hackforgood':print grant
                    if grant['Grantee']['Type'].lower() == 'group' \
                        and grant['Grantee']['URI'] == global_acl:
                        
                        if not bucket_result: bucket_result = bucket
                        bucket_result['Permissions'] = []
                        bucket_result['Permissions'].append(grant['Permission'])
                
                if bucket_result: results.append(bucket_result)

            # AccessDenied getting GetBucketAcl
            except ClientError: pass

        config = self.get_client_vars()

        for bucket in self.get_buckets(): self.pool.add_task(worker, bucket=bucket)
        self.pool.wait_completion()

        return self.inject_client_vars(results, config)

    def list_bucket_objects(self, bucket):
        '''List objects stored in a bucket
        
        Args:
            bucket (str): Name of the bucket
        
        Returns:
            list: List of bucket objects
        '''
        return self.client.list_objects(Bucket=bucket).get('Contents', [])
        



    def __init__(self):
        AwsBase.__init__(self, 's3')
