# -*- coding: utf-8 -*-
from servicemanager import AwsServiceManager
from services import AwsBase
from modules import *

class AwsManager:

    @property
    def service(self):
        return self.aws


    @property
    def finder(self):
        return ModuleFinder(self.aws)

    @property
    def security(self):
        return ModuleSecurity(self.aws)

    @property
    def stats(self):
        return ModuleStats(self.aws)

    @property
    def common(self):
        return ModuleCommon(self.aws)


    def __init__(self, region, profile=None, access_key=None, secret_key=None):
        self.aws = AwsServiceManager(region, profile, access_key, secret_key)
