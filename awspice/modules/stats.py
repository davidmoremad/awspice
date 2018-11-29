# -*- coding: utf-8 -*-

class StatsModule:
    '''
    Class responsible for processing general data to the AWS account.

    This class is dedicated to the global management of the AWS account in order to obtain statistics, costs or global information.

    Attributes:
        aws: awspice client
    '''

    def get_stats(self, regions=[]):
        '''
        Retrieve data about services in your AWS account like Volumes, Instances or Databases.

        Args:
            aws: AwsManager client
            region: To retrieve data only of this region

        Return:
            List of regions with its stats
        '''
        results = dict()
        regions = self.aws.ec2.parse_regions(regions)

        results['Users'] = self.aws.iam.get_users()
        results['Buckets'] = self.aws.s3.get_buckets()
        results['Regions'] = dict()
        for region in regions:
            self.aws.ec2.change_region(region['RegionName'])
            data = dict()
            data['Instances'] = self.aws.ec2.get_instances()
            data['SecurityGroups'] = self.aws.ec2.get_secgroups()
            data['Volumes'] = self.aws.ec2.get_volumes()
            # data['Snapshots'] = self.aws.ec2.get_snapshots();  # Need to select only private snaps
            data['Addresses'] = self.aws.ec2.get_addresses()
            data['Vpcs'] = self.aws.ec2.get_vpcs()
            data['LoadBalancers'] = self.aws.elb.get_loadbalancers()
            data['Databases'] = self.aws.rds.get_rdss()
            data['Certificates'] = self.aws.acm.list_certificates()
            results['Regions'][region['RegionName']] = data
        return results

    def cost_saving(self, regions=[]):
        '''
        List unused elements that carry expenses.

        Args:
            aws: AwsManager client.

        Returns:
            Dict Region with a list of regions with its unused elements
        '''
        results = dict()
        regions = self.aws.ec2.parse_regions(regions)

        for region in regions:
            self.aws.ec2.change_region(region['RegionName'])

            savings = dict()
            savings['Volumes'] = self.aws.ec2.get_volumes_by('status', 'available')
            adds = self.aws.ec2.get_addresses()
            savings['Addresses'] = filter(lambda x: x.get('AssociationId') == None, adds)
            elbs = self.aws.elb.get_loadbalancers()
            savings['LoadBalancers'] = filter(lambda x: x.get('Instances') == [], elbs)

            results[region['RegionName']] = savings
        return {'Regions': results}

    def __init__(self, aws):
        self.aws = aws
