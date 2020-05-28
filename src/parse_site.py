from bs4 import BeautifulSoup
from mechanize import Browser
import datetime


url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'


def check(receipt_number):
    browser = Browser()
    # browser.set_handle_robots(False)
    # browser.addheaders = \
    #     [('User-agent',
    #       'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    browser.open(url)
    print(receipt_number, end="\t")
    browser.select_form(name="caseStatusForm")
    browser.form["appReceiptNum"] = receipt_number
    resp = browser.submit()
    timestamp = f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S.%f}'
    return timestamp, *display_msg(resp)


def display_msg(resp):
    soup = BeautifulSoup(resp, features="html5lib")
    div = soup.find('div', attrs={'class': 'rows text-center'})
    return div.h1.string, "\t".join(map(str, div.p.contents))
