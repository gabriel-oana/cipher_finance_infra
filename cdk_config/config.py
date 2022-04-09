import os
from cdk_utils.yaml_reader import read_yaml_file

from cdk_config.config_s3 import S3Config
from cdk_config.config_iam import IAMConfig
from cdk_config.config_lambda import LambdaConfig
from cdk_config.config_vpc import VPCConfig


class Config:

    def __init__(self, env: str):
        default_path = f'{os.getcwd()}/cdk_env/{env}-cipher-finance-infra.yaml'
        self.config = read_yaml_file(default_path)

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
        return S3Config(self.config['s3']['raw'], env=self.env)

    @property
    def s3_processed(self) -> S3Config:
        return S3Config(self.config['s3']['processed'], env=self.env)

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
    def vpc(self) -> VPCConfig:
        return VPCConfig(self.config['vpc'], env=self.env)