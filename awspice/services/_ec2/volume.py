from threading import Lock

volume_filters = {
    'id': 'volume-id',
    'status': 'status',
    'tagname': 'tag:Name',
}


def _extract_volumes(self, filters=[], regions=[], return_first=False):
    regions = self.parse_regions(regions)
    results = dict() if return_first else list()
    lock = Lock()
    
    def worker(region):
        lock.acquire()
        self.change_region(region['RegionName'])
        config = self.get_client_vars()
        lock.release()

        volumes = self.client.describe_volumes(Filters=filters)['Volumes']
        volumes = self.inject_client_vars(volumes, config)

        if return_first and volumes:
            results.update(volumes[0])
        if not return_first and volumes:
            results.extend(volumes)

    # Launch tasks in threads
    for region in regions: self.pool.add_task(worker, region=region)

    # Wait results
    self.pool.wait_completion()

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

