import yaml
import os

CONFIG = yaml.safe_load(open("config/config.yaml"))

def auto_fix():
    container = CONFIG["auto_fix"]["docker_container_name"]
    print(f"Restarting container: {container}")
    os.system(f"docker restart {container}")


if __name__ == "__main__":
    auto_fix()
