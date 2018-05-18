# -*- coding: utf-8 -*-
from services import *

class ServiceManager:
    '''
    Parent class that provides access to services.

    For each service (ec2, s3, vpc ...) you are given access through a property of this class.
    This property will return an instance of the corresponding class, for example Ec2Service or VpcService.
    Each class of service (Ec2Service, S3Service ...) inherits from the AwsBase class.
    '''

    _ec2 = None
    _elb = None
    _acm = None
    _iam = None
    _rds = None
    _s3 = None
    _ce = None

    @property
    def ec2(self):
        if self._ec2 is None: self._ec2 = Ec2Service()
        return self._ec2

    @property
    def elb(self):
        if self._elb is None: self._elb = ElbService()
        return self._elb

    @property
    def acm(self):
        if self._acm is None: self._acm = AcmService()
        return self._acm

    @property
    def iam(self):
        if self._iam is None: self._iam = IamService()
        return self._iam

    @property
    def rds(self):
        if self._rds is None: self._rds = RdsService()
        return self._rds

    @property
    def s3(self):
        if self._s3 is None: self._s3 = S3Service()
        return self._s3

    @property
    def ce(self):
        if self._ce is None: self._ce = CostExplorerService()
        return self._ce


    @classmethod
    def get_auth_config(cls):
        '''
        Get the configuration of the client currently configured

        This method allows us to work with multiple accounts and different authentication methods (keys and profiles) without getting lost.

        Returns:
            A dictionary with the type of authentication used and the associated value. The secret_key is not returned for security reasons.

            {'Authorization': {'Type': 'Profile', 'Value': 'MyBoringCompany'}}
        '''
        if AwsBase.profile:
            auth = {'Authorization': {'Type':'Profile', 'Value':AwsBase.profile}}
        elif AwsBase.access_key:
            auth = {'Authorization': {'Type':'AccessKeys', 'Value':AwsBase.access_key}}
        else:
            auth = {'Authorization': {'Type':'Profile', 'Value': 'default'}}
        return auth


    def __init__(self, region, profile=None, access_key=None, secret_key=None):
        '''
        Constructor of the parent class of the services.

        With this method you can modify the configuration of the awspice client.
        It allows us to change the profile, the region or the access codes.

        Args:
            region (str): Region in which to make queries and operations.
            profile (str): Name of the AWS profile set in ~/.aws/credentials file
            access_key (str): API access key of your AWS account
            secret_key (str): API secret key of your AWS account
        '''
        AwsBase.region = region
        AwsBase.access_key = access_key
        AwsBase.secret_key = secret_key
        AwsBase.profile = profile
