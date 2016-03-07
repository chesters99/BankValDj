.. _validator-ref:

Bank Account Validator
----------------------
.. code-block:: python
   :linenos:

   from accounts.utils.BankValidator import Validator
   bv = Validator()
   result = bv.validate(sort_code, account)
   if not result:
       print (bv.message)
