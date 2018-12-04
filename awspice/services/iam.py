# -*- coding: utf-8 -*-
from base import AwsBase
from datetime import datetime

class IamService(AwsBase):
    '''
    Class belonging to the IAM Identity & Access management service.
    '''

    def get_inactive_users(self):
        ''' Get users who have not logged in AWS since 1 year.
        This method returns users who haven't used their password and one of their keys in less than 9 months.
        
        Returns:
            list: List of inactive users
        '''

        results = []
        today = datetime.now()
        min_inactive_days = 270 # 9 months

        def worker(user):
            pass_last_use = user.get('PasswordLastUsed', None)
            pass_inactive_days = (today - pass_last_use.replace(tzinfo=None)).days if pass_last_use else None

            if not pass_last_use or pass_inactive_days > min_inactive_days:

                inactive_keys = []
                for key in self.client.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata']:
                    key_info = self.client.get_access_key_last_used(AccessKeyId=key['AccessKeyId'])['AccessKeyLastUsed']
                    
                    key_last_use = key_info.get('LastUsedDate', None)
                    key_inactive_days = (today - key_last_use.replace(tzinfo=None)).days if key_last_use else None

                    if not key_last_use or key_inactive_days > min_inactive_days:
                        key.update({'Inactive': not bool(key_last_use), 'LastUsed': key_last_use})
                        inactive_keys.append(key)
                
                if inactive_keys:
                    inactive_pass = {'Inactive': not bool(pass_last_use), 'LastUsed': pass_last_use}
                    inactive_user = { 'LoginActivity' : { 'Password' : inactive_pass, 'AccessKeys' : inactive_keys } }
                    user.update(inactive_user)
                    results.append(user)


        for user in self.get_users(): self.pool.add_task(worker, user)
        self.pool.wait_completion()
        
        return results

    def get_users(self):
        '''
        List all users for an AWS account

        Returns:
            List of all users
        '''
        results = []
        config = self.get_client_vars()

        paginator = self.client.get_paginator('list_users').paginate()
        for response in paginator:
            for user in response['Users']: results.append(user)

        return self.inject_client_vars(results, config)

    def __init__(self):
        AwsBase.__init__(self, 'iam')
