import pathlib
import yaml


BASE_DIR = pathlib.Path(__file__).parent.parent
config_file = BASE_DIR / 'config' / 'config.yaml'


def get_config(path):
    with open(path) as f:
        config = yaml.safe_load(f)
    return config


app_config = get_config(config_file)
