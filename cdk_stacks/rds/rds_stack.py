import aws_cdk as cdk
from constructs import Construct
from aws_cdk import aws_ec2, aws_rds, aws_cloudwatch

from cdk_config.config import Config
from cdk_utils.cdk_tags import add_tags


class RDSPostgresStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, config: Config, sg, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = aws_ec2.Vpc.from_lookup(self, "VPC", vpc_name=config.vpc.name)

        self.db = aws_rds.DatabaseInstance(
            self,
            id=f'{config.env}-rds-instance-stack',
            vpc=vpc,
            credentials=aws_rds.Credentials.from_username(password=cdk.SecretValue.plain_text(config.rds.password),
                                                          username=config.rds.username),
            database_name=config.rds.database_name,
            engine=aws_rds.DatabaseInstanceEngine.postgres(version=aws_rds.PostgresEngineVersion.VER_12),
            instance_type=aws_ec2.InstanceType(config.rds.instance_type),
            multi_az=False,
            instance_identifier=config.rds.instance_name,
            allocated_storage=config.rds.storage,
            storage_type=aws_rds.StorageType.GP2,
            deletion_protection=config.rds.deletion_protection,
            delete_automated_backups=True,
            backup_retention=cdk.Duration.days(0),
            auto_minor_version_upgrade=False,
            max_allocated_storage=config.rds.max_storage,
            publicly_accessible=True,
            vpc_subnets=aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.PUBLIC),
            security_groups=[sg]
        )

        # Add alarm for high CPU
        aws_cloudwatch.Alarm(
            self,
            id=f"{config.env}-{config.base_stack_name}-RDS-HighCPU",
            metric=self.db.metric_cpu_utilization(),
            threshold=90,
            evaluation_periods=1
        )

        # Add alarm for high storage
        aws_cloudwatch.Alarm(
            self,
            id=f"{config.env}-{config.base_stack_name}-RDS-HighStorage",
            metric=self.db.metric_free_storage_space(),
            threshold=90,
            evaluation_periods=1
        )

        add_tags(self, tags=config.tags)

    def domain_name(self):
        return self.db.instance_endpoint.hostname
