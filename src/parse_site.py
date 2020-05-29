from bs4 import BeautifulSoup
import datetime
import requests


def check(receipt_number):
    resp = requests.post(
        'https://egov.uscis.gov/casestatus/mycasestatus.do',
        data={
            "changeLocale": None,
            "completedActionsCurrentPage": 0,
            "upcomingActionsCurrentPage": 0,
            "appReceiptNum": receipt_number,
            "caseStatusSearchBtn": "CHECK STATUS"
        }
    )
    timestamp = f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S.%f}'
    return timestamp, *display_msg(resp.content)


def display_msg(resp):
    soup = BeautifulSoup(resp, features="html5lib")
    div = soup.find('div', attrs={'class': 'rows text-center'})
    return div.h1.string, "\t".join(map(str, div.p.contents))
