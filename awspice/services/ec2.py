# -*- coding: utf-8 -*-
from base import AwsBase
from botocore.exceptions import ClientError

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
        'privateip': 'private-ip-address'
    }


    # #################################
    # -----------  COMMON  -----------
    # #################################

    def set_tag(self, resource_id, tag_key, tag_value, regions=[]):
        '''
        Set tag for an instance

        Args:
            elements_id (str): Element that will receive the change of label. (i-0123456890, vol-123456...)
            tag_key (str): Name of the element TAG (i.e: Name)
            tag_value (str): Value of that Tag
            regions (list): Regions where to look for this element

        Return:
            None
        '''
        regions = self.parse_regions(regions)
        for region in regions:
            self.change_region(region['RegionName'])
            try:
                self.client.create_tags(Resources=resource_id, Tags=[{'Key': tag_key, 'Value': tag_value}])
                return None
            except ClientError as e:
                pass
        raise Exception('The element {} does not exist for that regions.'.format(resource_id))



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
        Get all instances for one or more regions.

        Args:
            regions (list): Regions where to look for this element

        Returns:
            Instances (list): List of dictionaries with the instances requested
        '''
        return self._extract_instances(regions=regions)

    def get_instance_by(self, filter_key, filter_value, regions=[]):
        '''
        Get an instance for one or more regions that matches with filter

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter
            regions (list): Regions where to look for this element

        Return:
            Instance (dict): Dictionary with the instance requested
        '''
        return self.get_instances_by(filter_key, filter_value, regions, return_first=True)

    def get_instances_by(self, filter_key, filter_value, regions=[], return_first=False):
        '''
        Get an instance for one or more regions that matches with filter

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter
            regions (list): Regions where to look for this element
            return_first (bool): Select to return the first match

        Return:
            Instances (list): List of dictionaries with the instances requested
        '''
        self.validate_filters(filter_key, self.instance_filters)

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
        Get all volumes for one or more regions

        Args:
            regions (list): Regions where to look for this element

        Returns:
            Volumes (list): List of dictionaries with the volumes requested
        '''
        return self._extract_volumes(regions=regions)

    def get_volume_by(self, filter_key, filter_value, regions=[]):
        '''
        Get a volume for one or more regions that matches with filters

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter
            regions (list): Regions where to look for this element

        Returns:
            Volume (dict): Dictionary with the volume requested
        '''
        return self.get_volumes_by(filter_key, filter_value, regions, return_first=True)

    def get_volumes_by(self, filter_key, filter_value, regions=[], return_first=False):
        '''
        Get volumes for one or more regions that matches with filters

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter
            regions (list): Regions where to look for this element

        Returns:
            Volume (dict): Dictionary with the volume requested
        '''
        self.validate_filters(filter_key, self.instance_filters)

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
        Get all snapshots owned by self for the current region

        Returns:
            Snapshots (list): List of dictionaries with the snapshots requested
        '''
        return self.inject_client_vars(self.client.describe_snapshots(OwnerIds=['self'])['Snapshots'])

    def get_snapshot_by(self, filter_key, filter_value):
        '''
        Get a snapshot for a region tha matches with filters

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter

        Returns:
            Snapshot (dict): Dictionary with the snapshot requested
        '''
        snapshots = self.get_snapshots_by(filter_key, filter_value)
        if snapshots and len(snapshots) > 0:
            return snapshots[0]
        else:
            return None

    def get_snapshots_by(self, filter_key, filter_value):
        '''
        Get all snapshots for the current region that matches with filters

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter

        Returns:
            Snapshots (list): List of dictionaries with the snapshots requested
        '''
        self.validate_filters(filter_key, self.snapshot_filters)

        filters = [{
            'Name': self.snapshot_filters[filter_key],
            'Values': [filter_value]
        }]
        return self.inject_client_vars(self.client.describe_snapshots(Filters=filters)['Snapshots'])



    # #################################
    # ------------ SEC. GROUPS ------------
    # #################################

    def get_secgroups(self):
        '''
        Get all security groups for the current region

        Returns:
            SecurityGroups (list): List of dictionaries with the security groups requested
        '''
        return self.inject_client_vars(self.client.describe_security_groups()['SecurityGroups'])

    def get_secgroup_by(self, filter_key, filter_value):
        '''
        Get security group for a region that matches with filters

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter

        Returns:
            SecurityGroup (dict): Dictionaries with the security group requested
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
            SecurityGroups (list): List of dictionaries with the security groups requested
        '''
        self.validate_filters(filter_key, self.secgroup_filters)
        filters = [{
            'Name': self.secgroup_filters[filter_key],
            'Values': [filter_value]
        }]

        return self.inject_client_vars(self.client.describe_security_groups(Filters=filters)['SecurityGroups'])



    # #################################
    # ----------- ADDRESSES -----------
    # #################################

    def _extract_addresses(self, filters=[], regions=[], return_first=False):
        results = list()

        regions = self.parse_regions(regions)
        for region in regions:
            self.change_region(region['RegionName'])

            addresses = self.client.describe_addresses(Filters=filters)['Addresses']
            addresses = self.inject_client_vars(addresses)
            if return_first and len(addresses) > 0: return addresses[0]
            results.extend(addresses)

        return results

    def get_addresses(self, regions=[]):
        '''
        Get all IP Addresses for a region

        Args:
            regions (list): Regions where to look for this element

        Returns:
            Addresses (dict): List of dictionaries with the addresses requested
        '''
        return self._extract_addresses(regions=regions)

    def get_address_by(self, filter_key, filter_value, regions=[]):
        '''
        Get IP Addresses for a region that matches with filters

        Args:
            regions (list): Regions where to look for this element

        Returns:
            Address (dict): Dictionary with the address requested
        '''
        self.validate_filters(filter_key, self.address_filters)
        filters = [{
            'Name': self.address_filters[filter_key],
            'Values': [filter_value]
        }]
        return self._extract_addresses(filters=filters, regions=regions, return_first=True)



    # #################################
    # ------------ VPC ------------
    # #################################

    def get_vpcs(self):
        '''
        Get all VPCs for a region

        Returns:
            VPCs (list): List of dictionaries with the vpcs requested
        '''
        return self.inject_client_vars(self.client.describe_vpcs()['Vpcs'])



    def __init__(self):
        AwsBase.__init__(self, 'ec2')
