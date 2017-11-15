# -*- coding: utf-8 -*-

class ModuleFindElements:

    def find_instance(self, aws, filter_key, filter_value, accounts=[]):
        if isinstance(accounts, list) and len(accounts) > 0:
            if (accounts[0] == 'ALL'): accounts = aws.ec2.get_accounts()
            for account in accounts:
                aws.ec2.change_account(account)
                instance = aws.ec2.get_instance_by(filter_key, filter_value, region_switch=True)
                if instance: return instance
            return None
        else:
            return aws.ec2.get_instance_by(filter_key, filter_value, region_switch=True)

    def find_instances(self, aws, filter_key, filter_value, accounts=[]):
        results = list()
        if isinstance(accounts, list) and len(accounts) > 0:
            if (accounts[0] == 'ALL'): accounts = aws.ec2.get_accounts()
            for account in accounts:
                aws.ec2.change_account(account)
                results.extend(aws.ec2.get_instances_by(filter_key, filter_value, region_switch=True))
        else:
            results = aws.ec2.get_instances_by(filter_key, filter_value, region_switch=True)
        return results

    def find_volume(self, aws, filter_key, filter_value):
        for region in aws.ec2.get_regions():
            aws.ec2.change_region(region['RegionName'])
            volume = aws.ec2.get_volumes_by(filter_key, filter_value)
            if volume:
                return volume[0]

    def find_volumes(self, aws, filter_key, filter_value):
        results = []
        for region in aws.ec2.get_regions():
            aws.ec2.change_region(region['RegionName'])
            results.extend(aws.ec2.get_volumes_by(filter_key, filter_value))
        return results


    def find_snapshot(self, aws, filter_key, filter_value):
        for region in aws.ec2.get_regions():
            aws.ec2.change_region(region['RegionName'])
            snapshot = aws.ec2.get_snapshot_by(filter_key, filter_value)
            if snapshot:
                return snapshot

    def find_snapshots(self, aws, filter_key, filter_value):
        return aws.ec2.get_snapshots_by(filter_key, filter_value)
