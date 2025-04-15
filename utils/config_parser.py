import toml


def read_config(file_path: str) -> dict:
    try:
        with open(file_path, "r") as f:
            config = toml.load(f)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"配置文件未找到: {file_path}")
    except toml.TomlDecodeError as e:
        raise ValueError(f"TOML 解析错误: {e}")
    except Exception as e:
        raise RuntimeError(f"读取配置文件时发生未知错误: {e}")
