# -*- coding: utf-8 -*-
from .finder import FinderModule

class SecurityModule:
    '''
    This class facilitates methods for securing the AWS account

    Methods are available to help improve AWS account security by detecting bad configurations.
    '''

    @classmethod
    def get_instance_portlisting(cls, aws, instanceid):
        '''
        List SecurityGroups and rules for an instance

        Args:
            aws: AwsManager client
            instanceid: Id of instance to analyze

        Return:
            Dictionary with instance and its SecurityGroups
        '''
        results = dict()
        instance = FinderModule(aws).find_instance(aws, 'id', instanceid)
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

    @classmethod
    def get_region_portlisting(cls, aws, region):
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
