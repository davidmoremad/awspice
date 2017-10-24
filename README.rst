AWSTools
==============

AWSTools is a wrapper tool of Boto3 library to list inventory of your AWS infrastructure


Installation
-----------------

**Using pip**

.. code-block:: none

    pip install git+https://github.com/davidmoremad/awstools.git#egg=awstools

**Manually**

.. code-block:: none

    git clone https://github.com/davidmoremad/awstools.git#egg=awstools
    cd awstools
    pip install -r requirements.txt

Use
-----
The objective of the wrapper is to abstract the use of AWS, being able to dig through all the data of our account. This allows us for example:

- Search for a specific instance in all accounts and regions.
- Filter important services exposed to internet (ssh, rdp).
- Save costs by finding unused IPs, unattached volumes or ELB without instances.
