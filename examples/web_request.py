from src.parse_site import check as uscis_check

prefix = "LIN"
i = 2015550256

for i in [2015550118, 2000150095, 2015550507, 2000150097, 2000150098]:  # range(2015550256, 2015550656):
    receipt_number = "{}{}".format(prefix, i)
    print(uscis_check(receipt_number=receipt_number))
