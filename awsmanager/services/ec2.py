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
    # ----------- INSTANCES -----------
    # #################################

    def _extract_instances(self, filters=[], regions=[], return_first=False):
        results = list()

        regions = self.parse_regions(regions)
        for region in regions:
            self.change_region(region['RegionName'])

            reservations = self.client.describe_instances(Filters=filters)["Reservations"]
            for reserv in reservations:
                instances = self.inject_client_vars(reserv['Instances'])
                if return_first and instances: return instances[0]
                results.extend(instances)

        return results

    def get_instances(self, regions=[]):
        '''
        Get all instances for a region

        Returns:
            List of dictionaries with all instances
        '''
        return self._extract_instances(regions=regions)

    def get_instance_by(self, filter_key, filter_value, regions=[]):
        '''
        Get an instance for a region that matches with filter

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter

        Return:
            Instance that matches with filters
        '''
        return self.get_instances_by(filter_key, filter_value, regions, return_first=True)

    def get_instances_by(self, filter_key, filter_value, regions=[], return_first=False):
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

        return self._extract_instances(filters=filters, regions=regions, return_first=return_first)



    # #################################
    # ------------ VOLUMES ------------
    # #################################

    def _extract_volumes(self, filters=[], regions=[], return_first=False):
        results = list()

        regions = self.parse_regions(regions)
        for region in regions:
            self.change_region(region['RegionName'])

            volumes = self.client.describe_volumes(Filters=filters)['Volumes']
            volumes = self.inject_client_vars(volumes)
            if return_first and len(volumes) > 0: return volumes[0]
            results.extend(volumes)

        return results

    def get_volumes(self, regions=[]):
        '''
        Get all volumes for a region

        Returns:
            List of dictionaries with all volumes
        '''
        return self._extract_volumes(region_switch=region_switch)

    def get_volume_by(self, filter_key, filter_value, regions=[]):
        return self.get_volumes_by(filter_key, filter_value, regions, return_first=True)

    def get_volumes_by(self, filter_key, filter_value, regions=[], return_first=False):

        if filter_key not in self.instance_filters:
            raise Exception('Invalid filter key. Allowed filters: ' + str(self.instance_filters.keys()))

        filters = [{
            'Name': self.volume_filters[filter_key],
            'Values': [filter_value]
        }]

        return self._extract_volumes(filters=filters, regions=regions, return_first=return_first)




    # #################################
    # ------------ SNAPSHOTS ------------
    # #################################

    def get_snapshots(self):
        '''
        Get all snapshots owned by self for a region

        Returns:
            List of dictionaries with snapshots
        '''
        return self.inject_client_vars(self.client.describe_snapshots(OwnerIds=['self'])['Snapshots'])

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
            return self.inject_client_vars(self.client.describe_snapshots(Filters=filters)['Snapshots'])
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
        return self.inject_client_vars(self.client.describe_security_groups()['SecurityGroups'])

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
            return self.inject_client_vars(self.client.describe_security_groups(Filters=filters)['SecurityGroups'])
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
        return self.inject_client_vars(self.client.describe_addresses()['Addresses'])

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
            return self.inject_client_vars(self.client.describe_addresses(Filters=filters)['Addresses'])
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
        return self.inject_client_vars(self.client.describe_vpcs()['Vpcs'])

    def __init__(self):
        AwsBase.__init__(self, 'ec2')
