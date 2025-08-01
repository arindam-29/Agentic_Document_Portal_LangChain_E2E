import yaml
import os

def load_config(config_path: str = os.path.join("config", "config.yaml")) -> dict:
    with open(config_path, "r") as file:
        config=yaml.safe_load(file)
    return config

# Testing cell:
if __name__=="__main__":
    config = load_config()
    print(config)