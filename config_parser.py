# config_parser.py
import toml


def parse_config(file_path: str) -> dict:
    with open(file_path, "r") as f:
        config = toml.load(f)
    return config
