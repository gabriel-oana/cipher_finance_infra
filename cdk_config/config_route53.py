class Route53Config:

    def __init__(self, route_config: dict, env: str):
        self.route_config = route_config
        self.env = env

    @property
    def certificate_arn(self) -> str:
        return self.route_config['certificate_arn']

    @property
    def root_domain(self) -> str:
        return self.route_config['root_domain']

    @property
    def db_record_name(self) -> str:
        return self.route_config['db_record_name']
