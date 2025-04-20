import modules.globals as my_globals
from colorama import Fore


def sts_init_enum(sts_client):
    whoami(sts_client)
    get_victim_aws_account_id(sts_client)

def whoami(sts_client):
    print(f"{Fore.GREEN}Getting caller identity...")
    sts_caller_info = sts_client.get_caller_identity()
    if sts_caller_info:
        print(f"{Fore.CYAN}KeyID: {sts_caller_info['UserId']}")
        print(f"{Fore.CYAN}Account: {sts_caller_info['Account']}")
        print(f"{Fore.CYAN}ARN: {sts_caller_info['Arn']}")

def get_victim_aws_account_id(sts_client):
    try:
        if my_globals.victim_aws_account_ID is None:
            my_globals.victim_aws_account_ID = sts_client.get_caller_identity()['Account']
    except:
        pass