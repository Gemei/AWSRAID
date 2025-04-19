from colorama import Fore


def macie_init_enum(macie_client):
    list_macie_findings(macie_client)

def list_macie_findings(macie_client):
    print(f"{Fore.GREEN}Enumerating Macie Findings...")
    try:
        findings = macie_client.list_findings().get("findingIds", [])
        print(f"{Fore.MAGENTA}Macie Findings Count: {len(findings)}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to get Macie findings")
