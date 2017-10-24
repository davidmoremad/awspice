# -*- coding: utf-8 -*-
import sys
import boto3
from botocore.exceptions import ProfileNotFound

class AwsBase:

    region = None

    def set_client(self, service, region, access_key=None, secret_key=None, profile=None):
        '''
        Main method to set Boto3 client.
        Args:
            service (str): Service to use               (i.e.: ec2, s3, vpc...)
            region (str): Region name                   (i.e.: eu-central-1)
            access_key (str): API Access key
            secret_key (str): API Secret key
            profile (str): Profile name set in ~/.aws/credentials file

        Raises:
            ClientError: Invalid Access keys
            ProfileNotFound: Profile name not found in credentials file
        '''
        self.service = service
        AwsBase.region = region

        if (profile and access_key) or (profile and secret_key):
            print '[!] Use Profile or Access keys, not both.'
            sys.exit(0)

        if profile:
            self.client = boto3.Session(profile_name=profile).client(service, region_name=AwsBase.region)
        elif (access_key and secret_key):
            self.client = boto3.client( service,
                                        region_name=AwsBase.region,
                                        aws_access_key_id=access_key,
                                        aws_secret_access_key=secret_key)
        else:
            self.client = boto3.client(service, region_name=AwsBase.region)


    def change_region(self, region):
        '''
        Change region of the client keeping the service
        Args:
            region (str): Region ID of AWS              (i.e.: eu-central-1)
        '''
        AwsBase.region = region
        self.set_client(self.service, region=AwsBase.region)

    def __init__(self, service, access_key=None, secret_key=None, profile=None):
        self.set_client(service=service,
                        region=AwsBase.region,
                        access_key=access_key,
                        secret_key=secret_key,
                        profile=profile)
