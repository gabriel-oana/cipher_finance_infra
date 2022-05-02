import os


class RDSConfig:

    def __init__(self, rds_config: dict, env: str):
        self.rds_config = rds_config
        self.env = env

    @property
    def instance_name(self) -> str:
        return self.rds_config['instance_name']

    @property
    def instance_type(self) -> str:
        return self.rds_config['instance_type']

    @property
    def database_name(self) -> str:
        return self.rds_config['database_name']

    @property
    def storage(self) -> int:
        return self.rds_config['storage']

    @property
    def max_storage(self) -> int:
        return self.rds_config['max_storage']

    @property
    def deletion_protection(self) -> bool:
        return self.rds_config['deletion_protection']

    @property
    def username(self) -> str:
        return os.getenv('RDS_USERNAME')

    @property
    def password(self) -> str:
        return os.getenv('RDS_PASSWORD')
