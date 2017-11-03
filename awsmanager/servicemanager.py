# -*- coding: utf-8 -*-
from services import *

class AwsServiceManager:

    @property
    def ec2(self): return Ec2Service()

    @property
    def elb(self): return ElbService()

    @property
    def acm(self): return AcmService()

    @property
    def iam(self): return IamService()

    @property
    def rds(self): return RdsService()

    @property
    def s3(self): return S3Service()



    def get_auth_config(self):
        auth = {'AccessKey': AwsBase.access_key,
                'SecretKey': AwsBase.access_key,
                'Profile': AwsBase.profile}
        return auth


    def __init__(self, region, access_key=None, secret_key=None, profile=None):
        # AwsBase.region - Region is shared between services
        AwsBase.region = region
        AwsBase.access_key = access_key
        AwsBase.secret_key = secret_key
        AwsBase.profile = profile
