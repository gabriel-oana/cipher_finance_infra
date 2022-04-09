import os
import aws_cdk as cdk
from constructs import Construct

from cdk_utils.cdk_tags import add_tags
from cdk_config.config import Config
from cdk_stacks.s3.s3_stack import S3Stack


cdk_app = cdk.App()
config = Config(env=os.environ['CDK_ENVIRON'])


class RootStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, config: Config, **kwargs):
        super().__init__(scope, id, **kwargs)

        # S3 Buckets
        s3_raw_bucket = S3Stack(
            self,
            f'{config.env}-{config.base_stack_name}-s3-{config.s3_raw.bucket_name}',
            config=config,
            s3_config=config.s3_raw
        )

        S3Stack(
            self,
            f'{config.env}-{config.base_stack_name}-s3-{config.s3_processed.bucket_name}',
            config=config,
            s3_config=config.s3_processed,
        )

        # # IAM Roles
        # AuctionExtractorIAMStack(
        #     self,
        #     f'{config.env}-{config.base_stack_name}-iam-{config.iam_auction_extractor.name}',
        #     config=config,
        #     iam_role=config.iam_auction_extractor
        # )
        #
        # AuctionProcessorIAMStack(
        #     self,
        #     f'{config.env}-{config.base_stack_name}-iam-{config.iam_mining_processor.name}',
        #     config=config,
        #     iam_role=config.iam_mining_processor
        # )
        #
        # # Lambda Functions
        # AuctionExtractorLambdaStack(
        #     self,
        #     f'{config.env}-{config.base_stack_name}-lambda-{config.lambda_auction_extractor.name}',
        #     config=config,
        #     lambda_config=config.lambda_auction_extractor
        # )
        #
        # AuctionProcessorLambdaStack(
        #     self,
        #     f'{config.env}-{config.base_stack_name}-lambda-{config.lambda_auction_processor.name}',
        #     config=config,
        #     lambda_config=config.lambda_auction_processor,
        #     s3_bucket=s3_raw_bucket.get_s3_bucket()
        # )

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