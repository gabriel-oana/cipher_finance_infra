import uuid

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, MetaData, Float, Date, Integer


Base = declarative_base(metadata=MetaData(schema='finance'))


class ORM(Base):
    __tablename__ = 'stock_hourly_raw'

    id = Column(String, primary_key=True, default=uuid.uuid4())
    ticker = Column(String)
    updated_at = Column(String)
    ts = Column(Float)
    dt = Column(Date)
    price = Column(Float)
    change = Column(Float)
    prc_change = Column(Float)
    volume = Column(Integer)
    low = Column(Float)
    high = Column(Float)