
snapshot_filters = {
    'id': 'snapshot-id',
    'status': 'status',
    'owner': 'owner-id',
    'volume': 'volume-id',
}


def get_snapshots(self):
    '''
    Get all snapshots owned by self for the current region

    Returns:
        Snapshots (lst): List of dictionaries with the snapshots requested
    '''
    snapshots = self.client.describe_snapshots(OwnerIds=['self'])['Snapshots']
    return self.inject_client_vars(snapshots)

def get_snapshot_by(self, filters):
    '''
    Get a snapshot for a region tha matches with filters

    Args:
        filter_key (str): Name of the filter
        filter_value (str): Value of the filter

    Returns:
        Snapshot (dict): Dictionary with the snapshot requested
    '''
    snapshots = self.get_snapshots_by(filters)
    if snapshots and snapshots:
        return self.inject_client_vars(snapshots)[0]
    return None

def get_snapshots_by(self, filters):
    '''
    Get all snapshots for the current region that matches with filters

    Args:
        filter_key (str): Name of the filter
        filter_value (str): Value of the filter

    Returns:
        Snapshots (lst): List of dictionaries with the snapshots requested
    '''
    formatted_filters = self.validate_filters(filters, self.snapshot_filters)
    return self.inject_client_vars(self.client.describe_snapshots(Filters=formatted_filters)['Snapshots'])


