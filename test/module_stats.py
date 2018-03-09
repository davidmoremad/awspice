import unittest
import awspice

class ModuleStatsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nStarting unit tests of Module.Stats")

    def test_get_stats_of_region(self):
        aws = awspice.connect('eu-west-1', 'qa')
        stats = aws.stats.get_stats(regions=['eu-west-1'])
        self.assertTrue(isinstance(stats['Users'],list))
        self.assertTrue(isinstance(stats['Buckets'],list))
        self.assertTrue(isinstance(stats['Regions']['eu-west-1']['Instances'],list))
        self.assertTrue(isinstance(stats['Regions']['eu-west-1']['Volumes'],list))
        self.assertTrue(isinstance(stats['Regions']['eu-west-1']['SecurityGroups'],list))
        self.assertTrue(isinstance(stats['Regions']['eu-west-1']['Databases'],list))

    def test_get_stats_all_regions(self):
        aws = awspice.connect('eu-west-1', 'qa')
        stats = aws.stats.get_stats(regions='eu-west-1')
        self.assertTrue(isinstance(stats['Users'],list))
        self.assertTrue(isinstance(stats['Buckets'],list))
        self.assertTrue(isinstance(stats['Regions']['eu-west-1']['Instances'],list))
        self.assertTrue(isinstance(stats['Regions']['eu-west-1']['Volumes'],list))
        self.assertTrue(isinstance(stats['Regions']['eu-west-1']['SecurityGroups'],list))
        self.assertTrue(isinstance(stats['Regions']['eu-west-1']['Databases'],list))

    def test_cost_saving(self):
        aws = awspice.connect('eu-west-1')
        costs = aws.stats.cost_saving(regions='eu-west-1')
        self.assertTrue(isinstance(costs['Regions']['eu-west-1']['Volumes'],list))
        self.assertTrue(isinstance(costs['Regions']['eu-west-1']['Addresses'],list))
        self.assertTrue(isinstance(costs['Regions']['eu-west-1']['LoadBalancers'],list))


if __name__ == '__main__':
        unittest.main()
