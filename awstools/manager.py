# -*- coding: utf-8 -*-
from services import *
from services import AwsBase

class AwsManager:

    @property
    def ec2(self):
        return Ec2Manager(self.manager_access_key, self.manager_secret_key, self.manager_profile)

    @property
    def elb(self):
        return ElbManager(self.manager_access_key, self.manager_secret_key, self.manager_profile)

    @property
    def iam(self):
        return IamManager(self.manager_access_key, self.manager_secret_key, self.manager_profile)

    @property
    def rds(self):
        return RdsManager(self.manager_access_key, self.manager_secret_key, self.manager_profile)

    @property
    def s3(self):
        return S3Manager(self.manager_access_key, self.manager_secret_key, self.manager_profile)


    def __init__(self, region, access_key=None, secret_key=None, profile=None):
        # AwsBase.region - Region is shared between services
        AwsBase.region = region
        self.manager_access_key = access_key
        self.manager_secret_key = secret_key
        self.manager_profile = profile
