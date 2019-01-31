from threading import Lock

volume_filters = {
    'id': 'volume-id',
    'status': 'status',
    'instance': 'attachment.instance-id',
    'autodelete': 'attachment.delete-on-termination',
    'encrypted': 'encrypted',
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

        if volumes:
            volumes = self.inject_client_vars(volumes, config)
            if return_first:
                results.update(volumes[0])
            else:
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

def get_volume_by(self, filters, regions=[]):
    '''
    Get a volume for one or more regions that matches with filters

    Args:
        filter_key (str): Name of the filter
        filter_value (str): Value of the filter
        regions (lst): Regions where to look for this element

    Returns:
        Volume (dict): Dictionary with the volume requested
    '''
    return self.get_volumes_by(filters, regions, return_first=True)

def get_volumes_by(self, filters, regions=[], return_first=False):
    '''
    Get volumes for one or more regions that matches with filters

    Args:
        filter_key (str): Name of the filter
        filter_value (str): Value of the filter
        regions (lst): Regions where to look for this element

    Returns:
        Volume (dict): Dictionary with the volume requested
    '''
    formatted_filters = self.validate_filters(filters, self.volume_filters)
    return self._extract_volumes(filters=formatted_filters, regions=regions, return_first=return_first)

