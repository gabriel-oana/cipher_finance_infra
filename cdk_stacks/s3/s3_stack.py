import aws_cdk as cdk
from constructs import Construct
from aws_cdk import aws_s3 as s3
from aws_cdk import RemovalPolicy

from cdk_config.config_s3 import S3Config
from cdk_config.config import Config
from cdk_utils.cdk_tags import add_tags


class S3Stack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, config: Config, s3_config: S3Config, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.s3_bucket = s3.Bucket(
            self,
            id=f'{s3_config.bucket_name}-s3-bucket',
            bucket_name=s3_config.bucket_name,
            removal_policy=self._map_removal_policy(s3_config.removal_policy),
            auto_delete_objects=False,
            access_control=s3.BucketAccessControl.PRIVATE
        )

        cdk.CfnOutput(self,
                      f'{config.env}-{config.base_stack_name}-{s3_config.bucket_name}-s3-bucket-name',
                      value=self.s3_bucket.bucket_name,
                      description=f'Bucket name for environment: {config.env}')
        cdk.CfnOutput(self,
                      f'{config.env}-{config.base_stack_name}-{s3_config.bucket_name}-s3-bucket-arn',
                      value=self.s3_bucket.bucket_arn,
                      description=f'Bucket ARN for environment: {config.env}')

        add_tags(self, tags=config.tags)

    @staticmethod
    def _map_removal_policy(removal_policy: str) -> RemovalPolicy:
        if removal_policy == 'retain':
            return RemovalPolicy.RETAIN
        elif removal_policy == 'destroy':
            return RemovalPolicy.DESTROY
        elif removal_policy == 'SNAPSHOT':
            return RemovalPolicy.SNAPSHOT
        else:
            raise ValueError('Invalid s3 retention policy')

    def get_s3_bucket(self):
        return self.s3_bucket
