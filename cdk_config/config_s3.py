class S3Config:

    def __init__(self, s3_config: dict, env: str):
        self.s3_config = s3_config
        self.env = env

    @property
    def description(self) -> str:
        return self.s3_config['description']

    @property
    def bucket_name(self) -> str:
        bucket_name = f'{self.s3_config["bucket_name"]}'
        return bucket_name

    @property
    def versioned(self) -> bool:
        return bool(self.s3_config['versioned'])

    @property
    def removal_policy(self) -> str:
        return self.s3_config['removal_policy']

    @property
    def auto_delete_objects(self) -> bool:
        return self.s3_config['auto_delete_objects']