Awspice
=======


|Docs| |Version| |Codacy|


.. |Docs| image:: https://readthedocs.org/projects/awspice/badge/?version=latest
   :target: http://awspice.readthedocs.io/en/latest/?badge=latest
   :alt: Read the Docs
.. |Version| image:: http://img.shields.io/pypi/v/awspice.svg?style=flat
    :target: https://pypi.python.org/pypi/awspice/
    :alt: Version
.. |Codacy| image:: https://api.codacy.com/project/badge/Grade/827a55c2ed47488c8e642fe799028319
    :target: https://www.codacy.com/app/davidmoremad/awspice?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=davidmoremad/awspice&amp;utm_campaign=Badge_Grade
    :alt: Codacy

Table of content (Full doc in `ReadTheDocs <http://awspice.readthedocs.io/en/latest/>`_) :

* `Installation <#installation>`_
* `Configuration <#configuration>`_
* `Test <#test>`_
* `Usage <#usage>`_


****************
What is Awspice?
****************

Is a wrapper tool of Boto3 library to list inventory and manage your AWS infrastructure
The objective of the wrapper is to abstract the use of AWS, being able to dig through all the data of our account,
and for example you will be able of:

* Run a ssh-command for all instances in all regions
* List all instances with exposed critical ports like 22 or 3389
* Get info about all certificates of your account/s
* Obtain all the infrastructure after a domain associated with a balancer

------------------------------------------------------------------------------------------

.. installation-section

************
Installation
************

.. code-block:: bash

  pip install awspice

------------------------------------------------------------------------------------------

.. configuration-section

*************
Configuration
*************

The client is built and configured using ``awspice.connect()``. This method indicates the type of authentication and region on which you are going to work.


.. code-block:: python

  import awspice

  aws = awspice.connect() # Region: eu-west-1 | Profile: Default

  aws = awspice.connect(region='us-west-2', profile='dev_profile')
  aws = awspice.connect('us-west-2', access_key='AKIA***********', secret_key='/HR$4************')


------------------------------------------------------------------------------------------

.. test-section

*******
Test it
*******

To verify that the configuration has been correctly stored, you can run the following test.
This test only checks that your user is registered and enabled on the AWS account set in the client's configuration.

.. code-block:: python

  import awspice

  aws = awspice.connect(profile='<YOUR_PROFILE>')
  aws.test()



------------------------------------------------------------------------------------------

.. usage-section

*****
Usage
*****

**Example**: Get balancer and instances behind a domain.

.. code-block:: python

  aws = awspice.connect()

  elb = aws.service.elb.get_loadbalancer_by('domain', 'choosetravel.es')
  for elb_instance in elb['Instances']:
    instance = aws.service.ec2.get_instance_by('id', elb_instance['InstanceId'])


**Example**: List all unused volumes

.. code-block:: python

  regions = aws.service.ec2.get_regions()
  volumes = awsmanager.service.ec2.get_volumes_by('status', 'available', regions=regions)


**Example**: Search instance in all accounts and regions by Public IP

.. code-block:: python

  profiles = aws.service.ec2.get_profiles()
  regions = aws.service.ec2.get_regions()

  for profile in profiles:
      aws.service.ec2.change_profile(profile)

      instance = aws.service.ec2.get_instance_by('publicip', '35.158.163.235', regions=regions)

      if instance:
          print 'Instance found: %s (Account: %s, Region: %s)' % (instance['InstanceId'], instance['RegionName'], instance['Authorization']['Value'])
          break
