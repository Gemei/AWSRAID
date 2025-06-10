from colorama import Fore
import json, sys
from modules.utils import custom_serializer
import modules.globals as my_globals

def rds_init_enum(victim_session, attacker_session):
    list_rds_instances(victim_session)

def list_rds_instances(victim_session):
    print(f"{Fore.GREEN}Enumerating RDS Instances...")
    for region in my_globals.aws_regions:
        try:
            rds_client = victim_session.client("rds", region_name=region)
            dbs = rds_client.describe_db_instances().get("DBInstances", [])
            for db in dbs:
                print(f"{Fore.MAGENTA}\nRegion: {region} | RDS: {db['DBInstanceIdentifier']} | Status: {db['DBInstanceStatus']}")
                try:
                    print(f"{Fore.YELLOW}{json.dumps(db, indent=4, sort_keys=True, default=custom_serializer)}")
                except KeyboardInterrupt:
                    raise
                except:
                    print(f"{Fore.LIGHTBLACK_EX}Failed to format RDS instance data for {db['DBInstanceIdentifier']}")
        except KeyboardInterrupt:
            raise
        except:
            sys.stdout.write("\r\033[K")
            sys.stdout.write(f"{Fore.LIGHTBLACK_EX}Failed to list RDS instances in region {region}")
            sys.stdout.flush()
    print("")