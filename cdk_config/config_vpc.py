class VPCConfig:

    def __init__(self, vpc_config: dict, env: str):
        self.vpc_config = vpc_config
        self.env = env

    @property
    def cidr(self) -> str:
        return self.vpc_config['cidr']

    @property
    def max_azs(self) -> int:
        return self.vpc_config['max_azs']

    @property
    def nat_gateways(self) -> int:
        return self.vpc_config['nat_gateways']