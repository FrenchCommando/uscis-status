from src.parse_site import check as uscis_check

prefix = "LIN"
i = 2015550256

for i in range(2015550256, 2015550356):
    receipt_number = "{}{}".format(prefix, i)
    print(uscis_check(receipt_number=receipt_number))
