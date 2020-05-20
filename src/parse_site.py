from bs4 import BeautifulSoup
from mechanize import Browser
import datetime


class UscisInterface:
    url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'

    @staticmethod
    def check(receipt_number):
        browser = Browser()
        browser.open(UscisInterface.url)
        print(receipt_number, end="\t")
        browser.select_form(name="caseStatusForm")
        browser.form["appReceiptNum"] = receipt_number
        resp = browser.submit()
        timestamp = f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S.%f}'
        return timestamp, *UscisInterface.display_msg(resp)

    @staticmethod
    def display_msg(resp):
        soup = BeautifulSoup(resp, features="html5lib")
        div = soup.find('div', attrs={'class': 'rows text-center'})
        return div.h1.string, "\t".join(map(str, div.p.contents))

    @staticmethod
    def check_and_update(receipt_number):
        rep = UscisInterface.check(receipt_number=receipt_number)
