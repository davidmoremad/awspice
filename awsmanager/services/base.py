# -*- coding: utf-8 -*-
import sys
import boto3

class AwsBase:

    region = None
    profile = None
    access_key = None
    secret_key = None

    def set_auth_config(self, service, region, access_key=None, secret_key=None, profile=None):
        '''
        Set properties like service, region or auth method to be used by boto3 client
        Args:
            service (str): Service to use               (i.e.: ec2, s3, vpc...)
            region (str): Region name                   (i.e.: eu-central-1)
            access_key (str): API Access key
            secret_key (str): API Secret key
            profile (str): Profile name set in ~/.aws/credentials file
        '''
        self.service = service
        AwsBase.region = region

        if profile and (access_key or secret_key):
            print '[!] Use Profile or Access keys, not both.'
            sys.exit(0)

        if profile:
            AwsBase.profile = profile
            AwsBase.access_key = None
            AwsBase.secret_key = None
        elif access_key and secret_key:
            AwsBase.profile = None
            AwsBase.access_key = access_key
            AwsBase.secret_key = secret_key



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
        self.set_auth_config(service, region, access_key, secret_key, profile)

        if AwsBase.profile:
            self.client = boto3.Session(profile_name=AwsBase.profile).client(service, region_name=AwsBase.region)
        elif (AwsBase.access_key and AwsBase.secret_key):
            self.client = boto3.client( service, region_name=AwsBase.region, aws_access_key_id=AwsBase.access_key, aws_secret_access_key=AwsBase.secret_key)
        else:
            self.client = boto3.client(service, region_name=AwsBase.region)


    def inject_region(self, elements):
        results = []
        for element in elements:
            element['RegionName'] = AwsBase.region
            if AwsBase.profile:
                element['Authorization'] = {'Type':'Profile', 'Value':AwsBase.profile}
            elif AwsBase.access_key and AwsBase.secret_key:
                element['Authorization'] = {'Type':'AccessKeys', 'Value':AwsBase.access_key}
            results.append(element)
        return results


    def get_accounts(self):
        '''
        Get a list of all available accounts
        Args:
            account (str): Profile name              (i.e.: account01)
        '''
        return boto3.Session().available_profiles


    def change_account(self, account):
        '''
        Change account of the client keeping the region
        Args:
            account (str): Profile name              (i.e.: account01)
        '''
        AwsBase.profile = account
        self.set_client(self.service, region=AwsBase.region, profile=AwsBase.profile)


    def change_region(self, region):
        '''
        Change region of the client keeping the service
        Args:
            region (str): Region ID of AWS              (i.e.: eu-central-1)
        '''
        AwsBase.region = region
        self.set_client(self.service, region=AwsBase.region)

    def __init__(self, service):
        self.set_client(service=service,
                        region=AwsBase.region,
                        access_key=AwsBase.access_key,
                        secret_key=AwsBase.secret_key,
                        profile=AwsBase.profile)
