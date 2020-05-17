from bs4 import BeautifulSoup
from mechanize import Browser
import datetime


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
        timestamp = f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S.%f}'
        return timestamp, *UscisInterface.display_msg(resp)

    @staticmethod
    def display_msg(resp):
        soup = BeautifulSoup(resp, features="html5lib")
        div = soup.find('div', attrs={'class': 'rows text-center'})
        return div.h1.string, "\t".join(map(str, div.p.contents))

    def check_and_update(self, receipt_number):
        rep = self.check(receipt_number=receipt_number)
