AWSManager 2.0
============

AWSManager is a wrapper tool of Boto3 library to list inventory of your AWS infrastructure

- [AWSManager 2.0](#awsmanager-10)
  * [What is?](#what-is-)
  * [Installation](#installation)
  * [Usage](#usage)
    + [Authentication](#authentication)
    + [Getting service data](#getting-service-data)
    + [Highlevel functions](#highlevel-functions)
    + [Using boto3 client](#use-boto3-client)
  * [FAQs](#faqs)
    + [TypeError: datetime is not JSON serializable](#typeerror--datetime-is-not-json-serializable)

What is?
--------

The objective of the wrapper is to abstract the use of AWS, being able
to dig through all the data of our account. This allows us for example:

-   Search for a specific instance in all accounts and regions.
-   Filter important services exposed to internet (ssh, rdp).
-   Save costs by finding unused IPs, unattached volumes or ELB without instances.

Installation
------------

**Using pip**

``` {.sourceCode .python}
pip install git+https://github.com/davidmoremad/awsmanager.git#egg=awsmanager
```

**Manually**

``` {.sourceCode .python}
git clone https://github.com/davidmoremad/awsmanager.git#egg=awsmanager
cd awsmanager
pip install -r requirements.txt
```

Usage
------

### Authentication

AwsManager uses 3 authentication methods with the following priority:

1)  **Profile** (param:profile) - Name of the aws profile set in
    \~/.aws/credentials file
2)  **Access keys** (param:access\_key, param:secret\_key) - API access
    keys of your AWS account
3)  **Empty** - It uses default authentication method of Boto3 (Env.
    variables and default profile in \~/.aws/credentials file)

``` {.sourceCode .python}
awsmanager = AwsManager(region='eu-west-1')
awsmanager = AwsManager(region='eu-west-1', profile="it_account07")
awsmanager = AwsManager(region='eu-west-1', access_key="XXXXXXXXX", secret_key="YYYYYYYYYYY")
```

### Getting service data

``` {.sourceCode .python}
ec2s = awsmanager.service.s3.get_all_instances()     # Get all instances of all regions
vols = awsmanager.service.ec2.get_volumes_by('status', 'available')
adds = awsmanager.service.ec2.get_addresses()
elbs = awsmanager.service.elb.get_elbs()
rdss = awsmanager.service.rds.get_rdss()
s3s  = awsmanager.service.s3.get_buckets()
```

### Highlevel functions

In addition to the individual use of the services, you can also make use of higher level functions such as:
* Cost savings module: Lists all volumes, IP addresses and balancers that are not being used and therefore consume economic resources.
* Statistics module: It obtains general data of several services of a specific region or of all, such as databases, volumes, instances, balancers, snapshots...
* Location of elements: It allows locating instances, volumes or other elements in different regions or even different accounts if authentication is iterated.


``` {.sourceCode .python}
stats = aws.get_stats()
costs = aws.cost_savings()
ports = aws.get_ports_by_instance('i-0123456789')
```

You can locate instances, volumes, snapshots or other elements in the following way:
``` {.sourceCode .python}
instance = aws.find_instance('privateip', '172.16.11.50')
if instance: print instance['RegionName']
```

### Using boto3 client

Just use property client of any service:
```{.sourceCode .python}
awsmanager = AwsManager('eu-west-1')

instance_status = awsmanager.service.ec2.client.describe_instance_status(InstanceIds=['i-1234567890'])
```


FAQs
----

### TypeError: datetime is not JSON serializable

Boto3 returns the following datetime format: datetime(2012, 8, 8, 21, 46). To avoid this exception just need to use the following code:

``` {.sourceCode .python}
from awsmanager import ClsEncoder                          # Import util Encoder

instances = awsmanager.service.ec2.get_instances()         # Returns json not serializable
results = json.dumps(instances, indent=4, cls=ClsEncoder)  # Serializer
```
