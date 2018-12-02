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

distrib_amis = {
    'ubuntu': 'ami-f90a4880',
    'windows': 'ami-b5530b5e',
    'redhat': 'ami-c86c3f23',
}


def _extract_amis(self, filters=[], regions=[], return_first=False):
    filters.append({'Name': 'state', 'Values': ['available', 'pending']})
    # Just supported x64 OS
    filters.append({'Name': 'architecture', 'Values': ['x86_64']})
    filters.append({'Name': 'hypervisor', 'Values': ['xen']})
    filters.append({'Name': 'virtualization-type', 'Values': ['hvm']})
    filters.append({'Name': 'image-type', 'Values': ['machine']})
    filters.append({'Name': 'root-device-type', 'Values': ['ebs']})

    curRegion = self.region
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