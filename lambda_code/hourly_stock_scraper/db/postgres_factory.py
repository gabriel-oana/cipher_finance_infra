import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class PostgresFactory:

    @staticmethod
    def create(host: str, port: str, database: str, username: str, password: str) -> sqlalchemy.engine.base.Engine:
        engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')
        return engine

    def create_from_env(self) -> sqlalchemy.engine.base.Engine:
        return self.create(
            os.getenv('RDS_HOST'),
            os.getenv('RDS_PORT'),
            os.getenv('RDS_DATABASE'),
            os.getenv('RDS_USER'),
            os.getenv('RDS_PASS')
        )

    def create_session(self):
        engine = self.create_from_env()
        s = sessionmaker(bind=engine)
        session = s()

        return session

    def load(self, data: list, model: object):

        session = self.create_session()
        try:
            session.bulk_insert_mappings(model, data)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
