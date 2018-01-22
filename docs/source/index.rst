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


.. include:: getting_started.rst
  :start-after: installation-section
  :end-before: configuration-section


*************
Configuration
*************

The client is built and configured using ``awspice.connect()``. This method indicates the type of authentication and region on which you are going to work.


.. code-block:: python

  import awspice

  aws = awspice.connect() # Region: eu-west-1 | Profile: Default

  aws = awspice.connect(region='us-west-2', profile='dev_profile')
  aws = awspice.connect('us-west-2', access_key='AKIA***********', secret_key='/HR$4************')


`Read more <getting_started.html>`_

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
