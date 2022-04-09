"""
Scraper triggered by Cloudwatch Events.
This function is optimised for speed not code quality.
As result, everything is very straight forward with as little overhead as possible.
"""

from datetime import date, timedelta, datetime
import json
import requests
from bs4 import BeautifulSoup
import boto3


S3_BUCKET = 'dev-cipher-finance-raw'


class VUSA:
    name = 'Vanguard S&P 500 UCITS'
    ticker = 'VUSA.L'
    marker = 'vusa'
    url = 'https://uk.investing.com/etfs/vanguard-s-p-500-uk-historical-data'
    parser = 'uk_investing'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}


# UTILS
def get_model(marker: str):
    if marker == 'vusa':
        return VUSA()


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

    if model.marker == 'vusa':
        table = html_text.find('table', attrs={"class": "genTbl closedTbl historicalTbl"})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')

        data = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

        return data


# Transform
def parse(model, raw_data: list, start_date: datetime.date, end_date: datetime.date):

    # Parse the uk-investing results
    if model.parser == 'uk_investing':

        data = []
        for item, val in enumerate(raw_data):
            date_value = convert_str_to_date(val[0])

            # Get only values between the two dates
            if end_date >= date_value >= start_date:
                data.append({
                    "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "dt": convert_date_to_str(date_value),
                    "price": float(val[1].replace('$', '')),
                    "open": float(val[2].replace("$", '')),
                    "high": float(val[3].replace("$", '')),
                    "low": float(val[4].replace("$", '')),
                    "volume": clean_uk_investment_volume(val[5].replace(',', '.')),
                    "change": float((val[6].split('%'))[0])
                })
        return data


def save_data(data: list, model):
    client = boto3.client('s3')

    for item in data:
        client.put_object(Body=json.dumps(item), Bucket=S3_BUCKET, Key=f'{model.marker}/{item["dt"]}.json')


def lambda_handler(event, context):
    print(event, context)
    start = date.today() - timedelta(days=5)
    end = date.today()

    model = get_model('vusa')
    raw_data = requestor(model)

    clean_data = parse(model, start_date=start, end_date=end, raw_data=raw_data)
    save_data(data=clean_data, model=model)


if __name__ == '__main__':

    start = date.today() - timedelta(days=5)
    end = date.today()

    model = get_model('vusa')
    raw_data = requestor(model)

    clean_data = parse(model, start_date=start, end_date=end, raw_data=raw_data)
    save_data(data=clean_data, model=model)



