import unittest
import random
import awspice

class ServiceEc2TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nStarting unit tests of Service.EC2 ")

    #################################
    # -------- INSTANCES ---------- #
    #################################

    def test_get_instances(self):
        aws = awspice.connect('eu-west-1')
        instances = aws.service.ec2.get_instances()
        self.assertTrue(len(instances) > 15)

    def test_get_instance_by(self):
        aws = awspice.connect('eu-west-2')
        instance = aws.service.ec2.get_instance_by('id', 'i-541f08dc', regions=['eu-west-1','eu-west-2'])
        self.assertEquals(instance['State']['Name'], 'running')

    def test_get_instances_by(self):
        aws = awspice.connect('eu-west-1')
        instances = aws.service.ec2.get_instances_by('status', 'running', regions=['eu-west-1','eu-west-2'])
        for instance in instances:
            self.assertEquals(instance['State']['Name'], 'running')

    def test_set_tag(self):
        aws = awspice.connect('eu-west-1')
        rnd = random.choice('abcdefghij')
        results = aws.service.ec2.set_tag(['i-056811c5f5e5fff57'], 'Test', 'david_amrani' + rnd , regions=['eu-west-1', 'eu-central-1'])


    #################################
    # ---------- VOLUMES ---------- #
    #################################

    def test_get_volumes(self):
        aws = awspice.connect('eu-west-1')
        vols = aws.service.ec2.get_volumes()
        inst = aws.service.ec2.get_instances()
        self.assertTrue(len(vols) > len(inst))


    def test_get_volumes_by(self):
        aws = awspice.connect('eu-west-1')
        volumes = aws.service.ec2.get_volumes_by('status', 'available')
        self.assertEquals(volumes[0]['State'], 'available')


    def test_get_volume_by(self):
        aws = awspice.connect('eu-west-1')
        volume = aws.service.ec2.get_volume_by('status', 'in-use')
        self.assertTrue('i-' in volume['Attachments'][0]['InstanceId'])



    # #################################
    # ----------- ADDRESSES -----------
    # #################################

    def test_get_addresses(self):
        aws = awspice.connect('eu-west-1')
        addresses = aws.service.ec2.get_addresses(regions=['eu-west-1'])
        addresses = filter(lambda x: x.get('AssociationId') != None, addresses)
        self.assertTrue(len(addresses) > 20)

    def test_get_address_by(self):
        aws = awspice.connect('eu-west-1')
        address = aws.service.ec2.get_address_by('privateip', '172.22.1.221', regions=['eu-west-1'])
        self.assertTrue(address['PublicIp'], '52.214.252.60')



if __name__ == '__main__':
        unittest.main()
