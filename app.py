import os
import aws_cdk as cdk
from cdk_config.config import Config
from cdk_stacks.s3.s3_stack import S3Stack
from cdk_stacks.iam_role.stock_scraper_iam_stack import StockScraperIAMStack
from cdk_stacks.lambdas.historic_stock_scraper_lambda_stack import HistoricStockScraperLambdaStack
from cdk_stacks.lambdas.hourly_stock_scraper_lambda_stack import HourlyStockScraperLambdaStack
from cdk_stacks.rds.rds_stack import RDSPostgresStack
from cdk_stacks.vpc.vpc_stack import VpcStack
from cdk_stacks.security_group.sg_stack import SecurityGroupStack
from cdk_stacks.route53.route53_stack import Route53Stack


cdk_app = cdk.App()
config = Config(env=os.environ['CDK_ENVIRON'])


StockScraperIAMStack(
    scope=cdk_app,
    id=config.iam_stock_scraper.name,
    config=config,
    iam_role=config.iam_stock_scraper,
    env=cdk.Environment(
        account=os.environ['CDK_DEFAULT_ACCOUNT'],
        region=os.environ['CDK_DEFAULT_REGION']
    )
)


S3Stack(
    scope=cdk_app,
    id=f'{config.s3_raw.bucket_name}-s3',
    config=config,
    s3_config=config.s3_raw,
    env=cdk.Environment(
        account=os.environ['CDK_DEFAULT_ACCOUNT'],
        region=os.environ['CDK_DEFAULT_REGION']
    )
)


vpc_stack = VpcStack(
    scope=cdk_app,
    id=config.vpc.name,
    config=config,
    env=cdk.Environment(
        account=os.environ['CDK_DEFAULT_ACCOUNT'],
        region=os.environ['CDK_DEFAULT_REGION']
    )
)

sg = SecurityGroupStack(
    scope=cdk_app,
    id=config.sg.name,
    config=config,
    vpc=vpc_stack,
    env=cdk.Environment(
        account=os.environ['CDK_DEFAULT_ACCOUNT'],
        region=os.environ['CDK_DEFAULT_REGION']
    )
)

rds = RDSPostgresStack(
    cdk_app,
    f'{config.env}-cipher-rds',
    config=config,
    vpc=vpc_stack.vpc,
    sg=sg.sg,
    env=cdk.Environment(
        account=os.environ['CDK_DEFAULT_ACCOUNT'],
        region=os.environ['CDK_DEFAULT_REGION']
    )
)

Route53Stack(
    cdk_app,
    f'{config.env}-{config.base_stack_name}-route53',
    config=config,
    rds=rds,
    env=cdk.Environment(
        account=os.environ['CDK_DEFAULT_ACCOUNT'],
        region=os.environ['CDK_DEFAULT_REGION']
    )
)

# Lambda Functions
HistoricStockScraperLambdaStack(
    scope=cdk_app,
    id=config.lambda_historic_stock_scraper.name,
    config=config,
    lambda_config=config.lambda_historic_stock_scraper,
    env=cdk.Environment(
        account=os.environ['CDK_DEFAULT_ACCOUNT'],
        region=os.environ['CDK_DEFAULT_REGION']
    )
)

HourlyStockScraperLambdaStack(
    scope=cdk_app,
    id=config.lambda_hourly_stock_scraper.name,
    config=config,
    lambda_config=config.lambda_hourly_stock_scraper,
    env=cdk.Environment(
        account=os.environ['CDK_DEFAULT_ACCOUNT'],
        region=os.environ['CDK_DEFAULT_REGION']
    )
)

cdk_app.synth()