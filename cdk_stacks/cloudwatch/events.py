
import aws_cdk as cdk
from constructs import Construct
from aws_cdk import aws_events, aws_events_targets

from cdk_utils.cdk_tags import add_tags
from cdk_config.config import Config
from cdk_config.config_lambda import LambdaConfig


class CloudwatchEventStack(cdk.NestedStack):

    def __init__(self, scope: Construct, id: str, lambda_function, config: Config, lambda_event: dict, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Lambda Schedule
        lambda_schedule = aws_events.Schedule.cron(
                minute='0',
                hour='*',
                month='*',
                week_day='2-6',
                year='*')

        event_lambda_target = aws_events_targets.LambdaFunction(handler=lambda_function,
                                                                event=aws_events.RuleTargetInput.from_object(lambda_event))

        # Lambda hourly rule
        aws_events.Rule(
            self,
            f'{lambda_config.name}-rule',
            description="The once per hour CloudWatch event trigger for the Lambda",
            enabled=True,
            schedule=lambda_schedule,
            targets=[event_lambda_target]
        )