from bs4 import BeautifulSoup
import datetime
import asyncio


async def check(url_session, receipt_number):
    async with url_session.get(
        url='https://egov.uscis.gov/casestatus/mycasestatus.do',
        params={
            "appReceiptNum": receipt_number,
        }
    ) as resp:
        timestamp = f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S.%f}'
        text = await resp.text()
        display_result = await display_msg(text)
        return timestamp, *display_result


async def display_msg(text):
    loop = asyncio.get_event_loop()
    soup = await loop.run_in_executor(None, BeautifulSoup, text, 'html5lib')
    error_message = soup.find(id="formErrorMessages")
    if len(error_message.contents) > 1:
        return None, ''
    div = soup.find('div', attrs={'class': 'rows text-center'})
    status = div.h1.string
    msg = "\t".join(map(str, div.p.contents))
    return status, msg


# var appReceiptNum = "LIN2015550570";
# <h1> Case Was Approved </h1>
# <p> On April28, 2020, we</p>
# <h4>Validation Error(s)<br/>You must correct the following error(s) before proceeding:</h4>
