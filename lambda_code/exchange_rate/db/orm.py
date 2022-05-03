from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, MetaData, Float, Date


Base = declarative_base(metadata=MetaData(schema='finance'))


class ORM(Base):
    __tablename__ = 'exchange_rates'

    dt = Column(Date, primary_key=True)
    updated_dt = Column(Date)
    base_currency = Column(String)
    target_currency = Column(String)
    rate = Column(Float)
