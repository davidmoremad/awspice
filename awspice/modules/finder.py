# -*- coding: utf-8 -*-

class ModuleFinder:

    def find_instance(self, filter_key, filter_value, profiles=[], regions=[]):
        profiles = self.aws.ec2.parse_profiles(profiles)
        regions = self.aws.ec2.parse_regions(regions, True)

        for account in profiles:
            self.aws.ec2.change_account(account)
            instance = self.aws.ec2.get_instance_by(filter_key, filter_value, regions=regions)
            if instance: return instance
        return None

    def find_instances(self, filter_key, filter_value, profiles=[], regions=[]):
        results = list()
        profiles = self.aws.ec2.parse_profiles(profiles)
        regions = self.aws.ec2.parse_regions(regions, True)

        for account in profiles:
            self.aws.ec2.change_account(account)
            results.extend(self.aws.ec2.get_instances_by(filter_key, filter_value, regions=regions))
        return results

    def find_volume(self, filter_key, filter_value, profiles=[], regions=[]):
        profiles = self.aws.ec2.parse_profiles(profiles)
        regions = self.aws.ec2.parse_regions(regions, True)

        for account in profiles:
            self.aws.ec2.change_account(account)
            regions = self.aws.ec2.parse_regions(regions, True)
            volume = self.aws.ec2.get_volume_by(filter_key, filter_value, regions=regions)
            if volume: return volume
        return None

    def find_volumes(self, filter_key, filter_value, profiles=[], regions=[]):
        results = list()
        profiles = self.aws.ec2.parse_profiles(profiles)
        regions = self.aws.ec2.parse_regions(regions, True)

        for account in profiles:
            self.aws.ec2.change_account(account)
            regions = self.aws.ec2.parse_regions(regions, True)
            results.extend(self.aws.ec2.get_volumes_by(filter_key, filter_value, regions=regions))
        return results

    def __init__(self, aws):
        self.aws = aws
