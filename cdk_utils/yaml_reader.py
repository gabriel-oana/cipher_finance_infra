import yaml
import os


# Define custom tag handler
def yaml_join(loader, node) -> str:
    """
    Handler to join strings.
    Usage in yaml files: !join [a,b,c]
    Result abc
    """
    seq = loader.construct_sequence(node)
    return ''.join([str(i) for i in seq])


def yaml_from_env(loader, node) -> str:
    """
    Handler to load an environment variable.
    Usage in yaml files: !from_env <param>
    """
    seq = loader.construct_scalar(node)
    env_var = os.getenv(seq)
    if not env_var:
        raise ValueError(f'YAML Handler: Parse failed. Environment variable {seq} does not exist')
    return env_var


def read_yaml_file(file_path: str):
    with open(file_path, 'r') as stream:
        try:
            # register the tag handlers
            yaml.add_constructor('!join', yaml_join)
            yaml.add_constructor('!from_env', yaml_from_env)
            
            yaml_object = yaml.unsafe_load(stream)
            return yaml_object
        except yaml.YAMLError as exc:
            raise ImportError(f'{exc}')
