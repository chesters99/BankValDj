Test Django Application
=======================

UK Bank Account validation website, built as a learning exercise for Django

Validator
---------
.. code-block:: python
   :linenos:

   from accounts.utils.BankValidator import Validator
   bv = Validator()
   result = bv.validate(sort_code, account)
   if not result:
       print (bv.message)

NB: The site is completely pointless...