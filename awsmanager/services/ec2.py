# -*- coding: utf-8 -*-
from base import AwsBase

class Ec2Service(AwsBase):

    instance_filters = {
        'id': 'instance-id',
        'dnsname': 'dns-name',
        'publicip': 'network-interface.association.public-ip',
        'privateip': 'private-ip-address',
        'name': 'tag:Name',
        'tagname': 'tag:Name',
        'status': 'instance-state-name',
        'user': 'key-name',
    }

    snapshot_filters = {
        'id': 'snapshot-id',
        'status': 'status',
    }

    volume_filters = {
        'id': 'volume-id',
        'status': 'status',
    }

    secgroup_filters = {
        'id': 'group-id',
        'description': 'description',
    }

    address_filters = {
        'publicip': 'public-ip',
    }


    # #################################
    # ------------ REGIONS ------------
    # #################################

    def get_regions(self):
        '''
        Get all available regions

        Returns:
            regions (dict): List of regions with 'Endpoint' & 'RegionName'.
        '''
        regions = self.client.describe_regions()['Regions']
        return regions



    # #################################
    # ----------- INSTANCES -----------
    # #################################

    def _extract_instances(self, filters=[], region_switch=False, return_first=False):
        results = list()

        regions = self.get_regions() if region_switch else [{'RegionName': AwsBase.region}]
        for region in regions:
            self.change_region(region['RegionName'])

            reservations = self.client.describe_instances(Filters=filters)["Reservations"]
            for reserv in reservations:
                instances = self.inject_region(reserv['Instances'])
                if return_first and instances: return instances[0]
                results.extend(instances)

        return results

    def get_instances(self, region_switch=False):
        '''
        Get all instances for a region

        Returns:
            List of dictionaries with all instances
        '''
        return self._extract_instances(region_switch=region_switch)

    def get_instance_by(self, filter_key, filter_value, region_switch=False):
        '''
        Get an instance for a region that matches with filter

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter

        Return:
            Instance that matches with filters
        '''
        if filter_key not in self.instance_filters:
            raise Exception('Invalid filter key. Allowed filters: ' + str(self.instance_filters.keys()))

        filters = [{
            'Name': self.instance_filters[filter_key],
            'Values': [filter_value]
        }]

        return self._extract_instances(filters=filters, region_switch=region_switch, return_first=True)

    def get_instances_by(self, filter_key, filter_value, region_switch=False):
        '''
        Get all instances for a region using filters

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter

        Return:
            List of dictionaries with all instances that matches
        '''
        if filter_key not in self.instance_filters:
            raise Exception('Invalid filter key. Allowed filters: ' + str(self.instance_filters.keys()))

        filters = [{
            'Name': self.instance_filters[filter_key],
            'Values': [filter_value]
        }]

        return self._extract_instances(filters=filters, region_switch=region_switch)



    # #################################
    # ------------ VOLUMES ------------
    # #################################

    def get_volumes(self):
        '''
        Get all volumes for a region

        Returns:
            List of dictionaries with all volumes
        '''
        return self.inject_region(self.client.describe_volumes()['Volumes'])

    def get_volumes_by(self, filter_key, filter_value):
        if filter_key in self.volume_filters:
            filters = [{
                'Name': self.volume_filters[filter_key],
                'Values': [filter_value]
            }]
            return  self.inject_region(self.client.describe_volumes(Filters=filters)['Volumes'])

        else:
            return Exception('Invalid filter key. Allowed filters: ' + str(self.volume_filters.keys()))



    # #################################
    # ------------ SNAPSHOTS ------------
    # #################################

    def get_snapshots(self):
        '''
        Get all snapshots owned by self for a region

        Returns:
            List of dictionaries with snapshots
        '''
        return self.inject_region(self.client.describe_snapshots(OwnerIds=['self'])['Snapshots'])

    def get_snapshot_by(self, filter_key, filter_value):
        '''
        Get a snapshot for a region using filters

        Returns:
            Dictionary with snapshot that matches
        '''
        snapshots = self.get_snapshots_by(filter_key, filter_value)
        if snapshots and len(snapshots) > 0:
            return snapshots[0]
        else:
            return None

    def get_snapshots_by(self, filter_key, filter_value):
        '''
        Get all snapshots for a region using filters

        Returns:
            List of dictionaries with snapshots that matches
        '''
        if filter_key in self.snapshot_filters:
            filters = [{
                'Name': self.snapshot_filters[filter_key],
                'Values': [filter_value]
            }]
            return self.inject_region(self.client.describe_snapshots(Filters=filters)['Snapshots'])
        else:
            raise Exception('Invalid filter key. Allowed filters: ' + str(self.snapshot_filters.keys()))



    # #################################
    # ------------ SEC. GROUPS ------------
    # #################################

    def get_secgroups(self):
        '''
        Get all security groups for a region

        Returns:
            list of dictionaries with SecurityGroups.
        '''
        return self.inject_region(self.client.describe_security_groups()['SecurityGroups'])

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
        if filter_key in self.secgroup_filters:
            filters = [{
                'Name': self.secgroup_filters[filter_key],
                'Values': [filter_value]
            }]
            return self.inject_region(self.client.describe_security_groups(Filters=filters)['SecurityGroups'])
        else:
            raise Exception('Invalid filter key. Allowed filters: ' + str(self.secgroup_filters.keys()))



    # #################################
    # ------------ ADDRESSES ------------
    # #################################

    def get_addresses(self):
        '''
        Get all IP Addresses for a region

        Returns:
            list of dictionaries with all addresses
        '''
        return self.inject_region(self.client.describe_addresses()['Addresses'])

    def get_addresses_by(self, filter_key, filter_value):
        '''
        Get all IP Addresses for a region

        Returns:
            list of dictionaries with all addresses
        '''
        if filter_key in self.address_filters:
            filters = [{
                'Name': self.address_filters[filter_key],
                'Values': [filter_value]
            }]
            return self.inject_region(self.client.describe_addresses(Filters=filters)['Addresses'])
        else:
            raise Exception('Invalid filter key. Allowed filters: ' + str(self.address_filters.keys()))



    # #################################
    # ------------ VPC ------------
    # #################################

    def get_vpcs(self):
        '''
        Get all VPCs for a region

        Returns:
            List of dictionaries with all VPCs
        '''
        return self.inject_region(self.client.describe_vpcs()['Vpcs'])

    def __init__(self):
        AwsBase.__init__(self, 'ec2')
