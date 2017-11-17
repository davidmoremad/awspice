# -*- coding: utf-8 -*-
from base import AwsBase

class AcmService(AwsBase):

    def get_certificates(self):
        '''
        Get all certificates for a region

        Returns:
            List of arrays with all certificates
        '''
        return self.inject_client_vars(self.client.list_certificates()['CertificateSummaryList'])

    def __init__(self):
        AwsBase.__init__(self, 'acm')
