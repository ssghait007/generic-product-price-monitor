from config import email, google_app_pass
import smtplib
import requests
import json
import sys


def slack_alert(URL, price):
    title = f'Price fell down to {price}'
    message = 'Buy it now here: '+URL
    webhook_url = ""
    slack_msg = {
        "username": "BOT_NAME",
        "icon_emoji": ":tada:",
        "channel": "SLACK_CHANNEL_NAME",
        "attachments": [
                {
                    "color": "#75e403",
                    "fields": [
                        {
                            "title": title,
                            "value": message,
                            "short": "false",
                        }
                    ]}
        ]}
    byte_length = str(sys.getsizeof(slack_msg))
    headers = {"Content-Type": "application/json",
               "Content-Length":     byte_length}
    requests.post(webhook_url, data=json.dumps(
        slack_msg),    headers=headers)


def email_alert(URL, price):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(email, google_app_pass)
    subject = f'Price fell down to {price}'
    body = 'Buy it now here: '+URL
    msg = f"Subject:{subject}\n\n{body}"
    server.sendmail(email, email, msg)
    print('Email alert sent')
    server.quit()


def email_and_slack_alert(URL, price):
    slack_alert(URL, price)
    email_alert(URL, price)
