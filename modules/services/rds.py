from colorama import Fore
import json
from modules.utils import custom_serializer
import modules.globals as my_globals
from modules.logger import *

def rds_init_enum(victim_session, attacker_session):
    enable_print_logging()
    if victim_session:
        list_rds_instances(victim_session)
    if attacker_session:
        list_rds_public_snapshots(attacker_session)
        list_rds_public_cluster_snapshots(attacker_session)

def list_rds_instances(victim_session):
    print(f"{Fore.GREEN}[+] Enumerating RDS Instances:")
    for region in my_globals.aws_regions:
        try:
            rds_client = victim_session.client("rds", region_name=region)
            dbs = rds_client.describe_db_instances().get("DBInstances", [])
            for db in dbs:
                print(f"{Fore.MAGENTA} | Region: {region} | RDS: {db['DBInstanceIdentifier']} | Status: {db['DBInstanceStatus']}")
                try:
                    print(f"{Fore.YELLOW}   {json.dumps(db, indent=4, sort_keys=True, default=custom_serializer)}")
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"{Fore.LIGHTBLACK_EX} | Failed to format RDS instance data for {db['DBInstanceIdentifier']}")
                    log_error(f"Failed to format RDS instance data for {db['DBInstanceIdentifier']}\n | Error:{e}")
        except KeyboardInterrupt:
            raise
        except Exception as e:
            sys.stderr.write("\r\033[K")
            sys.stderr.write(f"{Fore.LIGHTBLACK_EX} | Failed to list RDS instances in region {region}")
            sys.stderr.flush()
            log_error(f"\n | Error:{e}")
    print("")

def list_rds_public_snapshots(attacker_session):
    print(f"{Fore.GREEN}[+] Enumerating Public RDS Snapshots for Account: {my_globals.victim_aws_account_ID}:")
    for region in my_globals.aws_regions:
        try:
            attacker_rds_client = attacker_session.client("rds", region_name=region)
            response = attacker_rds_client.describe_db_snapshots(
                SnapshotType='public',
                IncludePublic=True
            )
            found_victim_snapshots = 0
            snapshots = response.get('DBSnapshots', [])
            if snapshots:
                for snapshot in snapshots:
                    snapshot_arn = snapshot.get('DBSnapshotArn', '').split(":")[4]
                    if snapshot_arn in my_globals.victim_aws_account_ID:
                        print(f"{Fore.MAGENTA} | Region: {region} | Snapshot ID: {snapshot.get('DBClusterSnapshotArn', '')}")
                        found_victim_snapshots += 1
            else:
                sys.stdout.write("\r\033[K")
                sys.stdout.write(f"{Fore.LIGHTBLACK_EX} | No public RDS snapshots found in region {region} for account {my_globals.victim_aws_account_ID}")
                sys.stdout.flush()
            if found_victim_snapshots == 0:
                sys.stdout.write("\r\033[K")
                sys.stdout.write(f"{Fore.LIGHTBLACK_EX} | No public RDS snapshots found in region {region} for account {my_globals.victim_aws_account_ID}")
                sys.stdout.flush()

        except KeyboardInterrupt:
            raise
        except Exception as e:
            sys.stderr.write("\r\033[K")
            sys.stderr.write(f"{Fore.LIGHTBLACK_EX} | Failed to list public RDS snapshots in region {region}")
            sys.stderr.flush()
            log_error(f"\n | Error: {e}")
    print("")

def list_rds_public_cluster_snapshots(attacker_session):
    print(f"{Fore.GREEN}[+] Enumerating Public RDS Cluster Snapshots for Account: {my_globals.victim_aws_account_ID}:")
    for region in my_globals.aws_regions:
        try:
            attacker_rds_client = attacker_session.client("rds", region_name=region)
            response = attacker_rds_client.describe_db_cluster_snapshots(
                SnapshotType='public',
                IncludePublic=True
            )
            found_victim_snapshots = 0
            snapshots = response.get('DBClusterSnapshots', [])
            if snapshots:
                for snapshot in snapshots:
                    snapshot_arn = snapshot.get('DBClusterSnapshotArn', '').split(":")[4]
                    if snapshot_arn in my_globals.victim_aws_account_ID:
                        print(f"{Fore.MAGENTA} | Region: {region} | RDS Cluster Snapshot ID: {snapshot.get('DBClusterSnapshotArn', '')}")
                        found_victim_snapshots += 1
            else:
                sys.stdout.write("\r\033[K")
                sys.stdout.write(f"{Fore.LIGHTBLACK_EX} | No public RDS cluster snapshots found in region {region} for account {my_globals.victim_aws_account_ID}")
                sys.stdout.flush()
            if found_victim_snapshots == 0:
                sys.stdout.write("\r\033[K")
                sys.stdout.write(f"{Fore.LIGHTBLACK_EX} | No public RDS cluster snapshots found in region {region} for account {my_globals.victim_aws_account_ID}")
                sys.stdout.flush()

        except KeyboardInterrupt:
            raise
        except Exception as e:
            sys.stderr.write("\r\033[K")
            sys.stderr.write(f"{Fore.LIGHTBLACK_EX} | Failed to list public RDS cluster snapshots in region {region}")
            sys.stderr.flush()
            log_error(f"\n | Error: {e}")
    print("")