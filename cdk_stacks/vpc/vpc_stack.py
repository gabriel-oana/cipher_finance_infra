import aws_cdk as cdk
from constructs import Construct
from aws_cdk import aws_ec2

from cdk_utils.cdk_tags import add_tags
from cdk_config.config import Config


class VpcStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, config: Config, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = aws_ec2.Vpc(
            self,
            id=f"{config.env}-vpc",
            cidr=config.vpc.cidr,
            max_azs=config.vpc.max_azs,
            nat_gateways=config.vpc.nat_gateways,
            vpc_name=config.vpc.name,
            subnet_configuration=[
                aws_ec2.SubnetConfiguration(
                    subnet_type=aws_ec2.SubnetType.PUBLIC,
                    name="Public",
                    cidr_mask=24
                ), aws_ec2.SubnetConfiguration(
                    subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_NAT,
                    name="Private",
                    cidr_mask=24
                )
            ]
        )

        add_tags(self, config.tags)

        cdk.CfnOutput(
            self,
            id="VPCId",
            value=self.vpc.vpc_id,
            description="VPC ID",
            export_name=f"{self.region}:{self.account}:{self.stack_name}:vpc-id"
        )
