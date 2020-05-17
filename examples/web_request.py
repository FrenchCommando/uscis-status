from src.parse_site import UscisInterface


interface = UscisInterface()

prefix = "LIN"
i = 2015550256
print(interface.check(receipt_number="{}{}".format(prefix, i)))
