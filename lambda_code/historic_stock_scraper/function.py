"""
Scraper triggered by Cloudwatch Events.
This function is optimised for speed not code quality.
As result, everything is very straight forward with as little overhead as possible.
"""
import os
import time
import uuid
import json
import boto3
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

from db.orm import ORM
from db.postgres_factory import PostgresFactory


S3_BUCKET = f'{os.getenv("env")}-cipher-finance-raw'


class VUSA:
    name = 'Vanguard S&P 500 UCITS'
    ticker = 'VUSA.L'
    marker = 'vusa'
    currency = 'GBP'
    url = 'https://uk.investing.com/etfs/vanguard-s-p-500-uk-historical-data'
    parser = 'uk_investing'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}


class NVDA:
    name = 'Nvidia Corp'
    ticker = 'NVDA'
    marker = 'nvda'
    currency = 'USD'
    url = 'https://uk.investing.com/equities/nvidia-corp-historical-data'
    parser = 'uk_investing'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}


class CSCO:
    name = 'Cisco Systems Inc'
    ticker = 'CSCO'
    marker = 'csco'
    currency = 'USD'
    url = 'https://uk.investing.com/equities/cisco-sys-inc-historical-data'
    parser = 'uk_investing'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}


class AIAI:
    name: str = 'L&G Artificial Intelligence UCITS ETF'
    ticker: str = 'AIAI'
    marker: str = 'aiai'
    currency: str = 'GBP'
    url: str = 'https://uk.investing.com/etfs/lg-artificial-intelligence-ucits-historical-data'
    parser = 'uk_investing'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}


# UTILS
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


def convert_str_to_date(date_str: str) -> datetime.date:
    dt_obj = datetime.strptime(date_str, '%b %d, %Y')
    return dt_obj.date()


def convert_date_to_str(date_obj: datetime.date) -> str:
    dt_str = date_obj.strftime('%Y-%m-%d')
    return dt_str


def clean_uk_investment_volume(value_str: str) -> int:
    """
    Replaces the M and K with the values themselves
    """
    float_volume = float(value_str[:-1])

    if "M" in value_str:
        volume = int(float_volume * 100000)
    elif "K" in value_str:
        volume = int(float_volume * 1000)
    else:
        volume = float_volume

    return volume


# Extract
def requestor(model):
    r = requests.get(url=model.url, headers=model.headers)
    html_text = BeautifulSoup(r.text, features='html.parser')

    if model.marker in ['vusa', 'nvda', 'csco', 'aiai']:
        table = html_text.find('table', attrs={"class": "genTbl closedTbl historicalTbl"})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')

        data = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

        return data
    else:
        raise RuntimeError(f'Requestor not configure for marker {model.marker}')


# Transform
def parse(model, raw_data: list, start_date: datetime.date, end_date: datetime.date):

    # Parse the uk-investing results
    if model.parser == 'uk_investing':

        data = []
        parsed_dates = []
        for item, val in enumerate(raw_data):
            date_value = convert_str_to_date(val[0])

            # Get only values between the two dates
            # Do not parse the same date twice
            # Website has a bug
            if end_date >= date_value >= start_date and date_value not in parsed_dates:
                print(date_value)

                data.append({
                    "id": str(uuid.uuid4()),
                    "ticker": model.ticker,
                    "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "ts": round(time.time() * 1000),
                    "dt": convert_date_to_str(date_value),
                    "price": float(val[1].replace('$', '').replace(',', '')),
                    "open": float(val[2].replace("$", '').replace(',', '')),
                    "high": float(val[3].replace("$", '').replace(',', '')),
                    "low": float(val[4].replace("$", '').replace(',', '')),
                    "volume": clean_uk_investment_volume(val[5].replace(',', '.')),
                    "change": float((val[6].split('%'))[0].replace(',', ''))
                })
                parsed_dates.append(date_value)

        return data


def save_data_s3(data: list, model):
    client = boto3.client('s3')

    for item in data:
        year = item['dt'].split('-')[0]
        month = item['dt'].split('-')[1]
        day = item['dt'].split('-')[2]

        key = f'historic/{model.marker}/{year}/{month}/{day}/{model.marker}.json'
        client.put_object(Body=json.dumps(item), Bucket=S3_BUCKET, Key=key)


def save_data_pg(data: list, start_date: datetime.date, end_date: datetime.date):
    pg_factory = PostgresFactory()
    pg_factory.load(data=data, model=ORM, rm_existing_data=True, start_date=start_date, end_date=end_date)


def lambda_handler(event, context):
    marker = event['ticker']
    print(f'Processing {marker}')

    start = date.today() - timedelta(days=5)
    end = date.today()

    model = get_model(marker)
    raw_data = requestor(model)
    print(raw_data)

    clean_data = parse(model, start_date=start, end_date=end, raw_data=raw_data)
    print(clean_data)

    save_data_s3(data=clean_data, model=model)
    save_data_pg(data=clean_data, start_date=start, end_date=end)


if __name__ == '__main__':
    lambda_handler(
        event={"ticker": "aiai"},
        context=None
    )