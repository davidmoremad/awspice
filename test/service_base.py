import unittest
import re
from os.path import expanduser
import awspice

class ServiceBaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nStarting unit tests of Service.Base")


    def test_inject_client_vars(self):
        aws = awspice.connect('eu-west-1', 'qa')

        elements = [{'test': 1}, {'test': 2}]
        newelements = aws.service.ec2.inject_client_vars(elements)

        for el in newelements:
            self.assertEquals(el['RegionName'], 'eu-west-1')
            self.assertEquals(el['Authorization']['Type'], 'Profile')
            self.assertEquals(el['Authorization']['Value'], 'qa')




    ####################################
    # ~~~~~~~~~~~  PROFILES ~~~~~~~~~~ #
    ####################################

    def test_get_profiles(self):
        aws = awspice.connect('eu-west-1')
        profiles = sorted(aws.service.ec2.get_profiles())

        # GET profiles from file
        with open(expanduser("~") + "/.aws/credentials", 'r') as myfile:
            data = myfile.read().replace('\n', '')
        regex = re.compile(r'\[(?P<name>\w*)\]')
        credentials = sorted(regex.findall(data))

        self.assertEquals(profiles, credentials)

    def test_change_profile(self):
        aws = awspice.connect('eu-west-1')
        for profile in ['default', 'qa']:
            aws.service.ec2.change_profile(profile)
            profile = aws.service.get_auth_config()
            self.assertEquals(profile['Authorization']['Value'], profile['Authorization']['Value'])

    def test_parse_profiles_empty(self):
        aws = awspice.connect('eu-west-1', profile='qa')
        profiles = aws.service.ec2.parse_profiles([])
        self.assertEquals(profiles, ['qa'])

    def test_parse_profiles_list(self):
        aws = awspice.connect('eu-west-1', profile='qa')
        profiles = aws.service.ec2.parse_profiles(['qa', 'test'])
        self.assertEquals(profiles, ['qa', 'test'])

    def test_parse_profiles_string(self):
        aws = awspice.connect('eu-west-1', profile='qa')
        profiles = aws.service.ec2.parse_profiles('test_str')
        self.assertEquals(profiles, ['test_str'])

    def test_parse_profiles_string_ALL_hack(self):
        aws = awspice.connect('eu-west-1', profile='qa')
        profiles = sorted(aws.service.ec2.parse_profiles('ALL'))

        # GET profiles from file
        with open(expanduser("~") + "/.aws/credentials", 'r') as myfile:
            data = myfile.read().replace('\n', '')
        regex = re.compile(r'\[(?P<name>\w*)\]')
        credentials = sorted(regex.findall(data))

        self.assertEquals(profiles, credentials)




    ####################################
    # ~~~~~~~~~    REGIONS   ~~~~~~~~~ #
    ####################################

    def test_get_regions(self):
        aws = awspice.connect('eu-west-1')
        regions = [ 'us-east-1',
                    'us-east-2',
                    'us-west-1',
                    'us-west-2',
                    'eu-west-3',
                    'eu-west-1',
                    'eu-west-2',
                    'eu-central-1',
                    'ca-central-1',
                    'ap-south-1',
                    'ap-southeast-1',
                    'ap-southeast-2',
                    'ap-northeast-1',
                    'ap-northeast-2',
                    'sa-east-1']
        regions = sorted(regions)
        curregions = sorted([region['RegionName'] for region in aws.service.ec2.get_regions()])
        self.assertEquals(regions, curregions)

    def test_change_regions(self):
        aws = awspice.connect('eu-west-1')
        for region in ['eu-west-1','eu-west-2','eu-central-1']:
            aws.service.ec2.change_region(region)
            curRegion = aws.service.ec2.region
            self.assertEquals(curRegion, region)

    def test_parse_regions_empty(self):
        curRegion = 'eu-west-1'
        aws = awspice.connect(curRegion)
        results = sorted(aws.service.ec2.parse_regions([]))
        self.assertEquals(results[0]['RegionName'], aws.service.ec2.region)

    def test_parse_regions_empty_getALL(self):
        aws = awspice.connect('eu-west-1')
        regionsEmpty = []
        results = sorted(aws.service.ec2.parse_regions(regionsEmpty, True))
        allRegions = sorted(aws.service.ec2.get_regions())
        self.assertEquals(results, allRegions)

    def test_parse_regions_string(self):
        aws = awspice.connect('eu-west-1')
        regionsStr = 'eu-west-1'
        resultsStr = aws.service.ec2.parse_regions(regionsStr)
        self.assertEqual(resultsStr, [{'RegionName': 'eu-west-1'}])

    def test_parse_regions_list_strings(self):
        aws = awspice.connect('eu-west-1')
        regionsList = ['eu-west-1', 'eu-central-1']
        resultsList = aws.service.ec2.parse_regions(regionsList)
        self.assertIn({'RegionName':regionsList[0]}, resultsList)
        self.assertIn({'RegionName':regionsList[1]}, resultsList)



if __name__ == '__main__':
        unittest.main()
