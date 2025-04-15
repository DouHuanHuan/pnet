import tomli


def read_config(file_path):
    try:
        with open(file_path, "rb") as f:
            config = tomli.load(f)  # , 'owner')
        return config  # necessary_settings, pFN_settings, gFN_settings, hpc_settings
    except tomli.TOMLDecodeError:
        print(f"errors in {file_path}.")
