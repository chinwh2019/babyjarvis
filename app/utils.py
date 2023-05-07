import toml
import configparser

def get_openai_api_key():
    config = toml.load("env/local.toml")
    return config["openai"]["api_key"]


def read_config_file():
    config = configparser.ConfigParser()
    config.read("env/local.toml")
    return config


def get_api_key_from_config():
    config = read_config_file()
    if "openai" in config and "api_key" in config["openai"]:
        return config["openai"]["api_key"]
    return None