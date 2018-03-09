import unittest
import awspice

class ServiceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nStarting unit tests of Service Class")

    #################################
    # -------- INSTANCES ---------- #
    #################################

    def test_get_auth_config(self):
        aws = awspice.connect('eu-west-1', profile='default')
        self.assertEquals(aws.service.get_auth_config(), {'Authorization': {'Type':'Profile', 'Value': 'default'}})

if __name__ == '__main__':
        unittest.main()
