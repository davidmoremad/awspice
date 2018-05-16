import unittest
import awspice

class ModuleFinderTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nStarting unit tests of Module.Find_Elements")


    def test_find_instance_accounts(self):
        aws = awspice.connect('eu-west-2')
        instance = aws.finder.find_instance('id', 'i-541f08dc', profiles=['qa', 'default'])
        self.assertEquals(instance['InstanceId'], 'i-541f08dc')

    def test_find_instance_regions(self):
        aws = awspice.connect('eu-west-2', profile='default')
        instance = aws.finder.find_instance('id', 'i-541f08dc',regions=['eu-west-1'])
        self.assertEquals(instance['InstanceId'], 'i-541f08dc')

    def test_find_instances(self):
        aws = awspice.connect('eu-west-1')
        instances = aws.finder.find_instances('status', 'running', profiles=['qa'])
        self.assertEquals(instances[0]['State']['Name'], 'running')
        # Verify regions=[] == all regions
        q_regions = map(lambda x: x['RegionName'], instances)
        map(lambda x: self.assertTrue(x in ['eu-central-1', 'eu-west-1']), q_regions)


    def test_find_volume(self):
        aws = awspice.connect('eu-west-1')
        volume = aws.finder.find_volume('id', 'vol-04ee612f6b83104cd', profiles=['default', 'qa'])
        self.assertEquals(volume['State'], 'in-use')

    def test_find_volumes(self):
        aws = awspice.connect('eu-west-1')
        volumes = aws.finder.find_volumes('status', 'in-use', profiles=['qa'])
        self.assertEquals(volumes[2]['State'], 'in-use')



if __name__ == '__main__':
        unittest.main()
