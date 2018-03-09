import unittest
import random
import awspice

class ServiceS3TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nStarting unit tests of Service.S3 ")

    #################################
    # --------  BUCKETS  ---------- #
    #################################

    def test_get_public_buckets(self):
        aws = awspice.connect('eu-central-1')
        buckets = aws.service.s3.get_public_buckets()
        self.assertEquals(len(buckets), 1)


if __name__ == '__main__':
        unittest.main()
