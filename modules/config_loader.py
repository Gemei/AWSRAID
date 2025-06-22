import json, sys, os
from colorama import Fore

def load_config(file_path):
    if not os.path.exists(file_path):
        print(f"{Fore.RED}Config file '{file_path}' not found.")
        print(f"{Fore.YELLOW}Creating a template. Please fill in the values and rerun the script.")
        default_config = {
            "victim_access_key": "",
            "victim_secret_access_key": "",
            "victim_session_token": "",
            "victim_buckets": [],
            "victim_aws_account_ID": "",
            "victim_regions": ["us-east-1","us-east-2","us-west-1","us-west-2","ca-central-1","ca-west-1","eu-central-1","eu-central-2","eu-north-1","eu-south-1","eu-south-2","eu-west-1","eu-west-2","eu-west-3"],
            "attacker_access_key": "",
            "attacker_secret_access_key": "",
            "attacker_region": "",
            "attacker_IAM_role_name": "",
            "attacker_S3_role_arn": "",
            "user_name_wordlist": "./wordlists/pacu_usernames_word_list.txt",
            "start_username_brute_force": False,
            "role_name_wordlist": "./wordlists/pacu_role_names_word_list.txt",
            "start_role_name_brute_force": False
        }
        with open(file_path, "w") as f:
            json.dump(default_config, f, indent=4)
        sys.exit(1)
    with open(file_path, "r") as f:
        return json.load(f)
