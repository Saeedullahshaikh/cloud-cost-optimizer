import requests
import yaml
from notify import send_email
import os

CONFIG = yaml.safe_load(open("config/config.yaml"))

def check_service(url):
    try:
        res = requests.get(url, timeout=5)
        return res.status_code == 200
    except:
        return False


def monitor():
    sender = CONFIG["email"]["sender"]
    password = CONFIG["email"]["password"]
    receiver = CONFIG["email"]["receiver"]

    logs = []

    for target in CONFIG["monitor_targets"]:
        name = target["name"]
        url = target["url"]

        healthy = check_service(url)

        if healthy:
            logs.append(f"{name}: OK (Healthy)")
        else:
            logs.append(f"{name}: DOWN (Critical)")
            send_email(
                "CRITICAL ALERT",
                f"{name} is DOWN. Attempting auto fix...",
                sender, password, receiver
            )
            os.system("python3 scripts/auto_fix.py")

    send_email("Daily Status Report", "\n".join(logs), sender, password, receiver)


if __name__ == "__main__":
    monitor()
