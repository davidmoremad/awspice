Awspice
=======

.. image:: https://readthedocs.org/projects/awsmanager/badge/?version=latest
  :target: http://awsmanager.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status


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

************
Installation
************

.. code-block:: bash

  pip install git+https://github.com/davidmoremad/awsmanager.git@<VERSION>

------------------------------------------------------------------------------------------

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

*******
Test it
*******

To verify that the configuration has been correctly stored, you can run the following test.
This test only checks that your user is registered and enabled on the AWS account set in the client's configuration.

.. code-block:: python

  import awspice

  aws = awspice.connect(profile='<YOUR_PROFILE>')
  aws.test()
