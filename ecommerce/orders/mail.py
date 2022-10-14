import re

import boto3
from botocore.exceptions import ClientError


def clean_html(raw_html):
    cleaner = re.compile('<.*?>')
    clean_text = re.sub(cleaner, '', raw_html)
    return clean_text


SENDER = "FastAPI <fastapi@givmail.com>"
AWS_REGION = "us-east-2"
SUBJECT = "New Order Placed"

BODY_HTML = """
<html>
<head></head>
<body>
  <h1>Order Successfully Placed !</h1>
  <p>Hi, Your new order has been successfully placed. You will receive more information shortly.</p>
</body>
</html>
"""

BODY_TEXT = clean_html(BODY_HTML)
CHARSET = "UTF-8"

client = boto3.client('ses', region_name=AWS_REGION)


def order_notification(recipient):
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
