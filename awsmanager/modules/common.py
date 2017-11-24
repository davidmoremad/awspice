# -*- coding: utf-8 -*-
import sys, dns.resolver

class ModuleCommon():

    def get_balancer_by_domain(self, domain, regions=[]):
        '''
        Find LoadBalancer and instances through a domain.

        Args:
            aws: AwsManager client
            domain: Domain to found in AWS

        Returns:
            Dict with element LoadBalancer with its instances
        '''
        results = dict()
        ######## Get CNAME of ELB if exists #######
        try:
            cname = str(dns.resolver.query(domain, "CNAME")[0]).rstrip('.')
            if 'aws.com' not in cname: raise Exception
        except Exception:
            print('[!] Domain {} is not in AWS').format(domain)
            return None

        ######## Search ELB in AWS #######
        regions = self.aws.ec2.parse_regions(regions, default_all=True)
        for region in regions:
            self.aws.ec2.change_region(region['RegionName'])
            elb = [elb for elb in self.aws.elb.get_elbs() if elb['DNSName'].lower() == cname.lower()]
            if len(elb) > 0:
                results = elb[0]
                break;

        if len(results) == 0:
            return None

        elbinstances = map(lambda x: x['InstanceId'], elb[0]['Instances'])
        results['Instances'] = self.aws.ec2.client.describe_instance_status(InstanceIds=elbinstances)['InstanceStatuses']

        secgroups = list()
        for elb_sg in results['SecurityGroups']:
            secgroups.append(self.aws.ec2.get_secgroup_by('id',elb_sg))
        results['SecurityGroups'] = secgroups

        return {'LoadBalancer': results}

    def __init__(self, aws):
        self.aws = aws
