import sys
from datetime import datetime
from colorama import Fore

def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def validate_config(config):
    victim_access_key = config.get("victim_access_key") or None
    victim_secret_access_key = config.get("victim_secret_access_key") or None
    victim_buckets = config.get("victim_buckets") or None
    victim_aws_account_ID = config.get("victim_aws_account_ID") or None

    attacker_access_key = config.get("attacker_access_key") or None
    attacker_secret_access_key = config.get("attacker_secret_access_key") or None
    attacker_IAM_role = config.get("attacker_IAM_role_name") or None
    attacker_S3_role = config.get("attacker_S3_role_arn") or None

    if not attacker_access_key and not attacker_secret_access_key:
        print(f"{Fore.YELLOW}[*] Attacker credentials not provided. The following features will be disabled:"
              f"\n   - Searching for public EBS snapshots using victim account ID"
              f"\n   - Brute-forcing AWS account IDs via exposed S3 or access key IDs"
              f"\n   - Brute-forcing IAM usernames and roles")

    if not attacker_IAM_role:
        print(f"{Fore.YELLOW}[*] Attacker IAM role name not set. IAM user and role enumeration will be skipped.")

    if not attacker_S3_role and not victim_buckets:
        print(f"{Fore.YELLOW}[*] No attacker S3 role or victim buckets provided. Cannot brute-force victim AWS account ID from public S3 buckets.")

    if not victim_access_key and not victim_secret_access_key:
        print(f"{Fore.YELLOW}[*] Victim credentials not provided. Only unauthenticated enumeration will be performed.")

    elif not victim_secret_access_key:
        print(f"{Fore.YELLOW}[*] Victim secret access key missing. Only basic account-level information can be retrieved.")

    if not victim_aws_account_ID:
        print(f"{Fore.YELLOW}[*] Victim AWS account ID not provided. Public EBS snapshot enumeration might be skipped.")

    if not attacker_access_key and not attacker_secret_access_key and not victim_secret_access_key and not victim_access_key:
        print(f"{Fore.RED}You didn't supply enough information in \"enum.config.json\" config file. Scan cannot run!")
        sys.exit(0)