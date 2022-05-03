import aws_cdk as cdk
from constructs import Construct
from aws_cdk import aws_ec2

from cdk_config.config import Config
from cdk_utils.cdk_tags import add_tags


class SecurityGroupStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, config: Config, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = aws_ec2.Vpc.from_lookup(self, "VPC", vpc_name=config.vpc.name)

        self.sg = aws_ec2.SecurityGroup(
            self,
            f"{config.sg.name}-stack",
            vpc=vpc,
            security_group_name=config.sg.name,
            allow_all_outbound=True
        )

        # Ingress Rules
        self.sg.add_ingress_rule(
            peer=aws_ec2.Peer.ipv4(vpc.vpc_cidr_block),
            description='Postgres Ingress',
            connection=aws_ec2.Port.all_traffic()
        )

        add_tags(self, tags=config.tags)