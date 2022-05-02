import aws_cdk as cdk
from constructs import Construct
from aws_cdk import aws_ec2, aws_rds, aws_cloudwatch

from cdk_config.config import Config
from cdk_utils.cdk_tags import add_tags


class SecurityGroupStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, config: Config, vpc: aws_ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.sg = aws_ec2.SecurityGroup(
            self,
            f"{config.sg.name}-stack",
            vpc=vpc.vpc,
            security_group_name=config.sg.name,
            allow_all_outbound=True
        )

        # Egress Rules
        self.sg.add_egress_rule(
            peer=aws_ec2.Peer.ipv4(vpc.vpc.vpc_cidr_block),
            description='Postgres Egress',
            connection=aws_ec2.Port(
                protocol=aws_ec2.Protocol.TCP,
                string_representation='TCP',
                from_port=5432,
                to_port=5432
            )
        )

        # Ingress Rules
        self.sg.add_ingress_rule(
            peer=aws_ec2.Peer.ipv4(vpc.vpc.vpc_cidr_block),
            description='Postgres Ingress',
            connection=aws_ec2.Port(
                protocol=aws_ec2.Protocol.TCP,
                string_representation='TCP',
                from_port=5432,
                to_port=5432
            )
        )

        add_tags(self, tags=config.tags)