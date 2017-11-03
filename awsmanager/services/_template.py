# -*- coding: utf-8 -*-
from base import AwsBase

class Ec2Manager(AwsBase)

    def get_elements(self):
        try:
            return self.get_regions()
        except:
            return False

    def __init__(self, access_key, secret_key, profile):
        AwsBase.__init__(self, 'ec2', access_key, secret_key, profile)
