"""
Scraper triggered by Cloudwatch Events.
This function is optimised for speed not code quality.
As result, everything is very straight forward with as little overhead as possible.
"""
import json
import boto3
import requests
from bs4 import BeautifulSoup

from models.models import Ticker, VUSA, NVDA, CSCO, AIAI


def get_model(marker: str):
    if marker == 'vusa':
        return VUSA()
    elif marker == 'nvda':
        return NVDA()
    elif marker == 'csco':
        return CSCO()
    elif marker == 'aiai':
        return AIAI()
    else:
        raise ValueError(f'Marker {marker} not recognized')


# Extract
def requester(model):
    r = requests.get(url=model.url, headers=model.headers)
    html_text = BeautifulSoup(r.text, features='html.parser')
    raw_text = html_text.find('div', attrs={"class": "left current-data"})
    raw_data = raw_text.text.strip().replace('\n', ':').split(':')
    return raw_data


# Transform
def raw_transform(model, raw_data: list):

    # Parse the uk-investing results
    if model.parser == 'uk_investing':
        model.parse(raw_data=raw_data)


def save_data(model: Ticker):
    client = boto3.client('s3')

    # Get the file if exists else create it.
    try:
        obj = client.get_object(Bucket=model.s3_bucket, Key=model.s3_key)
        upload_data = json.loads(obj['Body'].read())
    except:
        upload_data = []

    upload_data.append(model.data.__dict__)
    client.put_object(Body=json.dumps(upload_data), Bucket=model.s3_bucket, Key=model.s3_key)


def lambda_handler(event, context):
    marker = event['ticker']
    model = get_model(marker)

    # Turn this on in dev
    model.debug = True

    raw_data = requester(model)
    print(raw_data)

    raw_transform(model, raw_data=raw_data)

    print(model)

    # save_data(model=model)


if __name__ == '__main__':
    lambda_handler(
        event={"ticker": "nvda"},
        context=None
    )
    lambda_handler(
        event={"ticker": "aiai"},
        context=None
    )