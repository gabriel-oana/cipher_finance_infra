import os
import json
import boto3
import requests
from bs4 import BeautifulSoup

from models.models import Ticker, VUSA, NVDA, CSCO, AIAI
from db.postgres_factory import PostgresFactory
from db.orm import ORM


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


def save_data_s3(model: Ticker):
    client = boto3.client('s3')

    # Get the file if exists else create it.
    try:
        obj = client.get_object(Bucket=model.s3_bucket, Key=model.s3_key)
        upload_data = json.loads(obj['Body'].read())
    except:
        upload_data = []

    upload_data.append(model.data.__dict__)
    client.put_object(Body=json.dumps(upload_data), Bucket=model.s3_bucket, Key=model.s3_key)


def save_data_postgres(model: Ticker):
    pg = PostgresFactory()
    pg.load(data=[model.data.__dict__], model=ORM)


def lambda_handler(event, context):
    marker = event['ticker']
    model = get_model(marker)
    model.debug = True if os.getenv('env') else False

    # Extract
    raw_data = requester(model)

    # Transform
    raw_transform(model, raw_data=raw_data)

    # Load
    save_data_s3(model=model)
    save_data_postgres(model=model)


if __name__ == '__main__':
    lambda_handler(
        event={"ticker": "nvda"},
        context=None
    )