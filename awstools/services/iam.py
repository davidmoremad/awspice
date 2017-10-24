# -*- coding: utf-8 -*-
from base import AwsBase

class IamManager(AwsBase):

    def get_users(self):
        '''
        List all users for an AWS account

        Returns:
            List of all users
        '''
        user_list = []

        iam = boto3.client('iam')
        paginator = iam.get_paginator('list_users')

        for response in paginator.paginate():
            for user in response['Users']:
                user_list.append(user)

        return user_list
