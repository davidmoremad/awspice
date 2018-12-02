
snapshot_filters = {
    'id': 'snapshot-id',
    'status': 'status',
}


def get_snapshots(self):
    '''
    Get all snapshots owned by self for the current region

    Returns:
        Snapshots (lst): List of dictionaries with the snapshots requested
    '''
    snapshots = self.client.describe_snapshots(OwnerIds=['self'])['Snapshots']
    return self.inject_client_vars(snapshots)

def get_snapshot_by(self, filter_key, filter_value):
    '''
    Get a snapshot for a region tha matches with filters

    Args:
        filter_key (str): Name of the filter
        filter_value (str): Value of the filter

    Returns:
        Snapshot (dict): Dictionary with the snapshot requested
    '''
    snapshots = self.get_snapshots_by(filter_key, filter_value)
    if snapshots and snapshots:
        return self.inject_client_vars(snapshots)[0]
    return None

def get_snapshots_by(self, filter_key, filter_value):
    '''
    Get all snapshots for the current region that matches with filters

    Args:
        filter_key (str): Name of the filter
        filter_value (str): Value of the filter

    Returns:
        Snapshots (lst): List of dictionaries with the snapshots requested
    '''
    self.validate_filters(filter_key, self.snapshot_filters)

    filters = [{
        'Name': self.snapshot_filters[filter_key],
        'Values': [filter_value]
    }]
    return self.inject_client_vars(self.client.describe_snapshots(Filters=filters)['Snapshots'])


