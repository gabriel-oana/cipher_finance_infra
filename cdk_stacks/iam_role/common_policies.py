from aws_cdk import aws_iam as iam


class CommonIAMPolicy:

    def __init__(self, env: str):
        self.env = env

    @staticmethod
    def cloudwatch_global_policy() -> iam.PolicyStatement:
        cloudwatch_policy = iam.PolicyStatement(
            actions=[
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            effect=iam.Effect.ALLOW,
            resources=['*']
        )
        return cloudwatch_policy

    def auction_extractor_s3_policy(self) -> iam.PolicyStatement:
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
                f"arn:aws:s3:::{self.env}-cipher-finance-raw",
                f"arn:aws:s3:::{self.env}-cipher-finance-raw/*"
            ]
        )
        return s3_raw_policy
