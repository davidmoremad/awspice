.. awspice documentation master file, created by
   sphinx-quickstart on Fri Jan 19 21:22:34 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to awspice's documentation!
===================================


.. toctree::
  :hidden:
  :maxdepth: 0
  :caption: Contents:

  Getting started <getting_started.rst>
  Services <services.rst>
  FAQs & Troubleshooting <troubleshooting.rst>

.. toctree::
  :hidden:
  :maxdepth: 0
  :caption: Site map:

  Awspice Module <modules.rst>


.. shields-section


|Docs| |Version|


.. |Docs| image:: https://readthedocs.org/projects/awspice/badge/?version=latest
   :target: http://awspice.readthedocs.io/en/latest/?badge=latest
   :alt: Read the Docs
.. |Version| image:: http://img.shields.io/pypi/v/awspice.svg?style=flat
    :target: https://pypi.python.org/pypi/awspice/
    :alt: Version

.. intro-section


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

.. include:: getting_started.rst
  :start-after: installation-section
  :end-before: configuration-section




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

.. include:: getting_started.rst
  :start-after: test-section


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`

------------------------------------------------------------------------------------------

Contact me
----------

| **Author**: David Amrani Hernández
| **Github**: `@davidmoremad <https://github.com/davidmoremad>`_
