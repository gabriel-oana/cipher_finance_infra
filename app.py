import os
import aws_cdk as cdk
from constructs import Construct

from cdk_utils.cdk_tags import add_tags
from cdk_config.config import Config
from cdk_stacks.s3.s3_stack import S3Stack
from cdk_stacks.iam_role.stock_scraper_iam_stack import StockScraperIAMStack
from cdk_stacks.lambdas.stock_scraper_lambda_stack import StockScraperLambdaStack
from cdk_stacks.cloudwatch.events import CloudwatchEventStack


cdk_app = cdk.App()
config = Config(env=os.environ['CDK_ENVIRON'])


class RootStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, config: Config, **kwargs):
        super().__init__(scope, id, **kwargs)

        # S3 Buckets
        s3_raw_bucket = S3Stack(
            self,
            f'{config.s3_raw.bucket_name}-stack',
            config=config,
            s3_config=config.s3_raw
        )

        # IAM Roles
        StockScraperIAMStack(
            self,
            f'{config.iam_stock_scraper.name}-stack',
            config=config,
            iam_role=config.iam_stock_scraper
        )

        # Lambda Functions
        StockScraperLambdaStack(
            self,
            f'{config.lambda_stock_scraper.name}-stack',
            config=config,
            lambda_config=config.lambda_stock_scraper
        )

        # vpc_stack = VpcStack(
        #     cdk_app,
        #     f'{config.env}-{config.base_stack_name}-vpc',
        #     config=config,
        #     env=core.Environment(
        #         account=os.environ['CDK_DEFAULT_ACCOUNT'],
        #         region=os.environ['CDK_DEFAULT_REGION']
        #     )
        # )
        #
        # rds_stack = RDSPostgresStack(
        #     cdk_app,
        #     f'{config.env}-{config.base_stack_name}-rds-postgres',
        #     config=config,
        #     vpc=vpc_stack.vpc
        # )

        add_tags(self, tags=config.tags)


RootStack(
    cdk_app,
    f'{config.env}-{config.base_stack_name}',
    config=config,
    env=cdk.Environment(
        account=os.environ['CDK_DEFAULT_ACCOUNT'],
        region=os.environ['CDK_DEFAULT_REGION']
    )
)

cdk_app.synth()