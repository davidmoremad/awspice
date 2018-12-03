# -*- coding: utf-8 -*-
import json
import boto3
from awspice.helpers import ThreadPool
from pkg_resources import resource_filename

class AwsBase(object):
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
    endpoints = None
    region = None
    profile = None
    access_key = None
    secret_key = None

    # THREADS NUMBER
    pool = ThreadPool(30)

    service_resources = ['ec2', 's3']


    def set_client(self, service):
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
        _region = str(AwsBase.region)
        _profile = str(AwsBase.profile) if AwsBase.profile else None
        _access_key = str(AwsBase.access_key) if AwsBase.access_key else None
        _secret_key = str(AwsBase.secret_key) if AwsBase.secret_key else None

        # 1. Validate args for authentication
        self.set_auth_config(region=_region,
                             profile=_profile,
                             access_key=_access_key,
                             secret_key=_secret_key)
        # 2. Set Boto3 client
        if _profile:
            self.client = boto3.Session(profile_name=_profile).client(service, region_name=_region)
            if service in self.service_resources:
                self.resource = boto3.Session(profile_name=_profile).resource(
                    service, region_name=_region)

        elif _access_key and _secret_key:
            self.client = boto3.client(service,
                                    region_name=_region,
                                    aws_access_key_id=_access_key,
                                    aws_secret_access_key=_secret_key)
            if service in self.service_resources:
                self.resource = boto3.resource(service,
                                            region_name=_region,
                                            aws_access_key_id=_access_key,
                                            aws_secret_access_key=_secret_key)
        # If auth isn't provided, set "default" profile (.aws/credentials)
        else:
            self.client = boto3.client(service, region_name=_region)
            if service in self.service_resources:
                self.resource = boto3.resource(service, region_name=_region)

    @classmethod
    def set_auth_config(cls, region, profile=None, access_key=None, secret_key=None):
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
            raise ValueError('Use Profile or Access keys, not both.')

        if profile:
            AwsBase.profile = profile
            AwsBase.access_key = None
            AwsBase.secret_key = None
        elif access_key and secret_key:
            AwsBase.profile = None
            AwsBase.access_key = access_key
            AwsBase.secret_key = secret_key

    @classmethod
    def get_client_vars(cls):
        '''Get information of the current client configuration
        Sometimes we need to store this variables, for example using threads, 
        because AwsBase is constantly changing 
        
        Returns:
            dict: Array with current client configuration ({'region': 'eu-west-1', 'profile': 'default'})
        '''

        _region_name = str(AwsBase.region)
        _region = dict(AwsBase.endpoints['Regions'][_region_name], RegionName=_region_name)
        _profile = str(AwsBase.profile)
        _access_key = str(AwsBase.access_key)

        return {'region': _region, 'profile': _profile, 'access_key': _access_key}



    @classmethod
    def inject_client_vars(cls, elements, client_conf=None):
        '''
        Insert in each item of a list, the region and the current credentials.

        This function is called by all the methods of all the services that return a list of objects
        to identify in what region and account they have been found.

        Args:
            elements (list): List of dictionaries
            client_conf (dict): Array with the client configuration (see `get_client_vars`)

        Returns:
            list. Returns same list with the updated elements (region and authentication included)

        '''

        # [!] used dict() to avoid to rewrite object AwsBase in next line
        if client_conf:
            _region_name = client_conf['region']['RegionName']
            _region_dict = client_conf['region']
            _profile =     client_conf['profile']
            _access_key =  client_conf['access_key']
        else:
            _region_name = str(AwsBase.region)
            _region_dict = dict(AwsBase.endpoints['Regions'][_region_name])
            _profile =     str(AwsBase.profile)
            _access_key =  str(AwsBase.access_key)
            _region_dict['RegionName'] = _region_name
        results = []

        for element in elements:

            if element.get('Authorization') and element.get('RegionName'):
                break
                
            elements_tagname = filter(lambda x: x['Key'] == 'Name', element.get('Tags', ''))
            element['TagName'] = next(iter(map(lambda x: x.get('Value', ''), elements_tagname)), '')
            element['Region'] = _region_dict

            if _profile:
                element['Authorization'] = {'Type':'Profile', 'Value': _profile}
            elif _access_key:
                element['Authorization'] = {'Type':'AccessKeys', 'Value': _access_key}
            else:
                element['Authorization'] = {'Type':'Profile', 'Value': 'default'}

            results.append(element)

        return results

    def region_in_regions(self, region, regions):
        '''
        Check if region is in a complex list of regions

        Args:
            region (str | lst) - Region name or parsed region format {'RegionName': 'eu-west-1'}
            regions (lst) - List of strings or dicts of regions

        Examples:
            region_in_regions('eu-west-1', [{'RegionName': 'eu-west-1}])

        Returns:
            bool
        '''
        return self.parse_regions(region)[0] in self.parse_regions(regions)

    @classmethod
    def validate_filters(cls, filter_key, filters_list):
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
    def get_profiles(cls):
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
        if profile != AwsBase.profile:
            AwsBase.profile = profile
            self.set_client(self.service)

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

    @classmethod
    def _load_endpoints(cls):
        '''
        Get AWS-Standard partition of endpoints.json file (botocore)

        Returns:
            dict: AWS-Standard partition
        '''
        if AwsBase.endpoints == None:
            # Load endpoints file
            endpoint_resource = resource_filename('botocore', 'data/endpoints.json')
            with open(endpoint_resource, 'r') as f:
                endpoints = json.load(f)

            # Get regions for "AWS Standard" (Not Gov, China)
            partitions = filter(lambda x: x['partitionName'] == "AWS Standard",
                                endpoints['partitions'])[0]

            # Format JSON & Save
            results = dict()
            results['Regions'] = dict()
            results['Services'] = partitions['services']
            results['Defaults'] = partitions['defaults']
            results['DnsSuffix'] = partitions['dnsSuffix']
            for k, v in partitions['regions'].iteritems():
                desc = v['description']
                results['Regions'][k] = {"Description": desc,
                                         "Country": desc[desc.find("(")+1:desc.find(")")]}
            AwsBase.endpoints = results

        return AwsBase.endpoints


    def get_endpoints(self):
        '''
        Get services and its regions and endpoints

        Returns:
            dict: Dict with services (key) and its regions and Endpoints.
        '''
        partition = self._load_endpoints()
        dns_suffix = partition['DnsSuffix']
        default_url = partition['Defaults']['hostname']

        # Return as list
        results = dict()
        for k, v in partition['Services'].iteritems():
            url = v.get('Defaults', {}).get('hostname', default_url)
            results[k] = {
                'Regions': v['endpoints'].keys(),
                'Endpoints': [url.format(service=k, region=region, dnsSuffix=dns_suffix) for region in v['endpoints'].keys()],
            }
        return results

    def get_regions(self):
        '''
        Get all available regions

        Returns:
            list. List of regions with 'Country' and 'RegionName'
        '''
        return self._load_endpoints()['Regions']

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
        self.set_client(self.service)

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
            AwsBase.region = aws.service.ec2.parse_regions([])
            regions = aws.service.ec2.parse_regions('eu-west-1')
            regions = aws.service.ec2.parse_regions(['eu-west-1'])
            regions = aws.service.ec2.parse_regions(['eu-west-1', 'eu-west-2'])

        Returns:
            list. List of a strings with profile names
        '''
        results = list()

        # regions = 'eu-west-1'
        if isinstance(regions, str):
            results = [{'RegionName':regions}]

        # regions = ['eu-west-1'] or [u'eu-west-1'] or [{'RegionName': 'eu-west-1}]
        elif isinstance(regions, list) and regions:
            if isinstance(regions[0], dict) and regions[0].get('RegionName', False):
                return regions
            elif isinstance(regions[0], basestring):
                [results.append({'RegionName': region}) for region in set(regions)]
            else:
                raise ValueError('Invalid regions value.')

        # regions = {'eu-west-1': {...}, 'eu-central-1' : {...} }  <--- AwsBase.endpoints['Regions']
        elif isinstance(regions, dict) and regions:
            if regions.get('eu-west-1', False):
                [results.append({'RegionName': region}) for region in regions.keys()]
            else:
                raise ValueError('Invalid regions value.')

        # regions = None <--- Get current or all regions
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
        self.set_client(service=service)
        self._load_endpoints()

