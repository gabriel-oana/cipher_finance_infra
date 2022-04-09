class IAMConfig:

    def __init__(self, iam_config: dict, env: str):
        self.iam_config = iam_config
        self.env = env

    @property
    def description(self) -> str:
        return self.iam_config['description']

    @property
    def name(self) -> str:
        name = f'{self.iam_config["name"]}'
        return name
