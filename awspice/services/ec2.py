# -*- coding: utf-8 -*-
from awspice.services.base import AwsBase
from botocore.exceptions import ClientError
import types
class Ec2Service(AwsBase):
    '''
    Class belonging to the EC2 Computing service.
    '''

    ami_filters = {
        'id': 'image-id',
        'name': 'name',
        'architecture': 'architecture',
        'platform': 'platform',
    }

    ami_distributions = {
        'ubuntu': 'ubuntu/images/hvm-ssd/ubuntu-*-*{version}*-amd64-server-*',
        'windows': 'Windows_Server-*{version}*-English-*-Base-20*.*.*',
        'amazon': 'amzn-ami-hvm-20*.*.*-x86_64-*',
    }

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

    distrib_amis = {
        'ubuntu': 'ami-f90a4880',
        'windows': 'ami-b5530b5e',
        'redhat': 'ami-c86c3f23',
    }

    snapshot_filters = {
        'id': 'snapshot-id',
        'status': 'status',
    }

    volume_filters = {
        'id': 'volume-id',
        'status': 'status',
        'tagname': 'tag:Name',
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
            elements_id (str): Id of resources to tag. (i.e: i-01234, vol-01234)
            tag_key (str): Name of the element TAG (i.e: Name)
            tag_value (str): Value of that Tag
            regions (lst): Regions where to look for this element

        Returns:
            None
        '''
        tags = [{'Key': tag_key, 'Value': tag_value}]
        curRegion = AwsBase.region
        regions = self.parse_regions(regions)

        for region in regions:
            self.change_region(region['RegionName'])
            try:
                self.client.create_tags(Resources=resource_id, Tags=tags)
                return None
            except ClientError:
                pass
            finally:
                self.change_region(curRegion)

        raise Exception('The element {} does not exist for that regions.'.format(resource_id))

    # #################################
    # -------------- AMIS -------------
    # #################################

    def _extract_amis(self, filters=[], regions=[], return_first=False):
        filters.append({'Name': 'state', 'Values': ['available', 'pending']})
        # Just supported x64 OS
        filters.append({'Name': 'architecture', 'Values': ['x86_64']})
        filters.append({'Name': 'hypervisor', 'Values': ['xen']})
        filters.append({'Name': 'virtualization-type', 'Values': ['hvm']})
        filters.append({'Name': 'image-type', 'Values': ['machine']})
        filters.append({'Name': 'root-device-type', 'Values': ['ebs']})

        curRegion = AwsBase.region
        regions = self.parse_regions(regions)
        results = list()

        for region in regions:
            self.change_region(region['RegionName'])

            amis = self.client.describe_images(Filters=filters)['Images']
            amis = self.inject_client_vars(amis)
            if return_first and amis:
                self.change_region(curRegion)
                return amis[0]
            results.extend(amis)

        self.change_region(curRegion)
        return results

    def get_amis_by_distribution(self, distrib, version='*', latest=False, regions=[]):
        '''
        Get one or more Images filtering by distribution

        Args:
            distrib (str): Distribution of the image (i.e.: ubuntu)
            version (str): Version of the system
            latest (bool): True if only returns the newest item.

        Return:
            Image (lst): List with the images requested.
        '''

        self.validate_filters(distrib, self.ami_distributions.keys())
        filters = [
            {'Name': 'name', 'Values': [self.ami_distributions[distrib].format(version=version)]},
            {'Name': 'is-public', 'Values': ['true']}
        ]

        results = self._extract_amis(filters=filters, regions=regions)
        results = sorted(results, key=lambda k: k['Name'])

        if latest and results:
            return [results[-1]]

        return results

    def get_ami_by(self, filter_key, filter_value, regions=[]):
        '''
        Get an ami for one or more regions that matches with filter

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter
            regions (lst): Regions where to look for this element

        Return:
            Image (dict): Image requested
        '''
        return self.get_amis_by(filter_key=filter_key,
                                filter_value=filter_value,
                                regions=regions,
                                return_first=True)

    def get_amis_by(self, filter_key, filter_value, regions=[], return_first=False):
        '''
        Get list of amis for one or more regions that matches with filter

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter
            regions (lst): Regions where to look for this element
            return_first (bool): True if return first result

        Return:
            Images (lst): List of requested images
        '''

        self.validate_filters(filter_key, self.ami_filters)

        filters = [{
            'Name': self.ami_filters[filter_key],
            'Values': [filter_value]
        }]

        return self._extract_amis(filters=filters, regions=regions, return_first=return_first)

    def get_amis(self, regions=[]):
        '''
        Get all images

        Args:
            regions (lst): Regions where to look for this element

        Returns:
            Images (lst): List of all images
        '''
        return self._extract_amis(regions=regions)


    # #################################
    # ----------- INSTANCES -----------
    # #################################

    def _extract_instances(self, filters=[], regions=[], return_first=False):
        results = list()
        curRegion = AwsBase.region
        regions = self.parse_regions(regions)

        for region in regions:
            self.change_region(region['RegionName'])

            reservations = self.client.describe_instances(Filters=filters)["Reservations"]
            for reserv in reservations:
                instances = self.inject_client_vars(reserv['Instances'])

                if return_first and instances:
                    self.change_region(curRegion)
                    return instances[0]

                results.extend(instances)

        self.change_region(curRegion)
        return results

    def get_instances(self, regions=[]):
        '''
        Get all instances for one or more regions.

        Args:
            regions (lst): Regions where to look for this element

        Returns:
            Instances (lst): List of dictionaries with the instances requested
        '''
        return self._extract_instances(regions=regions)

    def get_instance_by(self, filter_key, filter_value, regions=[]):
        '''
        Get an instance for one or more regions that matches with filter

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter
            regions (lst): Regions where to look for this element

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
            regions (lst): Regions where to look for this element
            return_first (bool): Select to return the first match

        Return:
            Instances (lst): List of dictionaries with the instances requested
        '''
        self.validate_filters(filter_key, self.instance_filters)

        filters = [{
            'Name': self.instance_filters[filter_key],
            'Values': [filter_value]
        }]

        return self._extract_instances(filters=filters, regions=regions, return_first=return_first)

    def create_instances(self, name, key_name, allowed_range, ami=None, distribution=None,
                         version=None, instance_type='t2.micro', region=None, vpc=None, count=1):
        '''
        Create a new instance

        Args:
            name (str): TagName of the instance
            key_name (str): The name of the key pair (i.e: it_user)
            allowed_range (str): Network range with access to instance (i.e: 10.0.0.0/32)
            ami (str): Id of the ami (i.e: ami-12345)
            instance_type (str): Type of hardware of the instance (i.e: t2.medium)
            distribution (str): Instead of ami, select an OS: (i.e: ubuntu)
            region (str): Name of the region where  instance will be displayed
            vpc (str): VPC identifier where the instance will be deployed.
            count (int): Number of instances to launch

        Returns:
            Instances (lst): List of launched instances
        '''

        if region:
            curRegion = AwsBase.region
            self.change_region(region)

        if not vpc:
            vpc = self.get_default_vpc()['VpcId']

        if not ami:
            latest_ami = []
            if distribution and version:
                latest_ami = self.get_amis_by_distribution(distribution, version, latest=True)
            elif distribution and not version:
                latest_ami = self.get_amis_by_distribution(distribution, latest=True)

            if latest_ami:
                ami = latest_ami[0]['ImageId']
            else:
                raise ValueError("Insert a valid AMI or distribution.\n" +
                                 "Parameters: Distribution={distrib}; Version={version}; ami={ami}".format(
                        distrib=distribution,
                        version=version,
                        ami=ami))

        secgroup_id = str()
        try:
            secgroup_id = self.create_security_group(name, allowed_range, vpc)
            instance = self.resource.create_instances(
                ImageId=ami,
                InstanceType=instance_type,
                KeyName=key_name,
                SecurityGroupIds=[secgroup_id],
                MaxCount=count,
                MinCount=count,
                TagSpecifications=[
                    {'ResourceType': 'instance', 'Tags': [
                        {'Key': 'Name', 'Value': name}]}
                ]
            )
            return instance
        except Exception:
            if secgroup_id:
                self.delete_security_group(secgroup_id)
            raise
        finally:
            self.change_region(curRegion)


    def start_instances(self, instance_ids, regions=[]):
        '''
        Stops an Amazon EC2 instance

        Args:
            instance_ids (lst): List of identifiers of instances to be started.

        Examples:
            $ aws.service.ec2.start_instances(instances=['i-001'])
            $ aws.service.ec2.start_instances(instances=['i-001', 'i-033'], regions=['eu-west-1', 'eu-central-1'])

        Returns:
            lst: List of instances to be started, with their previous and current status.
        '''
        regions = self.parse_regions(regions)
        started_instances = list()

        for region in regions:
            self.change_region(region['RegionName'])

            for instance in instance_ids:
                try:
                    x = self.client.start_instances(InstanceIds=[instance])
                    started_instances.extend(x['StartingInstances'])
                    instance_ids.remove(instance)

                except ClientError:
                    pass

        return started_instances


    def stop_instances(self, instance_ids, regions=[], force=False):
        '''
        Stops an Amazon EC2 instance

        Args:
            instance_ids (lst): List of identifiers of instances to be stopped.

        Examples:
            $ aws.service.ec2.stop_instances(instances=['i-001'])
            $ aws.service.ec2.stop_instances(instances=['i-001', 'i-033'], regions=['eu-west-1', 'eu-central-1'])

        Returns:
            lst: List of instances to be stopped, with their previous and current status.
        '''
        regions = self.parse_regions(regions)
        stopped_instances = list()

        for region in regions:
            self.change_region(region['RegionName'])

            for instance in instance_ids:
                try:
                    x = self.client.stop_instances(InstanceIds=[instance], Force=force)
                    stopped_instances.extend(x['StoppingInstances'])
                    instance_ids.remove(instance)

                except ClientError:
                    pass

        return stopped_instances



    # #################################
    # ------------ VOLUMES ------------
    # #################################

    def _extract_volumes(self, filters=[], regions=[], return_first=False):
        results = list()

        curRegion = AwsBase.region
        regions = self.parse_regions(regions)
        for region in regions:
            self.change_region(region['RegionName'])

            volumes = self.client.describe_volumes(Filters=filters)['Volumes']
            volumes = self.inject_client_vars(volumes)

            if return_first and volumes:
                self.change_region(curRegion)
                return volumes[0]

            results.extend(volumes)

        self.change_region(curRegion)
        return results

    def get_volumes(self, regions=[]):
        '''
        Get all volumes for one or more regions

        Args:
            regions (lst): Regions where to look for this element

        Returns:
            Volumes (lst): List of dictionaries with the volumes requested
        '''
        return self._extract_volumes(regions=regions)

    def get_volume_by(self, filter_key, filter_value, regions=[]):
        '''
        Get a volume for one or more regions that matches with filters

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter
            regions (lst): Regions where to look for this element

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
            regions (lst): Regions where to look for this element

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
    # ----------- SNAPSHOTS -----------
    # #################################

    def get_snapshots(self):
        '''
        Get all snapshots owned by self for the current region

        Returns:
            Snapshots (lst): List of dictionaries with the snapshots requested
        '''
        snapshots = self.client.describe_snapshots(OwnerIds=['self'])['Snapshots']
        return self.inject_client_vars(snapshots)

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
        if snapshots and snapshots:
            return self.inject_client_vars(snapshots)[0]
        return None

    def get_snapshots_by(self, filter_key, filter_value):
        '''
        Get all snapshots for the current region that matches with filters

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter

        Returns:
            Snapshots (lst): List of dictionaries with the snapshots requested
        '''
        self.validate_filters(filter_key, self.snapshot_filters)

        filters = [{
            'Name': self.snapshot_filters[filter_key],
            'Values': [filter_value]
        }]
        return self.inject_client_vars(self.client.describe_snapshots(Filters=filters)['Snapshots'])



    # #################################
    # ---------- SEC. GROUPS ----------
    # #################################

    def get_secgroups(self):
        '''
        Get all security groups for the current region

        Returns:
            SecurityGroups (lst): List of dictionaries with the security groups requested
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
        secgroup = self.get_secgroups_by(filter_key, filter_value)
        if secgroup:
            return self.inject_client_vars(secgroup)[0]
        return None

    def get_secgroups_by(self, filter_key, filter_value):
        '''
        Get all security groups for a region that matches with filters

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter

        Returns:
            SecurityGroups (lst): List of dictionaries with the security groups requested
        '''
        self.validate_filters(filter_key, self.secgroup_filters)
        filters = [{
            'Name': self.secgroup_filters[filter_key],
            'Values': [filter_value]
        }]

        secgroups = self.client.describe_security_groups(Filters=filters)['SecurityGroups']
        return self.inject_client_vars(secgroups)

    def create_security_group(self, name, allowed_range, vpc_id=None):
        '''
        Create a new Security Group

        Args:
            name (str): Name of the Security Group
            allowed_range (str): Network range with permissions (i.e: 10.0.0.0/32)
            vpc_id (str): Id of assigned VPC

        Returns:
            str: Identifier of the security group created.
        '''
        vpc = vpc_id if vpc_id else self.get_default_vpc()['VpcId']
        desc = 'Security group created by Awspice'
        default_rules = [
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': allowed_range}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': allowed_range}]}
        ]

        sg_id = self.client.create_security_group(
            GroupName=name, VpcId=vpc, Description=desc)['GroupId']
        self.client.authorize_security_group_ingress(
            GroupId=sg_id, IpPermissions=default_rules)

        return sg_id

    def delete_security_group(self, identifier):
        '''
        Delete an existing Security Group

        Args:
            identifier (str): Id of the Security Group

        Returns:
            none
        '''
        self.client.delete_security_group(GroupId=identifier)

    # #################################
    # ----------- ADDRESSES -----------
    # #################################

    def _extract_addresses(self, filters=[], regions=[], return_first=False):
        results = list()

        curRegion = AwsBase.region
        regions = self.parse_regions(regions)
        for region in regions:
            self.change_region(region['RegionName'])

            addresses = self.client.describe_addresses(Filters=filters)['Addresses']
            addresses = self.inject_client_vars(addresses)

            if return_first and addresses:
                self.change_region(curRegion)
                return addresses[0]

            results.extend(addresses)

        self.change_region(curRegion)
        return results

    def get_addresses(self, regions=[]):
        '''
        Get all IP Addresses for a region

        Args:
            regions (lst): Regions where to look for this element

        Returns:
            Addresses (dict): List of dictionaries with the addresses requested
        '''
        return self._extract_addresses(regions=regions)

    def get_address_by(self, filter_key, filter_value, regions=[]):
        '''
        Get IP Addresses for a region that matches with filters

        Args:
            regions (lst): Regions where to look for this element

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
    # ------------- VPCS --------------
    # #################################

    def _extract_vpcs(self, filters=[], regions=[], return_first=False):
        results = list()

        curRegion = AwsBase.region
        regions = self.parse_regions(regions)
        for region in regions:
            self.change_region(region['RegionName'])

            vpcs = self.client.describe_vpcs(Filters=filters)['Vpcs']
            vpcs = self.inject_client_vars(vpcs)

            if return_first and vpcs:
                self.change_region(curRegion)
                return vpcs[0]

            results.extend(vpcs)

        self.change_region(curRegion)
        return results

    def get_vpcs(self, regions=[]):
        '''
        Get all VPCs for a region

        Returns:
            VPCs (lst): List of dictionaries with the vpcs requested
        '''
        return self._extract_vpcs(regions=regions)

    def get_default_vpc(self):
        '''
        Get default Security Group

        Returns:
            SecurityGroup (dict): Default security group resource
        '''
        vpcs = self.get_vpcs()

        vpc = filter(lambda x: x['IsDefault'] is True, vpcs)
        return vpc[0]



    def __init__(self):
        AwsBase.__init__(self, 'ec2')
