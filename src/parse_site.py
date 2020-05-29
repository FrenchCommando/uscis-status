from bs4 import BeautifulSoup
import datetime
import requests


def check(receipt_number):
    resp = requests.get(
        url='https://egov.uscis.gov/casestatus/mycasestatus.do',
        params={
            "appReceiptNum": receipt_number,
        }
    )
    timestamp = f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S.%f}'
    return timestamp, *display_msg(resp.content)


def display_msg(resp):
    soup = BeautifulSoup(resp, features="html5lib")
    div = soup.find('div', attrs={'class': 'rows text-center'})
    return div.h1.string, "\t".join(map(str, div.p.contents))
