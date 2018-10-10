# -*- coding: utf-8 -*-
from base import AwsBase
import datetime

class CostExplorerService(AwsBase):
    '''
    Class belonging to the Cost Explorer service.
    '''

    def get_cost(self, from_date=None, to_date=None, tag_names=None, interval="Monthly"):
        '''
        Get the cost of item/s by its tag "Name".

        This method obtains the price of one or several elements (substances, balancers, addresses)
        between two dates and granularized in days or months.
        If the date is not indicated, the cost of the last month will be returned.

        Args:
            from_date (str): Date from which you want to obtain data. (Format: 2018-04-24)
            to_date (str): Date until which you want to obtain data. (Format: 2018-04-24)
            tagnames (lst): List of tag names of elements to obtain data (wildcards are not valid)
            interval (str): Time interval to be analyzed. [ MONTHLY | DAILY ]

        Examples:
            get_cost(['machine-1', 'machine-2'], '2018-12-24', '2018-12-26', interval='daily')
            get_cost() # Get account cost

        Returns:
            Costs (list): List of days or months with the requested costs
        '''

        # If the dates are empty, extract data from the last month.
        if from_date is None and to_date is None:
            from_date = (datetime.datetime.now() -
                datetime.timedelta(1*365/12)).replace(day=1).strftime('%Y-%m-%d')
            to_date = datetime.datetime.now().replace(day=1).strftime('%Y-%m-%d')

        # Parameters validation
        try:
            datetime.datetime.strptime(from_date, '%Y-%m-%d')
            datetime.datetime.strptime(to_date, '%Y-%m-%d')
            if not interval.upper() in ["DAILY", "MONTHLY"]:
                raise AssertionError()
        except:
            raise ValueError("Invalid parameters")

        timeperiod = {'Start': from_date , 'End': to_date}
        filters = {"Tags": {"Key": "Name", "Values": tag_names}} if tag_names else None

        if filters:
            results = self.client.get_cost_and_usage(TimePeriod=timeperiod,
                                                    Granularity=interval.upper(),
                                                    Filter=filters,
                                                    Metrics=['UnblendedCost'])
        else:
            results = self.client.get_cost_and_usage(TimePeriod=timeperiod,
                                                    Granularity=interval.upper(),
                                                    Metrics=['UnblendedCost'])
        return results['ResultsByTime']


    def __init__(self):
        AwsBase.__init__(self, 'ce')
        self.change_region('us-east-1')
