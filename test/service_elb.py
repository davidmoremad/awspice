import unittest
import random
import awspice

class ServiceElbTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nStarting unit tests of Service.ELB ")

    #################################
    # -------- BALANCERS ---------- #
    #################################

    def test_get_loadbalancers(self):
        aws = awspice.connect('eu-central-1')
        elbs = aws.service.elb.get_loadbalancers()
        self.assertTrue(len(elbs) ==20)

    def test_get_loadbalancer_by(self):
        aws = awspice.connect('eu-central-1')
        elb = aws.service.elb.get_loadbalancer_by('domain', 'aws.elevenpaths.com')
        self.assertEquals(elb['CanonicalHostedZoneName'], 'elevenpaths-web-pro-1763591843.eu-west-1.elb.amazonaws.com')


if __name__ == '__main__':
        unittest.main()
