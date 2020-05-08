from bs4 import BeautifulSoup
from mechanize import Browser


class UscisInterface:
    def __init__(self):
        url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
        self.browser = Browser()
        self.browser.open(url)

    def check(self, receipt_number):
        print(receipt_number, end="\t")
        self.browser.select_form(name="caseStatusForm")
        self.browser.form["appReceiptNum"] = receipt_number
        resp = self.browser.submit()
        return UscisInterface.display_msg(resp)

    @staticmethod
    def display_msg(resp):
        soup = BeautifulSoup(resp, features="html5lib")
        div = soup.find('div', attrs={'class': 'rows text-center'})
        return div.h1.string, "\t".join(map(str, div.p.contents))


if __name__ == "__main__":
    interface = UscisInterface()

    prefix = "LIN"
    for i in range(2015550000, 2015550250):
        print(interface.check(receipt_number="{}{}".format(prefix, i)))
