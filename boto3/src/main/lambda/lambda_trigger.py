# parse config.yaml and ask for input from user for client
import yaml


def get_config():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config

config=get_config()
print(config['niven']['region'])
