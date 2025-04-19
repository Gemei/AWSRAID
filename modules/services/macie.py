from colorama import Fore, Style

def macie_init_enum(macie_client):
    enumerate_macie_findings(macie_client)

def enumerate_macie_findings(macie_client):
    print(f"{Fore.GREEN}Enumerating Macie Findings...{Style.RESET_ALL}")
    try:
        findings = macie_client.list_findings().get("findingIds", [])
        print(f"{Fore.MAGENTA}Macie Findings Count: {len(findings)}{Style.RESET_ALL}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to get Macie findings{Style.RESET_ALL}")
