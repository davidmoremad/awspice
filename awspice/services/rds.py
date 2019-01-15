# -*- coding: utf-8 -*-
from base import AwsBase
from threading import Lock

class RdsService(AwsBase):
    '''
    Class belonging to the Remote Database System service.
    '''

    def get_rdss(self, regions=[]):
        '''
        Get RDS instances in regions

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
            rdss = self.client.describe_db_instances()['DBInstances']
            results.extend(self.inject_client_vars(rdss, config))

        for region in regions:
            self.pool.add_task(worker, region)
        self.pool.wait_completion()

        return results

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
