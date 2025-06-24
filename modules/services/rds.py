from colorama import Fore
import json
from modules.utils import custom_serializer
import modules.globals as my_globals
from modules.logger import *

def rds_init_enum(victim_session, attacker_session):
    enable_print_logging()
    list_rds_instances(victim_session)

def list_rds_instances(victim_session):
    print(f"{Fore.GREEN}Enumerating RDS Instances...")
    for region in my_globals.aws_regions:
        try:
            rds_client = victim_session.client("rds", region_name=region)
            dbs = rds_client.describe_db_instances().get("DBInstances", [])
            for db in dbs:
                print(f"{Fore.MAGENTA}Region: {region} | RDS: {db['DBInstanceIdentifier']} | Status: {db['DBInstanceStatus']}")
                try:
                    print(f"{Fore.YELLOW}{json.dumps(db, indent=4, sort_keys=True, default=custom_serializer)}")
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"{Fore.LIGHTBLACK_EX}Failed to format RDS instance data for {db['DBInstanceIdentifier']}")
                    log_error(f"Failed to format RDS instance data for {db['DBInstanceIdentifier']}\n | Error:{e}")
        except KeyboardInterrupt:
            raise
        except Exception as e:
            sys.stdout.write("\r\033[K")
            sys.stdout.write(f"{Fore.LIGHTBLACK_EX}Failed to list RDS instances in region {region}")
            sys.stdout.flush()
            log_error(f"Failed to list RDS instances in region {region}\n | Error:{e}")
    print("")