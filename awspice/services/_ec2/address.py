
address_filters = {
    'publicip': 'public-ip',
    'privateip': 'private-ip-address',
    'domain': 'domain',
    'instance': 'instance-id'
}


def _extract_addresses(self, filters=[], regions=[], return_first=False):
    results = list()

    regions = self.parse_regions(regions)
    for region in regions:
        self.change_region(region['RegionName'])

        addresses = self.client.describe_addresses(Filters=filters)['Addresses']
        addresses = self.inject_client_vars(addresses)

        if return_first and addresses:
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

def get_addresses_by(self, filters, regions=[]):
    '''
    Get all IP Addresses for a region

    Args:
        regions (lst): Regions where to look for this element

    Returns:
        Addresses (dict): List of dictionaries with the addresses requested
    '''
    formatted_filters = self.validate_filters(filters, self.address_filters)
    return self._extract_addresses(filters=formatted_filters, regions=regions)

def get_address_by(self, filters, regions=[]):
    '''
    Get IP Addresses for a region that matches with filters

    Args:
        regions (lst): Regions where to look for this element

    Returns:
        Address (dict): Dictionary with the address requested
    '''
    formatted_filters = self.validate_filters(filters, self.address_filters)
    return self._extract_addresses(filters=formatted_filters, regions=regions, return_first=True)

