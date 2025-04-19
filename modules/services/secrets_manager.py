import json
from colorama import Fore, Style
from modules.utils import custom_serializer

def sm_init_enum(secrets_client):
    enumerate_secrets_manager(secrets_client)

def enumerate_secrets_manager(secrets_client):
    print(f"{Fore.GREEN}Enumerating Secrets...{Style.RESET_ALL}")
    try:
        secrets_list = secrets_client.list_secrets()
        if secrets_list:
            for secret in secrets_list.get("SecretList"):
                name = secret["Name"]
                try:
                    secret_dump = secrets_client.get_secret_value(SecretId=name)
                    print(f"{Fore.MAGENTA}{json.dumps(secret_dump, indent=4, sort_keys=True, default=custom_serializer)}{Style.RESET_ALL}")
                except:
                    print(f"{Fore.LIGHTBLACK_EX}Failed to retrieve secret: {name}{Style.RESET_ALL}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list secrets{Style.RESET_ALL}")
