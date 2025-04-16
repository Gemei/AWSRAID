from colorama import Fore, Style

def enumerate_ssm_parameters(ssm_client):
    print(f"{Fore.GREEN}Enumerating SSM Parameters...{Style.RESET_ALL}")
    try:
        params = ssm_client.describe_parameters().get("Parameters", [])
        for param in params[:5]:
            print(f"{Fore.MAGENTA}SSM Parameter: {param['Name']}{Style.RESET_ALL}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list SSM parameters{Style.RESET_ALL}")
