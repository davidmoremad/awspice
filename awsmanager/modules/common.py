# -*- coding: utf-8 -*-
import sys, dns.resolver
from datetime import datetime
from dateutil.relativedelta import relativedelta
from . import ModuleFindElements

class ModuleCommon():

    def get_statistics(self, aws, region=None):
        '''
        Retrieve data about services in your AWS account like Volumes, Instances or Databases.

        Args:
            aws: AwsManager client
            region: To retrieve data only of this region

        Return:
            List of regions with its stats
        '''
        results = dict()
        results['Users'] = aws.iam.get_users();
        results['Buckets'] = aws.s3.get_buckets();
        results['Regions'] = dict()

        regions = {'RegionName': region} if region else aws.ec2.get_regions()
        for reg in regions:
            aws.ec2.change_region(reg['RegionName'])

            data = dict()
            data['Instances'] = aws.ec2.get_instances();
            data['SecurityGroups'] = aws.ec2.get_secgroups();
            data['Volumes'] = aws.ec2.get_volumes();
            # data['Snapshots'] = aws.ec2.get_snapshots();  # Need to select only private snaps
            data['Addresses'] = aws.ec2.get_addresses();
            data['Vpcs'] = aws.ec2.get_vpcs();
            data['LoadBalancers'] = aws.elb.get_elbs();
            data['Databases'] = aws.rds.get_rdss();
            data['Certificates'] = aws.acm.get_certificates();

            results['Regions'][reg['RegionName']] = data
        return results

    def cost_savings(self, aws):
        '''
        List unused elements that carry expenses.

        Args:
            aws: AwsManager client.

        Returns:
            Dict Region with a list of regions with its unused elements
        '''
        results = dict()

        for region in aws.ec2.get_regions():
            aws.ec2.change_region(region['RegionName'])

            savings = dict()
            savings['Volumes'] = aws.ec2.get_volumes_by('status', 'available')
            adds = aws.ec2.get_addresses()
            savings['Addresses'] = filter(lambda x: x.get('AssociationId') == None, adds)
            elbs = aws.elb.get_elbs()
            savings['Balancers'] = filter(lambda x: x.get('Instances') == [], elbs)

            results[region['RegionName']] = savings
        return {'Regions': results}

    def get_elb_by_domain(self, aws, domain):
        '''
        Find LoadBalancer and instances through a domain.

        Args:
            aws: AwsManager client
            domain: Domain to found in AWS

        Returns:
            Dict with element LoadBalancer with its instances
        '''
        results = dict()
        try:
            cname = str(dns.resolver.query(domain, "CNAME")[0]).rstrip('.')
            if 'aws.com' not in cname: raise Exception
        except Exception:
            print('[!] Domain {} is not in AWS').format(domain)
            return None

        for region in aws.ec2.get_regions():
            aws.ec2.change_region(region['RegionName'])
            elb = [elb for elb in aws.elb.get_elbs() if elb['DNSName'] == cname]
            if elb: break
        results.update(elb[0])

        elbinstances = map(lambda x: x['InstanceId'], elb[0]['Instances'])
        results['Instances'] = aws.ec2.client.describe_instance_status(InstanceIds=elbinstances)['InstanceStatuses']

        return {'LoadBalancer': results}

    def get_instance_portlisting(self, aws, instanceid):
        '''
        List SecurityGroups and rules for an instance

        Args:
            aws: AwsManager client
            instanceid: Id of instance to analyze

        Return:
            Dictionary with instance and its SecurityGroups
        '''
        results = dict()
        instance = ModuleFindElements().find_instance(aws, 'id', instanceid)
        results.update(instance)

        results['SecurityGroups'] = list()
        for secgroup in instance["SecurityGroups"]:
            sg = secgroup
            sg['Rules'] = list()
            for rule in aws.ec2.get_secgroup_by('id', secgroup["GroupId"])["IpPermissions"]:
                sg['Rules'].append({
                    'FromPort' : rule.get("FromPort", ''),
                    'ToPort'   : rule.get("ToPort", ''),
                    'Protocol' : rule.get("IpProtocol", '') if rule.get("IpProtocol", '') != '-1' else 'ALL',
                    'IpRange'  : [iprange["CidrIp"] for iprange in rule.get("IpRanges", '')]
                })
            results['SecurityGroups'].append(sg)

        return {'Instance': results}

    def get_region_portlisting(self, aws, region):
        '''
        List SecurityGroups and rules for all instances in region

        Args:
            aws: AwsManager client
            region: Region to analyze

        Return:
            Dictionary with regions, instances and its SecurityGroups
        '''
        results = []
        aws.ec2.change_region(region)

        for instance in aws.ec2.get_instances():
            ins_element = dict()
            ins_element.update(instance)
            ins_element['SecurityGroups'] = list()
            for securitygroup in instance['SecurityGroups']:
                sg_element = dict()
                sg_element.update(securitygroup)
                sg_element['Rules'] = list()
                for rule in aws.ec2.get_secgroup_by('id', securitygroup["GroupId"])["IpPermissions"]:
                    sg_element['Rules'].append({'ToPort'   : rule.get("ToPort", ''),
                                                'FromPort' : rule.get("FromPort", ''),
                                                'Protocol' : rule.get("IpProtocol", '') if rule.get("IpProtocol", '') != '-1' else 'ALL',
                                                'IpRange'  : [iprange["CidrIp"] for iprange in rule.get("IpRanges", '')]})
                ins_element['SecurityGroups'].append(sg_element)
            results.append(ins_element)

        return {'RegionName': region, 'Instances': results}
