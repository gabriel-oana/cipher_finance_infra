import os
import time
import traceback
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Model:

    ticker: str
    ts: int = round(time.time() * 1000)
    updated_at: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dt: str = datetime.now().strftime('%Y-%m-%d')
    price: float = None
    change: float = None
    prc_change: float = None
    volume: int = None
    low: float = None
    high: float = None

    @staticmethod
    def get_indices(raw_data: list, debug: bool = False) -> dict:
        """
        Finds the indices of where the values are in the list.
        List example: ['1,106.80', '+14.60', '\xa0\xa0', '+1.34%', '', '', '', '', '29/04 - Closed. Currency in GBP ( Disclaimer )', '', '', '', '', 'Volume', ' 14,423', 'Bid/Ask', ' 0.00 / 0.00', "Day's Range", ' 1,105.40 - 1,114.80']
        """

        indices = {
            "price": 0,
            "change": 1,
            "prc_change": 3,
            "volume": raw_data.index('Volume') + 1,
            "price_range": raw_data.index("Day's Range") + 1
        }
        if debug:
            print(f'Indices: {indices}')

        return indices

    def set_values(self, raw_data: list, debug: bool = False):

        if debug:
            print(f'Raw Data: {raw_data}')

        indices = self.get_indices(raw_data=raw_data, debug=debug)

        self._set_price(raw_data=raw_data, price_index=indices['price'], debug=debug)
        self._set_change(raw_data=raw_data, change_index=indices['change'], debug=debug)
        self._set_prc_change(raw_data=raw_data, prc_change_index=indices['prc_change'], debug=debug)
        self._set_volume(raw_data=raw_data, volume_index=indices['volume'], debug=debug)
        self._set_high_low(raw_data=raw_data, hl_index=indices['price_range'], debug=debug)

    def _set_price(self, raw_data: list, price_index: int, debug: bool):
        try:
            self.price = float(raw_data[price_index].replace(',', ''))
        except Exception as e:
            if debug:
                print(f'Set price failed: {str(e)}-{print(traceback.format_exc())}')

    def _set_change(self, raw_data: list, change_index: int, debug: bool):
        try:
            self.change = float(raw_data[change_index])
        except Exception as e:
            if debug:
                print(f'Set change failed: {str(e)}-{print(traceback.format_exc())}')

    def _set_prc_change(self, raw_data: list, prc_change_index: int, debug: bool):
        try:
            self.prc_change = float(raw_data[prc_change_index].replace('%', ''))
        except Exception as e:
            if debug:
                print(f'Set prc change failed: {str(e)}-{print(traceback.format_exc())}')

    def _set_volume(self, raw_data: list, volume_index: int, debug: bool):
        try:
            self.volume = int(raw_data[volume_index].replace(',', ''))
        except Exception as e:
            if debug:
                print(f'Set volume failed: {str(e)}-{print(traceback.format_exc())}')

    def _set_high_low(self, raw_data: list, hl_index: int, debug: bool):
        try:
            price_range = raw_data[hl_index].strip()
            self.low = float(price_range.split('-')[0].strip().replace(',', ''))
            self.high = float(price_range.split('-')[1].strip().replace(',', ''))
        except Exception as e:
            if debug:
                print(f'Set high low failed: {str(e)}-{print(traceback.format_exc())}')


@dataclass
class Ticker:
    ticker: str
    marker: str
    parser: str = 'uk_investing'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    s3_bucket: str = None
    s3_key: str = None
    debug: bool = False
    data: Model = None

    def __post_init__(self):
        ts_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        year = ts_now.split('-')[0]
        month = ts_now.split('-')[1]
        day = ts_now.split('-')[2].split(' ')[0]
        self.s3_key = f'hourly/{self.marker}/{year}/{month}/{day}/{self.marker}.json'

        env = os.getenv("ENV")
        if env:
            self.s3_bucket = f'{env}-cipher-finance-raw'
        else:
            self.s3_bucket = 'dev-cipher-finance-raw'

    def parse(self, raw_data: list):
        model = Model(ticker=self.ticker)
        model.set_values(raw_data=raw_data, debug=self.debug)
        self.data = model
