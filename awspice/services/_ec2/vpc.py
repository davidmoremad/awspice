
def _extract_vpcs(self, filters=[], regions=[], return_first=False):
    results = list()

    regions = self.parse_regions(regions)
    for region in regions:
        self.change_region(region['RegionName'])

        vpcs = self.client.describe_vpcs(Filters=filters)['Vpcs']
        vpcs = self.inject_client_vars(vpcs)

        if return_first and vpcs:
            self.change_region(curRegion)
            return vpcs[0]

        results.extend(vpcs)

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
