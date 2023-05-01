import toml


def get_openai_api_key():
    config = toml.load("env/local.toml")
    return config["openai"]["api_key"]
