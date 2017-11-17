import unittest
from awsmanager import AwsManager, ClsEncoder

class ModuleFinderTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nStarting unit tests of Module.Find_Elements")


    def test_find_instance_accounts(self):
        aws = AwsManager('eu-west-2')
        instance = aws.finder.find_instance('id', 'i-541f08dc', accounts=['qa', 'default'])
        self.assertEquals(instance['InstanceId'], 'i-541f08dc')

    def test_find_instance_regions(self):
        aws = AwsManager('eu-west-2', profile='default')
        instance = aws.finder.find_instance('id', 'i-541f08dc',regions=['eu-west-1'])
        self.assertEquals(instance['InstanceId'], 'i-541f08dc')

    def test_find_instances(self):
        aws = AwsManager('eu-west-1')
        instances = aws.finder.find_instances('status', 'running', accounts=['qa'])
        self.assertEquals(instances[0]['RegionName'], 'eu-west-1')
        self.assertEquals(instances[0]['State']['Name'], 'running')


    def test_find_volume(self):
        aws = AwsManager('eu-west-1')
        volume = aws.finder.find_volume('id', 'vol-04ee612f6b83104cd', accounts=['default', 'qa'])
        self.assertEquals(volume['State'], 'in-use')

    def test_find_volumes(self):
        aws = AwsManager('eu-west-1')
        volumes = aws.finder.find_volumes('status', 'in-use', accounts=['qa'])
        self.assertEquals(volumes[2]['State'], 'in-use')



if __name__ == '__main__':
        unittest.main()
