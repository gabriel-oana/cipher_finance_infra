import os
import subprocess

import aws_cdk as cdk
from constructs import Construct
from aws_cdk.aws_lambda import Function, AssetCode, Runtime, LayerVersion, Code
from aws_cdk import aws_iam as iam
from aws_cdk.aws_logs import RetentionDays
from aws_cdk import RemovalPolicy
from aws_cdk import aws_events, aws_events_targets

from cdk_utils.cdk_tags import add_tags
from cdk_config.config import Config
from cdk_config.config_lambda import LambdaConfig


class HourlyStockScraperLambdaStack(cdk.NestedStack):

    def __init__(self, scope: Construct, id: str, lambda_config: LambdaConfig, config: Config, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Removal Policy
        removal_policy = RemovalPolicy.DESTROY if lambda_config.retain_policy == 'destroy' else RemovalPolicy.RETAIN

        # IAM Role
        iam_role = iam.Role.from_role_arn(
            self,
            id=f'{config.env}-iam_role_scraper_imported',
            role_arn=f'arn:aws:iam::{os.getenv("CDK_DEFAULT_ACCOUNT")}:role/{lambda_config.iam_role}'
        )

        # Lambda function
        self.function = Function(
            self,
            f'{lambda_config.name}-lambda',
            description=lambda_config.description,
            handler='function.lambda_handler',
            code=AssetCode.from_asset(lambda_config.location),
            runtime=Runtime(name="python3.8"),
            role=iam_role,
            function_name=lambda_config.name,
            memory_size=lambda_config.memory_size,
            timeout=cdk.Duration.seconds(lambda_config.timeout_seconds),
            environment={
                "env": config.env
            },
            log_retention=RetentionDays.THREE_DAYS,
            layers=[
                self.create_dependencies_layer(config=config,
                                               base_path=lambda_config.location,
                                               lambda_config=lambda_config)
            ]
        )
        self.function.apply_removal_policy(removal_policy)
        add_tags(self, tags=config.tags)

        # Cloudwatch events triggers the lambda function at specific time with each event.
        lambda_schedule = aws_events.Schedule.cron(
                minute='0',
                hour='*',
                month='*',
                week_day='*',
                year='*')

        for ticker in config.lambda_historic_stock_scraper.cloudwatch_events:
            event_lambda_target = aws_events_targets.LambdaFunction(handler=self.function,
                                                                    event=aws_events.RuleTargetInput.from_object(ticker))

            cw_rule = aws_events.Rule(
                self,
                id=f'{lambda_config.name}-{ticker["ticker"]}-cw-rule',
                description="The once per hour CloudWatch event trigger for the Lambda",
                enabled=True,
                schedule=lambda_schedule,
                rule_name=f'{lambda_config.name}-{ticker["ticker"]}',
                targets=[event_lambda_target]
            )
            add_tags(cw_rule, tags=config.tags)

    def create_dependencies_layer(self, config: Config, base_path: str, lambda_config: LambdaConfig) -> LayerVersion:
        """
        Creates the packages required for the Lambda function
        """
        requirements_file = f'{base_path}/requirements.txt'
        output_dir = f'{os.getcwd()}/.build/{config.env}-{lambda_config.name}'

        if not os.environ.get('SKIP_PIP'):
            subprocess.check_call(
                f'pip install -r {requirements_file} -t {output_dir}/python'.split()
            )

        layer_id = f'{lambda_config.name}-lambda-dependencies'
        layer_code = Code.from_asset(output_dir)
        layer = LayerVersion(
            self,
            layer_id,
            code=layer_code,
            compatible_runtimes=[Runtime(name="python3.8")]
        )

        return layer

    @property
    def get_func(self):
        return self.function
