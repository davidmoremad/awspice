# -*- coding: utf-8 -*-
from base import AwsBase
from threading import Lock

class RdsService(AwsBase):
    '''
    Class belonging to the Remote Database System service.
    '''

    database_filters = {
        'id': 'db-instance-id',
        'cluster': 'db-cluster-id',
    }

    def _extract_databases(self, filters=[], regions=[], return_first=False):
        results = dict() if return_first else list()
        regions = self.parse_regions(regions=regions)
        lock = Lock()
        
        def worker(region):
            lock.acquire()
            self.change_region(region['RegionName'])
            config = self.get_client_vars()
            lock.release()
            
            rdss = self.client.describe_db_instances(Filters=filters)['DBInstances']

            if rdss:
                rds = self.inject_client_vars(rdss, config)
                if return_first:
                    results.update(rdss[0])
                else:
                    results.extend(rdss)

        for region in regions:
            self.pool.add_task(worker, region)
        self.pool.wait_completion()

        return results


    def get_database_by(self, filters, regions=[]):
        formatted_filters = self.validate_filters(filters, self.database_filters)
        return self._extract_databases(filters=formatted_filters, regions=regions, return_first=True)



    def get_databases(self, regions=[]):
        '''
        Get RDS instances in regions

        Args:
            regions (list): Regions where you want to look for

        Returns:
            (list): List of RDS dicts
        '''
        return self._extract_databases(regions=regions)

    def get_snapshots(self, regions=[]):
        '''
        Get RDS snapshots in regions

        Args:
            regions (list): Regions where you want to look for

        Returns:
            (list): List of RDS dicts
        '''
        results = list()
        regions = self.parse_regions(regions=regions)
        lock = Lock()
        
        def worker(region):
            lock.acquire()
            self.change_region(region['RegionName'])
            config = self.get_client_vars()
            lock.release()
            rdss = self.client.describe_db_snapshots()['DBSnapshots']
            results.extend(self.inject_client_vars(rdss, config))

        for region in regions:
            self.pool.add_task(worker, region)
        self.pool.wait_completion()

        return results


    def __init__(self):
        AwsBase.__init__(self, 'rds')
