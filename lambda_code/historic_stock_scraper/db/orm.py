from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, MetaData, Float, Date, Integer


Base = declarative_base(metadata=MetaData(schema='finance'))


class ORM(Base):
    __tablename__ = 'stock_daily_raw'

    id = Column(String, primary_key=True)
    ticker = Column(String)
    updated_at = Column(String)
    ts = Column(Float)
    dt = Column(Date)
    price = Column(Float)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Integer)
    change = Column(Float)


