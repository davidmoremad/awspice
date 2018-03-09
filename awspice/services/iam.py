# -*- coding: utf-8 -*-
from base import AwsBase

class IamService(AwsBase):
    '''
    Class belonging to the IAM Identity & Access management service.
    '''

    def get_users(self):
        '''
        List all users for an AWS account

        Returns:
            List of all users
        '''
        user_list = []

        paginator = self.client.get_paginator('list_users')

        for response in paginator.paginate():
            for user in response['Users']:
                user_list.append(user)

        return user_list

    def __init__(self):
        AwsBase.__init__(self, 'iam')
