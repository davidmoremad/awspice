# -*- coding: utf-8 -*-
from base import AwsBase
import sys, dns.resolver


class ElbService(AwsBase):
    '''
    Class belonging to the Load Balancers service.
    '''

    loadbalancer_filters = {
        'domain': '',
        'tagname': '',
        'cname': '',
    }

    def _get_cname_from_domain(self, domain):
        try:
            cname = str(dns.resolver.query(domain, "CNAME")[0]).rstrip('.')
            if 'aws.com' not in cname: raise ValueError('Domain %s is not in AWS' % domain)
            return cname
        except (dns.resolver.NXDOMAIN):
            print("Couldn't find any records (NXDOMAIN)")
            raise
        except (dns.resolver.NoAnswer):
            print("Couldn't find any records (NoAnswer)")
            raise


    def get_loadbalancers(self, regions=[]):
        '''
        Get all Elastic Load Balancers for a region

        Args:
            regions (list): Regions where to look for this element

        Returns:
            LoadBalancers (list): List of dictionaries with the load balancers requested
        '''
        results = list()
        regions = self.parse_regions(regions=regions)
        for region in regions:
            self.change_region(region['RegionName'])

            elbs = self.client.describe_load_balancers()['LoadBalancerDescriptions']
            results.extend(self.inject_client_vars(elbs))

        return results


    def get_loadbalancer_by(self, filter_key, filter_value, regions=[]):
        '''
        Get a load balancer for a region that matches with filter

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter
            regions (list): Regions where to look for this element

        Return:
            LoadBalancer (dict): Dictionary with the load balancer requested
        '''
        self.validate_filters(filter_key, self.loadbalancer_filters)
        regions = self.parse_regions(regions=regions)

        if filter_key == 'tagname':
            for region in regions:
                self.change_region(region)
                elbs = self.client.describe_load_balancers(LoadBalancerNames=[filter_value])['LoadBalancerDescriptions']
                if elbs:
                    return self.inject_client_vars(elbs)[0]
        elif filter_key == 'domain' or filter_key == 'cname':
            cname = self._get_cname_from_domain(filter_value) if filter_key == 'domain' else filter_value
            self.change_region(cname.split('.')[1])

            elb = [elb for elb in self.get_loadbalancers() if elb['DNSName'].lower() == cname.lower()]
            return elb[0] if elb else None


    def __init__(self):
        AwsBase.__init__(self, 'elb')
