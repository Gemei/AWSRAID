from colorama import Fore, Style

def whoami(sts_client):
    print(f"{Fore.GREEN}Getting caller identity...{Style.RESET_ALL}")
    sts_caller_info = sts_client.get_caller_identity()
    if sts_caller_info:
        print(f"{Fore.CYAN}KeyID: {sts_caller_info['UserId']}")
        print(f"{Fore.CYAN}Account: {sts_caller_info['Account']}")
        print(f"{Fore.CYAN}ARN: {sts_caller_info['Arn']}{Style.RESET_ALL}")
