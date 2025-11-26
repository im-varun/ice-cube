import configparser

def load_config(config_file: str) -> dict:
    """
    Loads a configuration file and returns its contents as a dictionary.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        dict: A dictionary representation of the configuration file.
    """
    config = configparser.ConfigParser()
    config.read(config_file)

    config_dict = {}

    for section in config.sections():
        config_dict[section] = {}
        
        for key, value in config.items(section):
            config_dict[section][key] = value

    return config_dict