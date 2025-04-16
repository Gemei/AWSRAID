import json, sys, os
from colorama import Fore, Style

def load_config(file_path):
    if not os.path.exists(file_path):
        print(f"{Fore.RED}Config file '{file_path}' not found.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Creating a template. Please fill in the values and rerun the script.{Style.RESET_ALL}")
        default_config = {
            "access_key": "YOUR_ACCESS_KEY",
            "secret_access_key": "YOUR_SECRET_ACCESS_KEY",
            "session_token": "OPTIONAL",
            "region": "DEFAULT_REGION",
            "buckets": ["OPTIONAL S3 BUCKETS. DELETE IF NOT REQUIRED"]
        }
        with open(file_path, "w") as f:
            json.dump(default_config, f, indent=4)
        sys.exit(1)
    with open(file_path, "r") as f:
        return json.load(f)
