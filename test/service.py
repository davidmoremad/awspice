import unittest
from awsmanager import AwsManager, ClsEncoder

class ServiceEc2TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nStarting unit tests of Service.EC2 ")

    #################################
    # -------- INSTANCES ---------- #
    #################################

    def test_get_auth_config(self):
        aws = AwsManager('eu-west-1', profile='default')
        self.assertEquals(aws.service.get_auth_config(), {'Authorization': {'Type':'Profile', 'Value': 'default'}})

if __name__ == '__main__':
        unittest.main()
