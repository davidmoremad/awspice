# -*- coding: utf-8 -*-
from base import AwsBase

class AcmService(AwsBase):
    '''
    Class belonging to the ACM certificate management service.
    '''

    def list_certificates(self, regions=[]):
        '''
        List all certificates

        Args:
            regions (lst): List of regions to list certificates

        Returns:
            List of certificates
        '''
        certificates = list()
        regions = self.parse_regions(regions)

        for region in regions:
            self.change_region(region['RegionName'])
            certificates.extend(self.inject_client_vars(self.client.list_certificates()['CertificateSummaryList']))

        return certificates

    def get_certificate_by(self, filter_key, filter_value, regions=[]):
        '''
        Get certificate filtering by domain

        Args:
            filter_key (str): Name of the field to be searched. (Domain)
            filter_value (str): Value for the previous field. (i.e.: google.es)
            regions (lst): List of regions where the certificate can be.

        Returns:
            Certificate matched to the filter entered.
        '''
        filters = ['domain']
        if filter_key not in filters:
            raise Exception('Invalid filter key. Allowed filters: ' + str(filters))

        certificates = self.list_certificates(regions=regions)
        certificate_arn = filter(lambda x: x['DomainName'] == filter_value , certificates)
        if certificate_arn:
            return self.get_certificate(arn=certificate_arn[0]['CertificateArn'], regions=[certificate_arn[0]['RegionName']])
        else:
            return None

    def get_certificate(self, arn, regions=[]):
        '''
        Get certificate using CertificateArn (Ceritificate Identifier)

        Args:
            arn (str): ARN of the certificate
            regions (lst): List of regions where the certificate can be.

        Returns:
            Certificate matched to the ARN entered.
        '''
        regions = self.parse_regions(regions)
        for region in regions:
            self.change_region(region['RegionName'])
            certificate = self.inject_client_vars([self.client.describe_certificate(CertificateArn=arn)['Certificate']])[0]
            if certificate: return certificate
        return None


    def __init__(self):
        AwsBase.__init__(self, 'acm')
