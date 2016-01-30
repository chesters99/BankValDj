
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


#print(validate_card_number('49927398716'))
#print(validate_card_number('49927398717'))
#print(validate_card_number('1234567812345678'))
#print(validate_card_number('1234567812345670'))
