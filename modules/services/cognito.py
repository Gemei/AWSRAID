from colorama import Fore
import sys
import modules.globals as my_globals

def cognito_init_enum(victim_session, attacker_session):
    list_cognito_users(victim_session)

def list_cognito_users(victim_session):
    print(f"{Fore.GREEN}Enumerating Cognito User Pools...")
    for region in my_globals.aws_regions:
        try:
            cognito_client = victim_session.client("cognito-idp", region_name=region)
            pools = cognito_client.list_user_pools(MaxResults=60).get("UserPools", [])
            for pool in pools:
                print(f"{Fore.MAGENTA}\nRegion: {region} | User Pool: {pool['Name']} | ID: {pool['Id']}")
                try:
                    users = cognito_client.list_users(UserPoolId=pool['Id']).get("Users", [])
                    for user in users:
                        print(f"{Fore.MAGENTA}Region: {region} | Pool: {pool['Name']} | User: {user.get('Username')} | Status: {user.get('UserStatus')}")
                except:
                    print(f"{Fore.LIGHTBLACK_EX}Failed to list users in pool {pool['Id']}")
        except:
            sys.stdout.write("\r\033[K")
            sys.stdout.write(f"{Fore.LIGHTBLACK_EX}Failed to list Cognito user pools in region {region}")
            sys.stdout.flush()
    print("")