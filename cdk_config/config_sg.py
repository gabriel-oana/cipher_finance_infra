class SGConfig:

    def __init__(self, sg_config: dict, env: str):
        self.sg_config = sg_config
        self.env = env

    @property
    def name(self) -> str:
        return self.sg_config['name']
