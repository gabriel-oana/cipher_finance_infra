class LambdaConfig:

    def __init__(self, lambda_conf: dict, env: str):
        self.lambda_conf = lambda_conf
        self.env = env

    @property
    def description(self) -> str:
        return self.lambda_conf['description']

    @property
    def retain_policy(self) -> str:
        return self.lambda_conf['retain_policy']

    @property
    def timeout_seconds(self) -> int:
        return self.lambda_conf['timeout_seconds']

    @property
    def memory_size(self) -> int:
        return self.lambda_conf['memory_size']

    @property
    def location(self) -> str:
        return self.lambda_conf['location']

    @property
    def name(self) -> str:
        return self.lambda_conf["name"]

    @property
    def iam_role(self) -> str:
        return self.lambda_conf['iam_role']

    @property
    def cloudwatch_events(self) -> dict:
        return self.lambda_conf['cloudwatch_events']
