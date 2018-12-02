
secgroup_filters = {
    'id': 'group-id',
    'description': 'description',
}


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
