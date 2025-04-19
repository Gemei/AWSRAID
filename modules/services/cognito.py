from colorama import Fore


def cognito_init_enum(cognito_client):
    list_cognito_users(cognito_client)

def list_cognito_users(cognito_client):
    print(f"{Fore.GREEN}Enumerating Cognito User Pools...")
    try:
        pools = cognito_client.list_user_pools(MaxResults=10).get("UserPools", [])
        for pool in pools:
            print(f"{Fore.MAGENTA}User Pool: {pool['Name']} | ID: {pool['Id']}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list Cognito user pools")
