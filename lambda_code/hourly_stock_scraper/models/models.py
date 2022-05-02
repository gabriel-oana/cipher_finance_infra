from dataclasses import dataclass, field

from models.base_models import Ticker


@dataclass
class VUSA(Ticker):
    name: str = 'Vanguard S&P 500 UCITS'
    ticker: str = 'VUSA.L'
    marker: str = 'vusa'
    currency: str = 'GBP'
    url: str = 'https://uk.investing.com/etfs/vanguard-s-p-500-uk-historical-data'


@dataclass
class NVDA(Ticker):
    name: str = 'Nvidia Corp'
    ticker: str = 'NVDA'
    marker: str = 'nvda'
    currency: str = 'USD'
    url: str = 'https://uk.investing.com/equities/nvidia-corp-historical-data'


@dataclass
class CSCO(Ticker):
    name: str = 'Cisco Systems Inc'
    ticker: str = 'CSCO'
    marker: str = 'csco'
    currency: str = 'USD'
    url: str = 'https://uk.investing.com/equities/cisco-sys-inc-historical-data'


@dataclass
class AIAI(Ticker):
    name: str = 'L&G Artificial Intelligence UCITS ETF'
    ticker: str = 'AIAI'
    marker: str = 'aiai'
    currency: str = 'GBP'
    url: str = 'https://uk.investing.com/etfs/lg-artificial-intelligence-ucits-historical-data'