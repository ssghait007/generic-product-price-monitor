import requests
from bs4 import BeautifulSoup
from lxml import etree
import smtplib
import sys


from alerthelper import email_alert, slack_alert, email_and_slack_alert

arg_error = """
This script requires below input arguments 
1. URL of the product page
2. XPATH of the price element
3. Price threshold, if price goes below this alert is triggered
4. Alert type - email / slack / email+slack
"""


if len(sys.argv) < 5:
    print(sys.argv)
    print("Not enough arguments")
    print("""
    $python main.py URL XPATH PRICE NOTIFICATION_PREF
    """)
    print(arg_error)
    sys.exit()

url = sys.argv[1]
xPath = sys.argv[2]
thresholdPrice = sys.argv[3]
alertType = sys.argv[4]

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

webpage = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(webpage.content, "html.parser")
dom = etree.HTML(str(soup))
price = dom.xpath(xPath)[0].text.strip('₹')

Fprice = float(price)
FthresholdPrice = float(thresholdPrice)
notif = {
    "email": email_alert,
    "slack": slack_alert,
    "email+slack": email_and_slack_alert

}
if Fprice < FthresholdPrice:
    notif[alertType](url, price)
