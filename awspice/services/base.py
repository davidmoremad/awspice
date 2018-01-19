# -*- coding: utf-8 -*-
import sys
import boto3

class AwsBase:

    region = None
    profile = None
    access_key = None
    secret_key = None



    def set_client(self, service, region, profile=None, access_key=None, secret_key=None):
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

    def set_auth_config(self, service, region, profile=None, access_key=None, secret_key=None):
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


    def inject_client_vars(self, elements):
        results = []
        for element in elements:
            element['RegionName'] = AwsBase.region
            if AwsBase.profile:
                element['Authorization'] = {'Type':'Profile', 'Value':AwsBase.profile}
            elif AwsBase.access_key and AwsBase.secret_key:
                element['Authorization'] = {'Type':'AccessKeys', 'Value':AwsBase.access_key}
            else:
                element['Authorization'] = {'Type':'Profile', 'Value': 'default'}
            results.append(element)
        return results

    def validate_filters(self, filter_key, filters_list):
        if filter_key not in filters_list:
            raise Exception('Invalid filter key. Allowed filters: ' + str(filters_list.keys()))


    # #################################
    # ------------ ACCOUNTS -----------
    # #################################

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

    def parse_accounts(self, accounts=[]):
        '''
        Parse strings or list of strings to dictionary with accounts.

        Args:
            accounts: List of regions to parse

        Returns:
            A list of accounts.
        '''
        results = list()
        if isinstance(accounts, str):
            if accounts == 'ALL':
                return self.get_accounts()
            else:
                return [accounts]

        if isinstance(accounts, list) and len(accounts) > 0:
            return accounts
        else:
            return [self.profile]



    # #################################
    # ------------ REGIONS ------------
    # #################################

    def get_regions(self):
        '''
        Get all available regions

        Returns:
            regions (dict): List of regions with 'Endpoint' & 'RegionName'.
        '''
        curService = self.service
        self.set_client('ec2', AwsBase.region)
        regions = self.client.describe_regions()['Regions']
        self.set_client(curService, AwsBase.region)
        return regions


    def change_region(self, region):
        '''
        Change region of the client keeping the service
        Args:
            region (str): Region ID of AWS              (i.e.: eu-central-1)
        '''
        AwsBase.region = region
        self.set_client(self.service, region=AwsBase.region)

    def parse_regions(self, regions=[], default_all=False):
        '''
        Parse strings or list of strings to dictionary with region format.

        Args:
            regions: List of regions to parse
            default_all: True to return all regions if region param is empty

        Returns:
            A list of formatted regions.
        '''
        results = list()
        if isinstance(regions, str):
            results = [{'RegionName':regions}]

        elif isinstance(regions, list) and len(regions) > 0:
            if isinstance(regions[0], dict): return regions
            for region in regions:
                results.append({'RegionName': region})
        else:
            results = self.get_regions() if default_all else [{'RegionName': AwsBase.region}]
        return results



    def __init__(self, service):
        self.set_client(service=service,
                        region=AwsBase.region,
                        access_key=AwsBase.access_key,
                        secret_key=AwsBase.secret_key,
                        profile=AwsBase.profile)
