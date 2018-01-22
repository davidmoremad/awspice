===============
Getting started
===============

.. requirements-section

************
Requirements
************

Awspice is an abstraction layer of AWS, so it will be necessary to meet the following requirements:

+---------------------+-------------------------------------------------------------+
| We just need ...    | And it means...                                             |
+=====================+=============================================================+
| **AWS account**     | Have an Amazon Web Services account of any kind             |
+---------------------+-------------------------------------------------------------+
| **IAM user**        | Enabled user with programmatic keys (access and secret key) |
+---------------------+-------------------------------------------------------------+
| **Permissions**     | Have permissions in the services and regions to use         |
+---------------------+-------------------------------------------------------------+


------------------------------------------------------------------------------------------

.. installation-section

************
Installation
************

.. code-block:: bash

  pip install git+https://github.com/davidmoremad/awsmanager.git@<VERSION>


------------------------------------------------------------------------------------------

.. configuration-section

*************
Configuration
*************

The client is built and configured using ``awspice.connect()``. This method indicates the type of authentication and region on which you are going to work.
There are two ways to set your credentials *(Only one of the two can be used)*:
* **Profile** *(Recommended)* ─ The access keys are stored in ``~/.aws/credentials`` file. (`Read more <https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html>`_)
* **Access keys** ─ Typing the hard-coded access keys.

+-----------------+-----------------+-------------------------------------------------+
| Parameter name  | Default value   | Description                                     |
+=================+=================+=================================================+
| region          | eu-west-1       | Region on which you are going to work.          |
+-----------------+-----------------+-------------------------------------------------+
| profile         | default         | Name of the profile in ~/.aws/credentials file  |
+-----------------+-----------------+-------------------------------------------------+
| access_key      |                 | User API access key                             |
+-----------------+-----------------+-------------------------------------------------+
| secret_key      |                 | User API secret key                             |
+-----------------+-----------------+-------------------------------------------------+


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
