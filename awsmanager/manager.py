# -*- coding: utf-8 -*-
from servicemanager import AwsServiceManager
from services import AwsBase
from modules import *

class AwsManager:

    @property
    def service(self):
        return self.aws

    def find_instance(self, filter_key, value):
        return ModuleFindElements().find_instance(self.aws, filter_key, value)

    def find_instances(self, filter_key, value):
        return ModuleFindElements().find_instances(self.aws, filter_key, value)

    def find_snapshot(self, filter_key, value):
        return ModuleFindElements().find_snapshot(self.aws, filter_key, value)

    def find_snapshots(self, filter_key, value):
        return ModuleFindElements().find_snapshots(self.aws, filter_key, value)

    def find_volume(self, filter_key, value):
        return ModuleFindElements().find_volume(self.aws, filter_key, value)

    def find_volumes(self, filter_key, value):
        return ModuleFindElements().find_volumes(self.aws, filter_key, value)



    def get_stats(self, region=None):
        return ModuleCommon().get_statistics(self.aws, region=region)

    def cost_savings(self):
        return ModuleCommon().cost_savings(self.aws)



    def get_balancer_by_domain(self, domain):
        return ModuleCommon().get_elb_by_domain(self.aws, domain)

    def get_ports_by_instance(self, instanceid):
        return ModuleCommon().get_instance_portlisting(self.aws, instanceid)

    def get_ports_by_region(self, region):
        return ModuleCommon().get_region_portlisting(self.aws, region)


    def __init__(self, region, access_key=None, secret_key=None, profile=None):
        self.aws = AwsServiceManager(region, access_key, secret_key, profile)



    # @property
    # def get_ports_by_region(self):
    #     return None
    #
