import sys
import modules.globals as my_globals
from datetime import datetime
from colorama import Fore

def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def validate_config(config):
    my_globals.victim_access_key = config.get("victim_access_key") or None
    my_globals.victim_secret_access_key = config.get("victim_secret_access_key") or None
    my_globals.victim_session_token = config.get("victim_session_token") or None
    my_globals.victim_region = config.get("victim_region", "us-east-1")
    my_globals.victim_buckets = config.get("victim_buckets") or None
    my_globals.victim_aws_account_ID = config.get("victim_aws_account_ID") or None

    my_globals.attacker_access_key = config.get("attacker_access_key") or None
    my_globals.attacker_secret_access_key = config.get("attacker_secret_access_key") or None
    my_globals.attacker_region = config.get("attacker_region", "us-east-1")
    my_globals.attacker_IAM_role_name = config.get("attacker_IAM_role_name") or None
    my_globals.attacker_S3_role_arn = config.get("attacker_S3_role_arn") or None

    warnings = []
    errors = []

    if not my_globals.attacker_access_key and not my_globals.attacker_secret_access_key:
        warnings.append("[*] Attacker credentials not provided. The following features will be disabled:\n"
                        "   - Searching for public EBS snapshots using victim account ID\n"
                        "   - Brute-forcing AWS account IDs via exposed S3 or access key IDs\n"
                        "   - Brute-forcing IAM usernames and roles")

    if not my_globals.attacker_IAM_role_name:
        warnings.append("[*] Attacker IAM role name not set. IAM user and role enumeration will be skipped.")

    if not my_globals.attacker_S3_role_arn and not my_globals.victim_buckets:
        warnings.append("[*] No attacker S3 role or victim buckets provided. Cannot brute-force victim AWS account ID from public S3 buckets.")

    if not my_globals.victim_access_key and not my_globals.victim_secret_access_key:
        warnings.append("[*] Victim credentials not provided. Only unauthenticated enumeration will be performed.")
    elif not my_globals.victim_secret_access_key:
        warnings.append("[*] Victim secret access key missing. Only basic account-level information can be retrieved.")

    if not my_globals.victim_aws_account_ID:
        warnings.append("[*] Victim AWS account ID not provided. Public EBS snapshot enumeration might be skipped.")

    if all(not x for x in [my_globals.attacker_access_key, my_globals.attacker_secret_access_key,
                           my_globals.victim_secret_access_key, my_globals.victim_access_key]):
        errors.append("You didn't supply enough information in \"enum.config.json\" config file. Scan cannot run!")

    if all(not x for x in [my_globals.victim_access_key, my_globals.victim_buckets, my_globals.victim_aws_account_ID]):
        errors.append("You didn't supply enough information in \"enum.config.json\" config file. Scan cannot run!")

    for warning in warnings:
        print(f"{Fore.YELLOW}{warning}")

    if errors:
        for error in errors:
            print(f"{Fore.RED}{error}")
        sys.exit(0)
