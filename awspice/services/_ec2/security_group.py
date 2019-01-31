from threading import Lock

secgroup_filters = {
    'id': 'group-id',
    'name': 'group-name',
    'description': 'description',
    'protocol': 'ip-permission.protocol',
    'fromport': 'ip-permission.from-port',
    'toport': 'ip-permission.to-port',
    'range': 'ip-permission.cidr',
}

def _extract_secgroups(self, filters=[], regions=[], return_first=False):
    regions = self.parse_regions(regions)
    results = dict() if return_first else list()
    lock = Lock()

    def worker(region):
        lock.acquire()
        self.change_region(region['RegionName'])
        config = self.get_client_vars()
        lock.release()

        secgroups = self.client.describe_security_groups(Filters=filters)["SecurityGroups"]

        if secgroups:
            secgroups = self.inject_client_vars(secgroups, config)

            if return_first:
                results.update(secgroups[0])
            if not return_first:
                results.extend(secgroups)

    for region in regions: self.pool.add_task(worker, region=region)
    self.pool.wait_completion()
    
    return results

def get_secgroups(self, regions=[]):
    '''
    Get all security groups for the current region

    Returns:
        SecurityGroups (lst): List of dictionaries with the security groups requested
    '''
    return self._extract_secgroups(regions=regions)

def get_secgroup_by(self, filters, regions=[]):
    '''
    Get security group for a region that matches with filters

    Args:
        filter_key (str): Name of the filter
        filter_value (str): Value of the filter

    Returns:
        SecurityGroup (dict): Dictionaries with the security group requested
    '''
    formatted_filters = self.validate_filters(filters, self.secgroup_filters)
    return self._extract_secgroups(filters=formatted_filters, regions=regions, return_first=True)

def get_secgroups_by(self, filters, regions=[]):
    '''
    Get all security groups for a region that matches with filters

    Args:
        filter_key (str): Name of the filter
        filter_value (str): Value of the filter

    Returns:
        SecurityGroups (lst): List of dictionaries with the security groups requested
    '''
    formatted_filters = self.validate_filters(filters, self.secgroup_filters)
    return self._extract_secgroups(filters=formatted_filters, regions=regions)

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
