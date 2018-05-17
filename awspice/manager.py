# -*- coding: utf-8 -*-
from servicemanager import ServiceManager
from modules import *
from botocore.exceptions import ProfileNotFound, ClientError


class AwsManager:
    """
    Main class that provides access to services (ec2, s3, vpc ...) and modules (finder, stats ..)

    This master class provides access to individual services through the "services" property,
    and also to other complex modules such as "finder", "stats" and "security".

    Attributes:
        aws: Object of type #ServiceManager that provides access to the other services.
    """

    @property
    def service(self):
        return self.aws

    @property
    def finder(self):
        return FinderModule(self.aws)

    @property
    def security(self):
        return SecurityModule(self.aws)

    @property
    def stats(self):
        return StatsModule(self.aws)


    def test(self):
        """
        Method to verify that the loaded configuration is correct and access with the AWS API is correct

        Returns:
            boolean. True if the test was successful, false if it failed.
        """
        try:
            self.aws.ec2.get_regions()
            print('[OK] Your awspice is ready to give a helping hand :)')
            return True
        except ProfileNotFound:
            print('[!] You type like a lame pigeon. Profile not found in ~/.aws/credentials file')
            return False
        except ClientError:
            print('[!] Was it so difficult to copy and paste? Invalid credentials. Verify your access keys or permissions for that IAM user')
            return False


    def __init__(self, region='eu-west-1', profile=None, access_key=None, secret_key=None):
        '''
        Initialization and configuration of the client

        Args:
            region (str): Region in which to make queries and operations.
            profile (str): Name of the AWS profile set in ~/.aws/credentials file
            access_key (str): API access key of your AWS account
            secret_key (str): API secret key of your AWS account

        Returns:
            None

        '''
        self.aws = ServiceManager(region, profile=profile, access_key=access_key, secret_key=secret_key)
