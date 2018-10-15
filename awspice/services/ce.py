# -*- coding: utf-8 -*-
from base import AwsBase
import datetime

class CostExplorerService(AwsBase):
    '''
    Class belonging to the Cost Explorer service.
    '''

    granularities = ['DAILY', 'MONTHLY']
    filter_dimensions = ['AZ', 'INSTANCE_TYPE', 'LINKED_ACCOUNT', 'OPERATION', 'PURCHASE_TYPE', 'REGION', 'SERVICE', 'USAGE_TYPE', 'USAGE_TYPE_GROUP', 'RECORD_TYPE', 'OPERATING_SYSTEM', 'TENANCY', 'SCOPE', 'PLATFORM', 'SUBSCRIPTION_ID', 'LEGAL_ENTITY_NAME', 'DEPLOYMENT_OPTION', 'DATABASE_ENGINE', 'CACHE_ENGINE', 'INSTANCE_TYPE_FAMILY']
    group_dimensions = ['AZ', 'INSTANCE_TYPE', 'LEGAL_ENTITY_NAME', 'LINKED_ACCOUNT', 'OPERATION', 'PLATFORM', 'PURCHASE_TYPE', 'SERVICE', 'TAGS', 'TENANCY', 'USAGE_TYPE']

    def get_cost(self, from_date=None, to_date=None, interval="Monthly", group_by='', filter_by={}, ec2_running_hours=False):
        '''
        Get the cost of account or its elements.

        This method obtains costs of an account/s , one or several elements (substances, balancers, addresses)
        between two dates and granularized in days or months.
        If the date is not indicated, the cost of the last month will be returned.

        Args:
            from_date (str): Date from which you want to obtain data. (Format: 2018-04-24)
            to_date (str): Date until which you want to obtain data. (Format: 2018-04-24)
            interval (str): Time interval to be analyzed. [ MONTHLY | DAILY ]
            group_by (str): Group results by ['AZ', 'INSTANCE_TYPE', 'LEGAL_ENTITY_NAME', 'LINKED_ACCOUNT', 'OPERATION', 'PLATFORM', 'PURCHASE_TYPE', 'SERVICE', 'TAGS', 'TENANCY', 'USAGE_TYPE']
            filter_by (dict): Key of the filter and value. {'TAG_NAME': ['ec2-tagname', 'LINKED_ACCOUNT: ['1234']]}

        Examples:
            get_cost(['machine-1', 'machine-2'], '2018-12-24', '2018-12-26', interval='daily')
            get_cost() # Get account cost

        Returns:
            Costs (list): List of days or months with the requested costs
        '''
        # If the dates are empty, extract data from the last month.
        if from_date is None and to_date is None:
            from_date = (datetime.datetime.now() - datetime.timedelta(1*365/12)).replace(day=1).strftime('%Y-%m-%d')
            to_date = datetime.datetime.now().replace(day=1).strftime('%Y-%m-%d')

        # Parameters validation
        try:
            datetime.datetime.strptime(from_date, '%Y-%m-%d')
            datetime.datetime.strptime(to_date, '%Y-%m-%d')
            assert interval.upper() in self.granularities, "interval. Valid values are %s" % str(self.granularities)
            assert isinstance(group_by, str), "group_by. Valid values are %s" % str(self.group_dimensions)
            assert isinstance(filter_by, dict), "filter_by. Valid values are %s" % str(self.filter_dimensions)
        except Exception as e:
            raise ValueError("Invalid parameter: " + str(e))

        timeperiod = {'Start': from_date , 'End': to_date}
        if ec2_running_hours: filter_by['USAGE_TYPE_GROUP'] = 'EC2: Running Hours'
        filters = self._format_filters(filter_by)
        groups  = self._format_groups(group_by)

        if filters:
            results = self.client.get_cost_and_usage(TimePeriod=timeperiod,
                                                    Granularity=interval.upper(),
                                                    Filter=filters,
                                                    Metrics=['UnblendedCost'],
                                                    GroupBy=groups)
        else:
            results = self.client.get_cost_and_usage(TimePeriod=timeperiod,
                                                    Granularity=interval.upper(),
                                                    Metrics=['UnblendedCost'],
                                                    GroupBy=groups)
        return results['ResultsByTime']
        

    def _format_groups(self, group):
        """Give the correct format to groups for get_cost function
        
        Args:
            group (str): Type of group to filter
        
        Returns:
            list: Well-formatted keys and values of groups 
        """
        result = []
        if group:
            if group.upper() in self.group_dimensions:
                result = [{'Type': 'DIMENSION', 'Key': group.upper()}]
            else:
                raise ValueError("%s is not a valid filter to group by" % group)
        return result


    def _format_filters(self, filters):
        """Give the correct format to filters for get_cost function
        
        Args:
            filters {dict}: Key and values of your filters

        Raises:
            ValueError: Invalid filter key passed.
        
        Returns:
            dict -- Well-formatted keys and values of filters
        """
        args = filters.keys()
        result = {}
        if len(args) == 1:
            for key, value in filters.iteritems():
                tagvalue = value if isinstance(value, list) else [value]
                if key.upper().startswith('TAG_'):
                    tagkey = key[4:].title()
                    result['Tags'] = {'Key': tagkey, 'Values': tagvalue}
                elif key.upper() in self.filter_dimensions:
                    result['Dimensions'] = {'Key': key.upper(), 'Values': tagvalue}
                else:
                    raise ValueError('Invalid filter. Allowed filters: %s' % str(self.filter_dimensions))
        elif len(args) > 1:
            result['And'] = list()
            for key, value in filters.iteritems():
                result['And'].append(self._format_filters({key: value}))
        return result

    def __init__(self):
        AwsBase.__init__(self, 'ce')
        self.change_region('us-east-1')
