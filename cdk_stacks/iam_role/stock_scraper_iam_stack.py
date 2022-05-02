import aws_cdk as cdk
from constructs import Construct
from aws_cdk import aws_iam as iam

from cdk_config.config import Config
from cdk_config.config_iam import IAMConfig
from cdk_utils.cdk_tags import add_tags

from cdk_stacks.iam_role.common_policies import CommonIAMPolicy


class StockScraperIAMStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, iam_role: IAMConfig, config: Config, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        assumed_principal = iam.ServicePrincipal('lambda.amazonaws.com')

        # IAM Role
        self.iam_role = iam.Role(
            self,
            iam_role.name,
            description=iam_role.description,
            role_name=iam_role.name,
            assumed_by=assumed_principal
        )

        # Policies
        iam_policy = CommonIAMPolicy(env=config.env)
        cloudwatch_policy = iam_policy.cloudwatch_global_policy()

        iam.ManagedPolicy(
            scope=self,
            id=f"{iam_role.name}-policy",
            statements=[
                cloudwatch_policy,
                self.s3_raw_policy(env=config.env)
            ],
            roles=[self.iam_role]
        )

        add_tags(self, tags=config.tags)

        cdk.CfnOutput(self, f"{iam_role.name}-name",
                      value=self.iam_role.role_name,
                      description=f'IAM Role Scraper name for environment: {config.env}')
        cdk.CfnOutput(self, f"{iam_role.name}-arn",
                      value=self.iam_role.role_arn,
                      description=f'IAM Role Scraper ARN for environment: {config.env}')

    @property
    def get_role(self):
        return self.iam_role

    @staticmethod
    def s3_raw_policy(env: str) -> iam.PolicyStatement:
        s3_raw_policy = iam.PolicyStatement(
            actions=[
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket",
                "s3:DeleteObject",
                "s3:GetObjectVersion",
            ],
            effect=iam.Effect.ALLOW,
            resources=[
                f"arn:aws:s3:::{env}-cipher-finance-raw",
                f"arn:aws:s3:::{env}-cipher-finance-raw/*"
            ]
        )
        return s3_raw_policy
