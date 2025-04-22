from colorama import Fore


def ssm_init_enum(victim_ssm_client, attacker_ssm_client):
    list_ssm_parameters(victim_ssm_client)

def list_ssm_parameters(ssm_client):
    print(f"{Fore.GREEN}Enumerating SSM Parameters...")
    try:
        params = ssm_client.describe_parameters().get("Parameters", [])
        for param in params[:5]:
            print(f"{Fore.MAGENTA}SSM Parameter: {param['Name']}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list SSM parameters")
