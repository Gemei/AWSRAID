from botocore.exceptions import ClientError
import modules.globals as my_globals
from colorama import Fore
from modules.logger import *

def sts_init_enum(victim_sts_client, attacker_sts_session):
    enable_print_logging()
    if victim_sts_client:
        get_victim_user(victim_sts_client)
    if attacker_sts_session and my_globals.victim_access_key and my_globals.victim_aws_account_ID is None :
        get_victim_aws_account_id(attacker_sts_session)

def get_victim_user(sts_client):
    print(f"{Fore.GREEN}[+] Getting caller identity:")
    try:
        sts_caller_info = sts_client.get_caller_identity()
        if sts_caller_info:
            print(f"{Fore.CYAN} | KeyID: {sts_caller_info['UserId']}")
            print(f"{Fore.CYAN} | Account: {sts_caller_info['Account']}")
            print(f"{Fore.CYAN} | ARN: {sts_caller_info['Arn']}")
        if my_globals.victim_aws_account_ID is None:
            my_globals.victim_aws_account_ID = sts_caller_info['Account']
        if "assumed-role" in sts_caller_info["Arn"]:
            my_globals.victim_aws_role_name = sts_caller_info["Arn"].split("/")[1]
        else:
            my_globals.victim_aws_username = sts_caller_info["Arn"].split("/")[-1]
    except KeyboardInterrupt:
        raise
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']

        if error_code == "AccessDenied":
            print(
                f"{Fore.YELLOW}Access denied with provided credentials:"
                f"\nAccess Key: {my_globals.victim_access_key}"
                f"\nSecret Key: {my_globals.victim_secret_access_key}"
                f"\nSecurity Token: {my_globals.victim_session_token}"
                f"\nError: {error_message}"
                f"\nContinuing enumeration, but functionality may be limited...",
                file=sys.stderr
            )
        elif error_code in ["InvalidClientTokenId", "UnrecognizedClientException"]:
            print(
                f"{Fore.RED}Invalid AWS credentials:"
                f"\nAccess Key: {my_globals.victim_access_key}"
                f"\nSecret Key: {my_globals.victim_secret_access_key}"
                f"\nSecurity Token: {my_globals.victim_session_token}"
                f"\nError: {error_message}",
                file=sys.stderr
            )
            exit(1)
        else:
            print(
                f"{Fore.RED}ClientError occurred:"
                f"\nError Code: {error_code}"
                f"\nError: {error_message}"
                f"\nExiting...",
                file=sys.stderr
            )
            exit(1)

def get_victim_aws_account_id(attacker_sts_session):
    print(f"{Fore.GREEN}[+] Getting AWS account ID from victim access key {my_globals.victim_access_key}:")
    try:
        if my_globals.victim_access_key is not None:
            sts_client = attacker_sts_session.client("sts")
            sts_caller_info = sts_client.get_access_key_info(AccessKeyId=my_globals.victim_access_key)
            my_globals.victim_aws_account_ID = sts_caller_info['Account']
            print(f"{Fore.CYAN} | Victim's AWS Account ID: {my_globals.victim_aws_account_ID}")
        else:
            print(f"{Fore.YELLOW} | Victim access key was not provided")
    except KeyboardInterrupt:
        raise
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        if error_code == "InvalidClientTokenId":
            print(f"{Fore.LIGHTBLACK_EX} | Failed to retrieve victim AWS account using access key: {my_globals.victim_access_key}"
                  f" | Error: {error_message}",
                  file=sys.stderr
            )
        else:
            print(
                f"{Fore.LIGHTBLACK_EX}ClientError occurred:"
                f"\nError Code: {error_code}"
                f"\nError: {error_message}",
                file=sys.stderr
            )
