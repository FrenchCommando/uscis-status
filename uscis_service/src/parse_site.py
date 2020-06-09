async def check(url_session, receipt_number):
    async with url_session.get(
        url='https://egov.uscis.gov/casestatus/mycasestatus.do',
        params={"appReceiptNum": receipt_number}
    ) as resp:
        time = resp.headers['date']
        d = await display_msg(resp.content)
        if d["ErrorMessage"]:
            return time, None, ''
        return time, d["LongCaseStatus"], d["StatusContent"]


async def display_msg(content):
    i = 0
    d = dict()
    async for line in content:
        if i == 598:
            # print(line)  # appReceiptNum
            d["appReceiptNum"] = line.decode("utf-8").split("\"")[1]
        elif i == 624:
            # print(line)  # Short Case Status
            d["ShortCaseStatus"] = line.decode("utf-8").strip()
        elif i == 637:
            # print(line)  # Long Case Status with h1
            d["LongCaseStatus"] = line.decode("utf-8").strip().split("<h1>")[1].split("</h1>")[0]
        elif i == 638:
            # print(line)  # Case Status Content p
            d["StatusContent"] = line.decode("utf-8").strip().split("<p>")[1].split("</p>")[0]
        elif i == 673:  # [671, 672, 673]:
            # print(line)  # formErrorMessages
            error_message = line.decode("utf-8").strip()
            d["ErrorMessage"] = error_message != '</div>'
            # '</div>'
            # '<h4>Validation Error(s)<br/>You must correct the following error(s) before proceeding:</h4>'
        # print(i, line)
        i += 1
    # print(d)
    return d


# 598 - var appReceiptNum = "LIN2015550570";
# 637 - <h1> Case Was Approved </h1>
# 638 - <p> On April28, 2020, we</p>
# 673 - <h4>Validation Error(s)<br/>You must correct the following error(s) before proceeding:</h4>
