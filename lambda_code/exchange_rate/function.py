import os
import boto3
import json
from datetime import datetime
import requests

from db.orm import ORM
from db.postgres_factory import PostgresFactory


API_KEY = os.getenv('EXCHANGE_RATES_API')
S3_BUCKET = f'{os.getenv("env")}-cipher-finance-raw'


def extract():
    """
    This one takes priority
    """
    r = requests.get(
        url='https://api.getgeoapi.com/v2/currency/convert',
        params={
            "from": 'USD',
            "to": 'GBP',
            "amount": 1,
            "api_key": API_KEY
        }
    )

    return r.json()


def transform(data: dict) -> dict:

    clean_data = {
        "dt": datetime.now().strftime('%Y-%m-%d'),
        "updated_dt": data['updated_date'],
        "base_currency": "USD",
        "target_currency": "GBP",
        "rate": data['rates']['GBP']['rate']
    }

    return clean_data


def save_s3(clean: dict):
    client = boto3.client('s3')

    # File key
    year = datetime.now().strftime('%Y')
    s3_key = f'exchange_rates/{year}/exchange_rates.json'

    # Get the file if exists else create it.
    try:
        obj = client.get_object(Bucket=S3_BUCKET, Key=s3_key)
        upload_data = json.loads(obj['Body'].read())
    except:
        upload_data = []

    upload_data.append(clean)
    client.put_object(Body=json.dumps(upload_data), Bucket=S3_BUCKET, Key=s3_key)


def save_pg(clean: dict):
    pg = PostgresFactory()
    pg.load(data=[clean], model=ORM)


def lambda_handler(event, context):
    raw = extract()
    print(raw)
    clean = transform(raw)
    save_s3(clean)
    save_pg(clean)


if __name__ == '__main__':
    r = extract()
    c = transform(r)
    save_s3(c)
