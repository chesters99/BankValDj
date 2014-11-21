""" Luhn Method to validate credit card number """

def validate_card_number(card_number):
    total = 0
    odd = 1
    length = len(card_number)
    lookup = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
    for count in range(length-1, -1, -1):
        digit = int(card_number[count])
        total += digit if odd else lookup[digit]
        odd = not odd
    return (total % 10) == 0


print(validate_card_number('49927398716'))
print(validate_card_number('49927398717'))
print(validate_card_number('1234567812345678'))
print(validate_card_number('1234567812345670'))


# NOTES on credit card processing:
# set autocomplete = off on credit card fields
# set the following in the header
# <meta http-equiv="cache-control" content ="no-cache">
# <meta http-equiv="pragma" content ="no-cache">
# <meta http-equiv="refresh" content ="7200">
# set at the start of the checkout view
# request.session.set_expiry(7200)
# flag @sensitive_post_parameters on the method to obscure credit card info
#
#
