from colorama import Fore
import json, sys
from modules.utils import custom_serializer
import modules.globals as my_globals

def macie_init_enum(victim_session, attacker_session):
    list_macie_findings(victim_session)

def list_macie_findings(victim_session):
    print(f"{Fore.GREEN}Enumerating Macie Findings...")
    for region in my_globals.aws_regions:
        try:
            macie_client = victim_session.client("macie2", region_name=region)
            findings = macie_client.list_findings().get("findingIds", [])
            print(f"{Fore.MAGENTA}\nRegion: {region} | Macie Findings Count: {len(findings)}")
            try:
                if findings:
                    details = macie_client.get_findings(findingIds=findings[:5]).get("findings", [])
                    print(f"{Fore.YELLOW}Sample Findings:\n{json.dumps(details, indent=4, sort_keys=True, default=custom_serializer)}")
            except KeyboardInterrupt:
                raise
            except:
                print(f"{Fore.LIGHTBLACK_EX}Failed to get finding details in region {region}")
        except KeyboardInterrupt:
            raise
        except:
            sys.stdout.write("\r\033[K")
            sys.stdout.write(f"{Fore.LIGHTBLACK_EX}Failed to list Macie findings in region {region}")
            sys.stdout.flush()
    print("")