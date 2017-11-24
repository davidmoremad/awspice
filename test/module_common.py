import unittest
from awsmanager import AwsManager, ClsEncoder

class ModuleCommonTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nStarting unit tests of Module.Common")

    def test_get_elb_by_domain(self):
        aws = AwsManager('ap-southeast-1')
        elb = aws.common.get_balancer_by_domain('www.elevenpaths.com')
        self.assertEquals(elb['LoadBalancer']['DNSName'], 'elevenpaths-web-pro-1763591843.eu-west-1.elb.amazonaws.com')


if __name__ == '__main__':
        unittest.main()
