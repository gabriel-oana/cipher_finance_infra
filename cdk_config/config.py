import os
import yaml

from config.config_s3 import S3Config
from config.config_iam import IAMConfig
from config.config_lambda import LambdaConfig
from config.config_vpc import VPCConfig


class Config:

    def __init__(self, env: str):
        default_path = f'{os.getcwd()}/cdk_env/{env}-wow-config.yaml'
        self.config = yaml.safe_load(open(default_path))

    @property
    def env(self) -> str:
        return self.config['env']

    @property
    def tags(self) -> dict:
        return self.config['tags']

    @property
    def base_stack_name(self) -> dict:
        return self.config['base_stack_name']

    @property
    def s3_raw(self) -> S3Config:
        return S3Config(self.config['s3_bucket']['raw'], env=self.env)

    @property
    def s3_processed(self) -> S3Config:
        return S3Config(self.config['s3_bucket']['processed'], env=self.env)

    @property
    def iam_auction_extractor(self) -> IAMConfig:
        return IAMConfig(self.config['iam_role']['auction-extractor'], env=self.env)

    @property
    def iam_mining_processor(self) -> IAMConfig:
        return IAMConfig(self.config['iam_role']['auction-processor'], env=self.env)

    @property
    def lambda_auction_extractor(self) -> LambdaConfig:
        return LambdaConfig(self.config['lambdas']['auction-extractor'], env=self.env)

    @property
    def lambda_auction_processor(self) -> LambdaConfig:
        return LambdaConfig(self.config['lambdas']['auction-processor'], env=self.env)

    @property
    def rds(self) -> RDSConfig:
        return RDSConfig(self.config['rds'], env=self.env)

    @property
    def vpc(self) -> VPCConfig:
        return VPCConfig(self.config['vpc'], env=self.env)