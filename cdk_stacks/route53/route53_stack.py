import aws_cdk as cdk
from constructs import Construct
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_route53 as route53

from cdk_config.config import Config
from cdk_utils.cdk_tags import add_tags


class Route53Stack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, config: Config, rds, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # ACM Certificate
        certificate = acm.Certificate.from_certificate_arn(self,
                                                           f'{config.env}-{config.base_stack_name}-certificate',
                                                           certificate_arn=config.route53.certificate_arn)

        # Route 53 - Add the linkage between custom name on API Gateway and route 53.
        zone = route53.HostedZone.from_lookup(self,
                                              f'{config.env}-{config.base_stack_name}-route-53-zone',
                                              domain_name=f'{config.route53.root_domain}')

        route53.CnameRecord(self,
                            f'{config.env}-{config.base_stack_name}-route-53-record',
                            zone=zone,
                            record_name=config.route53.db_record_name,
                            domain_name=rds.domain_name(),
                            ttl=cdk.Duration.minutes(300))

        add_tags(self, tags=config.tags)