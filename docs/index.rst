.. BankValDj documentation master file, created by
   sphinx-quickstart on Sat Aug 23 13:31:27 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

UK Bank Account Validation
==========================

Contents:

.. contents::

Validator
---------
.. code-block:: python
   :linenos:

   from accounts.utils.BankValidator import Validator
   bv = Validator()
   result = bv.validate(sort_code, account)
   if not result:
       print (bv.message)

Models
------
.. automodule:: main.models
    :members:

.. automodule:: rules.models
    :members:

Views
-----
.. automodule:: main.views
    :members:

.. automodule:: rules.views
    :members:


Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Overview
--------
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
Curabitur pretium tincidunt lacus. Nulla gravida orci a odio. Nullam varius, turpis et
commodo pharetra, est eros bibendum elit, nec luctus magna felis sollicitudin mauris.
