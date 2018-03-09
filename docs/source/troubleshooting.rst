

======================
FAQs & Troubleshooting
======================

**************************
Frequently Asked Questions
**************************


Running Tests
---------------

At the moment this functionality is not available as they have not been mocked.

.. code-block:: bash

  $ pip install -r requirements.txt
  $ python -m unittest -v test



Generating Documentation
------------------------

Sphinx is used for documentation. You can generate HTML locally with the following:


.. code-block:: bash

  $ pip install -r requirements_dev.txt
  $ cd docs
  $ make html



***************
Troubleshooting
***************


TypeError: datetime is not JSON serializable
--------------------------------------------
Sometimes Boto3 returns a non-serializable result to JSON and we get the following error when dumping that result:
``TypeError: datetime.datetime (2015, 12, 3, 21, 20, 17, 326000, tzinfo = tzutc ()) is not JSON serializable``

You can solve it using this encoder in the following way:

.. code-block:: python

  import awspice

  json.dumps(json, indent=4, cls=awspice.ClsEncoder)
