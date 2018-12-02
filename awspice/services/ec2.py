# -*- coding: utf-8 -*-
from awspice.services.base import AwsBase
from awspice.helpers import dnsinfo_from_ip
from botocore.exceptions import ClientError
import time

class Ec2Service(AwsBase):
    '''
    Class belonging to the EC2 Computing service.
    '''


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
    from _ec2.image import ami_filters
    from _ec2.image import ami_distributions
    from _ec2.image import distrib_amis

    from _ec2.image import _extract_amis
    from _ec2.image import get_amis
    from _ec2.image import get_ami_by
    from _ec2.image import get_amis_by
    from _ec2.image import get_amis_by_distribution


    # #################################
    # ----------- INSTANCES -----------
    # #################################
    from _ec2.instance import instance_filters
    
    from _ec2.instance import _extract_instances
    from _ec2.instance import get_instances
    from _ec2.instance import get_instance_by
    from _ec2.instance import get_instances_by
    from _ec2.instance import start_instances
    from _ec2.instance import stop_instances
    from _ec2.instance import create_instances


    # #################################
    # ------------ VOLUMES ------------
    # #################################
    from _ec2.volume import volume_filters

    from _ec2.volume import _extract_volumes
    from _ec2.volume import get_volumes
    from _ec2.volume import get_volume_by
    from _ec2.volume import get_volumes_by


    # #################################
    # ----------- SNAPSHOTS -----------
    # #################################
    from _ec2.snapshot import snapshot_filters

    from _ec2.snapshot import get_snapshots
    from _ec2.snapshot import get_snapshot_by
    from _ec2.snapshot import get_snapshots_by


    # #################################
    # ---------- SEC. GROUPS ----------
    # #################################
    from _ec2.security_group import secgroup_filters

    from _ec2.security_group import get_secgroups
    from _ec2.security_group import get_secgroup_by
    from _ec2.security_group import get_secgroups_by
    from _ec2.security_group import create_security_group
    from _ec2.security_group import delete_security_group


    # #################################
    # ----------- ADDRESSES -----------
    # #################################
    from _ec2.address import address_filters

    from _ec2.address import _extract_addresses
    from _ec2.address import get_addresses
    from _ec2.address import get_address_by
    

    # #################################
    # ------------- VPCS --------------
    # #################################
    from _ec2.vpc import _extract_vpcs
    from _ec2.vpc import get_vpcs
    from _ec2.vpc import get_default_vpc


    def __init__(self):
        AwsBase.__init__(self, 'ec2')
