# -*- coding: utf-8 -*-
from base import AwsBase

class Ec2Manager(AwsBase):


    # ------------ REGIONS ------------

    def get_regions(self):
        '''
        Get all available regions

        Returns:
            regions (dict): List of regions with 'Endpoint' & 'RegionName'.
        '''
        regions = self.client.describe_regions()['Regions']
        return regions

    # ------------ INSTANCES ------------

    def get_all_instances(self):
        '''
        Get all instances of all regions

        Return:
            List of arrays with all instances
        '''
        instance_list = []

        for aws_region in self.get_regions():
            self.change_region('ec2', aws_region['RegionName'])
            instance_list.extend(self.get_instances())

        return instance_list

    def get_all_instances_by(self, filter_key, filter_value):
        '''
        Get all instances of all region using filters

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter

        Return:
            List of arrays with all instances that matches
        '''
        instance_list = []

        for aws_region in self.get_regions():
            self.change_region('ec2', aws_region['RegionName'])
            instance_list.extend(self.get_instances_by(filter_key, filter_value))

        return instance_list

    def get_instances(self):
        '''
        Get all instances for a region

        Returns:
            List of arrays with all instances
        '''
        reservations =  self.client.describe_instances()

        instance_list = []
        for reserv in reservations["Reservations"]:
            for instance in reserv['Instances']:
                instance_list.append(instance)

        return instance_list

    def get_instance_by(self, filter_key, filter_value):
        '''
        Get an instance for a region that matches with filter

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter

        Return:
            Instance that matches with filters
        '''
        result = self.get_instances_by(filter_key, filter_value)
        if len(result) > 0:
            return result[0]
        else:
            return None

    def get_instances_by(self, filter_key, filter_value):
        '''
        Get all instances for a region using filters

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter

        Return:
            List of arrays with all instances that matches
        '''
        dict_filters = {
            'id': 'instance-id',
            'dnsname': 'dns-name',
            'publicip': 'network-interface.association.public-ip',
            'privateip': 'private-ip-address',
            'tagname': 'tag:Name',
            'status': 'instance-state-name',
            'user': 'owner-id',
        }

        if filter_key in dict_filters:
            filters = [{
                'Name': dict_filters[filter_key],
                'Values': [filter_value]
            }]

            instance_list = []
            for reservation in self.client.describe_instances(Filters=filters)["Reservations"]:
                for instance in reservation['Instances']:
                    instance_list.append(instance)
            return instance_list
        else:
            return None

    # ------------ VOLUMES ------------

    def get_volumes(self):
        '''
        Get all volumes for a region

        Returns:
            List of arrays with all volumes
        '''
        return self.client.describe_volumes()['Volumes']

    def get_volumes_by(self, filter_key, filter_value):
        dict_filters = {
            'status': 'status',
        }

        if filter_key in dict_filters:
            filters = [{
                'Name': dict_filters[filter_key],
                'Values': [filter_value]
            }]
            return self.client.describe_volumes(Filters=filters)['Volumes']
        else:
            return None

    # ------------ ADDRESSES ------------

    def get_addresses(self):
        '''
        Get all IP Addresses for a region

        Returns:
            list of arrays with all addresses
        '''
        return self.client.describe_addresses()['Addresses']

    # ------------ SEC. GROUPS ------------

    def get_secgroups(self):
        '''
        Get all security groups for a region

        Returns:
            list of arrays with SecurityGroups.
        '''
        return self.client.describe_security_groups()['SecurityGroups']

    def get_secgroup_by(self, filter_key, filter_value):
        '''
        Get security group for a region that matches with filters

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter

        Returns:
            First Security group that matches with filters
        '''
        result = self.get_secgroups_by(filter_key, filter_value)
        if len(result) > 0:
            return result[0]
        else:
            return None

    def get_secgroups_by(self, filter_key, filter_value):
        '''
        Get all security groups for a region that matches with filters

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter

        Returns:
            All Security group that matches with filters
        '''
        dict_filters = {
            'id': 'group-id',
            'description': 'description',
            'owner': 'owner-id',
        }

        if filter_key in dict_filters:
            filters = [{
                'Name': dict_filters[filter_key],
                'Values': [filter_value]
            }]
            return self.client.describe_security_groups(Filters=filters)['SecurityGroups']
        else:
            return None

    def __init__(self, access_key, secret_key, profile):
        AwsBase.__init__(self, 'ec2', access_key, secret_key, profile)
