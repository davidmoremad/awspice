import unittest
import random
import awspice

class ServiceCeTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nStarting unit tests of Service.CE")

    def test_get_cost(self):
        time_from = '2018-02-01'
        time_to = '2018-02-28'
        aws = awspice.connect('eu-central-1')
        instance = aws.service.ec2.get_instance_by('id', 'i-0ac0ed3329e4114ae')
        cost = aws.service.ce.get_cost([instance['TagName']], time_from, time_to)
        self.assertGreater(float(cost[0]['Total']['UnblendedCost']['Amount']), 8.67)


if __name__ == '__main__':
        unittest.main()
