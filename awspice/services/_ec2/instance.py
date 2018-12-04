from threading import Lock
from awspice.helpers import extract_region_from_ip

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


def _extract_instances(self, filters=[], regions=[], return_first=False):
    regions = self.parse_regions(regions)
    results = dict() if return_first else list()
    lock = Lock()

    def worker(region):
        # Race Condition: Locking AwsBase.region...
        # Change region > Get client config > Do the query
        lock.acquire()
        self.change_region(region['RegionName'])
        config = self.get_client_vars()
        lock.release()

        reservations = self.client.describe_instances(Filters=filters)["Reservations"]
        for reserv in reservations:
            instances = self.inject_client_vars(reserv['Instances'], config)

            if return_first and instances:
                results.update(instances[0])
            if not return_first and instances:
                results.extend(instances)

    # Launch tasks in threads
    for region in regions: self.pool.add_task(worker, region=region)

    # Wait results
    self.pool.wait_completion()
    
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
    results = []

    self.validate_filters(filter_key, self.instance_filters)
    filters = [{
        'Name': self.instance_filters[filter_key],
        'Values': [filter_value]
    }]
    
    if filter_key == "publicip":
        ip_in_aws, ip_region = extract_region_from_ip(filter_value)
        if not ip_in_aws: return results
        if regions and (ip_region in regions or ip_region in regions.keys()):
            regions = ip_region

    results = self._extract_instances(filters=filters, regions=regions, return_first=return_first)
    return results

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