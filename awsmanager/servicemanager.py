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
        if AwsBase.profile:
            auth = {'Authorization': {'Type':'Profile', 'Value':AwsBase.profile}}
        elif AwsBase.access_key:
            auth = {'Authorization': {'Type':'AccessKeys', 'Value':AwsBase.access_key}}
        else:
            auth = {'Authorization': {'Type':'Profile', 'Value': 'default'}}
        return auth


    def __init__(self, region, profile=None, access_key=None, secret_key=None):
        # AwsBase.region - Region is shared between services
        AwsBase.region = region
        AwsBase.access_key = access_key
        AwsBase.secret_key = secret_key
        AwsBase.profile = profile
