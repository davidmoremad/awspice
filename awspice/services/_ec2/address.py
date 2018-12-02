
address_filters = {
    'publicip': 'public-ip',
    'privateip': 'private-ip-address'
}


def _extract_addresses(self, filters=[], regions=[], return_first=False):
    results = list()

    regions = self.parse_regions(regions)
    for region in regions:
        self.change_region(region['RegionName'])

        addresses = self.client.describe_addresses(Filters=filters)['Addresses']
        addresses = self.inject_client_vars(addresses)

        if return_first and addresses:
            self.change_region(curRegion)
            return addresses[0]

        results.extend(addresses)

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

