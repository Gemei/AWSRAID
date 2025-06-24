from colorama import Fore
import json
from modules.utils import custom_serializer
import modules.globals as my_globals
from botocore.config import Config
from modules.logger import *

def macie_init_enum(victim_session, attacker_session):
    enable_print_logging()
    list_macie_findings(victim_session)

def list_macie_findings(victim_session):
    print(f"{Fore.GREEN}Enumerating Macie Findings...")
    config = Config(connect_timeout=5, read_timeout=10, retries={'max_attempts': 1})
    for region in my_globals.aws_regions:
        try:
            macie_client = victim_session.client("macie2", region_name=region, config=config)
            findings = macie_client.list_findings().get("findingIds", [])
            print(f"{Fore.MAGENTA}Region: {region} | Macie Findings Count: {len(findings)}")
            try:
                if findings:
                    details = macie_client.get_findings(findingIds=findings[:5]).get("findings", [])
                    print(f"{Fore.YELLOW}Sample Findings:\n{json.dumps(details, indent=4, sort_keys=True, default=custom_serializer)}")
            except KeyboardInterrupt:
                raise
            except IndexError as ie:
                print(f"{Fore.LIGHTBLACK_EX}Failed to get finding details in region {region}")
                log_error(f"Failed to get finding details in region {region}\n | Error:{ie}")
        except KeyboardInterrupt:
            raise
        except Exception as e:
            sys.stderr.write("\r\033[K")
            sys.stderr.write(f"{Fore.LIGHTBLACK_EX}Failed to list Macie findings in region {region}")
            sys.stderr.flush()
            log_error(f"\n | Error:{e}")
    print("")