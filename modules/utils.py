import sys
import modules.globals as my_globals
from datetime import datetime
from colorama import Fore

def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def validate_config(config):
    if not my_globals.attacker_access_key and not my_globals.attacker_secret_access_key:
        print(f"{Fore.YELLOW}[*] Attacker credentials not provided. The following features will be disabled:"
              f"\n   - Searching for public EBS snapshots using victim account ID"
              f"\n   - Brute-forcing AWS account IDs via exposed S3 or access key IDs"
              f"\n   - Brute-forcing IAM usernames and roles")

    if not my_globals.attacker_IAM_role_name:
        print(f"{Fore.YELLOW}[*] Attacker IAM role name not set. IAM user and role enumeration will be skipped.")

    if not my_globals.attacker_S3_role_arn and not my_globals.victim_buckets:
        print(f"{Fore.YELLOW}[*] No attacker S3 role or victim buckets provided. Cannot brute-force victim AWS account ID from public S3 buckets.")

    if not my_globals.victim_access_key and not my_globals.victim_secret_access_key:
        print(f"{Fore.YELLOW}[*] Victim credentials not provided. Only unauthenticated enumeration will be performed.")

    elif not my_globals.victim_secret_access_key:
        print(f"{Fore.YELLOW}[*] Victim secret access key missing. Only basic account-level information can be retrieved.")

    if not my_globals.victim_aws_account_ID:
        print(f"{Fore.YELLOW}[*] Victim AWS account ID not provided. Public EBS snapshot enumeration might be skipped.")

    if not my_globals.attacker_access_key and not my_globals.attacker_secret_access_key and not my_globals.victim_secret_access_key and not my_globals.victim_access_key:
        print(f"{Fore.RED}You didn't supply enough information in \"enum.config.json\" config file. Scan cannot run!")
        sys.exit(0)

    if not my_globals.victim_access_key and not my_globals.victim_buckets and not my_globals.victim_aws_account_ID:
        print(f"{Fore.RED}You didn't supply enough information in \"enum.config.json\" config file. Scan cannot run!")
        sys.exit(0)