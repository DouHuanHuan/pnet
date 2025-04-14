import tomli


def read_config(file_path):
    try:
        with open(file_path, "rb") as f:
            config = tomli.load(f)  # , 'owner')
            necessary_settings = config['necessary_settings']
            pFN_settings = config['pFN_settings']
            gFN_settings = config['gFN_settings']
            hpc_settings = config['hpc_settings']
        return config  # necessary_settings, pFN_settings, gFN_settings, hpc_settings
    except tomli.TOMLDecodeError:
        print(f"errors in {file_path}.")
