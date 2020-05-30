from bs4 import BeautifulSoup
import datetime


async def check(url_session, receipt_number):
    async with url_session.get(
            url='https://egov.uscis.gov/casestatus/mycasestatus.do',
            params={
                    "appReceiptNum": receipt_number,
            }) as resp:
        timestamp = f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S.%f}'
        text = await resp.text()
        display_result = await display_msg(text)
        return timestamp, *display_result


async def display_msg(text):
    soup = BeautifulSoup(text, features="html5lib")
    error_message = soup.find(id="formErrorMessages")
    if len(error_message.contents) > 1:
        return None, ''
    div = soup.find('div', attrs={'class': 'rows text-center'})
    return div.h1.string, "\t".join(map(str, div.p.contents))
