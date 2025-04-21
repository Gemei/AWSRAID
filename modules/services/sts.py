import modules.globals as my_globals
from colorama import Fore

def sts_init_enum(victim_sts_client, attacker_sts_client):
    if victim_sts_client:
        get_victim_user(victim_sts_client)
    if attacker_sts_client:
        get_victim_aws_account_id(attacker_sts_client)

def get_victim_user(sts_client):
    print(f"{Fore.GREEN}Getting caller identity...")
    sts_caller_info = sts_client.get_caller_identity()
    if sts_caller_info:
        print(f"{Fore.CYAN}KeyID: {sts_caller_info['UserId']}")
        print(f"{Fore.CYAN}Account: {sts_caller_info['Account']}")
        print(f"{Fore.CYAN}ARN: {sts_caller_info['Arn']}")
    if my_globals.victim_aws_account_ID is None:
        my_globals.victim_aws_account_ID = sts_client.get_caller_identity()['Account']
    my_globals.victim_aws_username = sts_caller_info["Arn"].split("/")[-1]

def get_victim_aws_account_id(sts_client):
    try:
        if my_globals.victim_aws_account_ID is None and my_globals.victim_access_key is not None:
            sts_caller_info = sts_client.get_access_key_info(AccessKeyId=my_globals.victim_access_key)
            my_globals.victim_aws_account_ID = sts_caller_info['Account']
            print(f"{Fore.CYAN}Victim's AWS Account ID: {my_globals.victim_aws_account_ID}")
        else:
            print(f"{Fore.YELLOW} Victim access key was not provided")
    except Exception as e:
        print(f"{Fore.LIGHTBLACK_EX}Failed to retrieve victim AWS account using access key: {my_globals.victim_access_key}\n{e}")