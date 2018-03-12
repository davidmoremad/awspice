# -*- coding: utf-8 -*-
import sys
import boto3

class AwsBase:
    '''
    Base class from which all services inherit (ec2, s3, vpc ...)

    This class contains methods and properties that are common to all AWS services and should
    be accessible by all of them. This class is responsible for instantiating the client and
    processing information related to the accounts and regions.

    Attributes:
        client: Boto3 client
        region: Current region used by the client
        profile: Current profile used by the client
        access_key: Current access key used by the client
        secret_key: Current secret key used by the client

    '''

    region = None
    profile = None
    access_key = None
    secret_key = None


    def set_client(self, service, region, profile=None, access_key=None, secret_key=None):
        '''
        Main method to set Boto3 client

        Args:
            service (str): Service to use    (i.e.: ec2, s3, vpc...)
            region (str): Region name to use (i.e.: eu-central-1)
            profile (str): Profile name set in ~/.aws/credentials file
            access_key (str): API access key of your AWS account
            secret_key (str): API secret key of your AWS account

        Raises:
            ClientError: Access keys are not valid or lack of permissions for a service/region
            ProfileNotFound: Profile name not found in credentials file

        Returns:
            None
        '''
        self.set_auth_config(service=service,
                             region=region,
                             profile=profile,
                             access_key=access_key,
                             secret_key=secret_key)

        if AwsBase.profile:
            self.client = boto3.Session(profile_name=AwsBase.profile).client(service,
                                                                        region_name=AwsBase.region)
        elif AwsBase.access_key and AwsBase.secret_key:
            self.client = boto3.client(service,
                                        region_name=AwsBase.region,
                                        aws_access_key_id=AwsBase.access_key,
                                        aws_secret_access_key=AwsBase.secret_key)
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
        AwsBase.region = region

        if profile and (access_key or secret_key):
            auth_error = 'Use Profile or Access keys, not both.'
            print '[!] %s' % auth_error
            raise ValueError(auth_error)
            sys.exit(0)

        if profile:
            AwsBase.profile = profile
            AwsBase.access_key = None
            AwsBase.secret_key = None
        elif access_key and secret_key:
            AwsBase.profile = None
            AwsBase.access_key = access_key
            AwsBase.secret_key = secret_key

    @classmethod
    def inject_client_vars(self, elements):
        '''
        Insert in each item of a list, the region and the current credentials.

        This function is called by all the methods of all the services that return a list of objects
        to identify in what region and account they have been found.

        Args:
            elements (list): List of dictionaries

        Returns:
            list. Returns same list with the updated elements (region and authentication included)

        '''
        results = []
        for element in elements:
            elements_tag_name = filter(lambda x: x['Key'] == 'Name', element.get('Tags',''))
            element['TagName'] = next(iter(map(lambda x: x.get('Value', ''), elements_tag_name)), '')
            element['RegionName'] = AwsBase.region
            if AwsBase.profile:
                element['Authorization'] = {'Type':'Profile', 'Value':AwsBase.profile}
            elif AwsBase.access_key and AwsBase.secret_key:
                element['Authorization'] = {'Type':'AccessKeys', 'Value':AwsBase.access_key}
            else:
                element['Authorization'] = {'Type':'Profile', 'Value': 'default'}
            results.append(element)
        return results

    @classmethod
    def validate_filters(self, filter_key, filters_list):
        '''
        Validate that an item is within a list

        Args:
            filter_key (str): Item to validate
            filters_list (list): Pre-validated list

        Returns:
            None

        Raises:
            ValueError: Filter is not in the accepted filter list
        '''
        if filter_key not in filters_list:
            raise ValueError('Invalid filter key. Allowed filters: ' + str(filters_list.keys()))


    # #################################
    # ------------ PROFILES -----------
    # #################################

    @classmethod
    def get_profiles(self):
        '''
        Get a list of all available profiles in ~/.aws/credentials file

        Returns:
            list. List of strings with available profiles
        '''
        return boto3.Session().available_profiles

    def change_profile(self, profile):
        '''
        Change profile of the client

        This method changes the account/profile used but keeps the same region and service

        Args:
            profile (str): Name of the profile set in ~/.aws/credentials file

        Examples:
            $ aws = awspice.connect()
            $ aws.service.ec2.change_profile('my_boring_company')

        Returns:
            None
        '''
        AwsBase.profile = profile
        self.set_client(self.service, region=AwsBase.region, profile=AwsBase.profile)

    def parse_profiles(self, profiles=[]):
        '''
        Validation method which get a profile or profile list and return the expected list of them

        The purpose of this method is that a user can pass different types of data as a "profile"
        argument and obtain a valid output for any method that works with this type of data.

        Args:
            profiles (list | str): String or list of string to parse

        Examples:
            $ account_str = aws.service.ec2.parse_profiles('my_company')
            $ account_lst = aws.service.ec2.parse_profiles(['my_company'])
            $ accounts_lst = aws.service.ec2.parse_profiles(['my_company', 'other_company'])

        Returns:
            list. List of a strings with profile names
        '''
        if isinstance(profiles, str):
            if profiles == 'ALL':
                return self.get_profiles()
            return [profiles]

        if isinstance(profiles, list) and profiles:
            return profiles
        return [self.profile]


    # #################################
    # ------------ REGIONS ------------
    # #################################

    def get_regions(self):
        '''
        Get all available regions

        Returns:
            list. List of regions with 'Endpoint' and 'RegionName'
        '''
        currentService = self.service
        self.set_client('ec2', AwsBase.region)
        regions = self.client.describe_regions()['Regions']
        self.set_client(currentService, AwsBase.region)
        return regions

    def change_region(self, region):
        '''
        Change region of the client

        This method changes the region used but keeps the same service and profile

        Args:
            region (str): Region Name (ID) of AWS (i.e.: eu-central-1)

        Examples:
            aws.service.ec2.change_region('eu-west-1')

        Returns:
            None
        '''
        AwsBase.region = region
        self.set_client(self.service, region=AwsBase.region)

    def parse_regions(self, regions=[], default_all=False):
        '''
        Validation method which get a region or list of regions and return the expected list of them

        The purpose of this method is that a user can pass different types of data as a "region"
        argument and obtain a valid output for any method that works with this type of data.

        Args:
            regions (list | str): String or list of string to parse
            default_all (bool): If the list of regions is empty and this argument is True,
                                a list with all regions will be returned. This is useful when you do
                                not know the data entry of type "region" and you want to search by
                                default in all regions (if regions are empty means that the user
                                does not know where an element is located).

        Examples:
            regions = aws.service.ec2.parse_regions('eu-west-1')
            regions = aws.service.ec2.parse_regions(['eu-west-1'])
            regions = aws.service.ec2.parse_regions(['eu-west-1', 'eu-west-2'])

        Returns:
            list. List of a strings with profile names
        '''
        results = list()
        if isinstance(regions, str):
            results = [{'RegionName':regions}]

        elif isinstance(regions, list) and regions:
            if isinstance(regions[0], dict):
                return regions
            for region in regions:
                results.append({'RegionName': region})
        else:
            results = self.get_regions() if default_all else [{'RegionName': AwsBase.region}]
        return results


    def __init__(self, service):
        '''
        This constructor configures the corresponding service according to the class that calls it.

        Every time the EC2Service Class is called (inherits from this class), this constructor will
        change the client's service to 'ec2'. And then, if ELBService service is called, this method
        is called again changing the service from 'ec2' to 'elb'.

        Args:
            service (str): AWS service to uso

        Returns:
            None
        '''
        self.service = service
        self.set_client(service=service,
                        region=AwsBase.region,
                        access_key=AwsBase.access_key,
                        secret_key=AwsBase.secret_key,
                        profile=AwsBase.profile)
