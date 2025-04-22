from colorama import Fore


def rds_init_enum(victim_rds_client, attacker_rds_client):
    list_rds_instances(victim_rds_client)

def list_rds_instances(rds_client):
    print(f"{Fore.GREEN}Enumerating RDS Instances...")
    try:
        dbs = rds_client.describe_db_instances().get("DBInstances", [])
        for db in dbs:
            print(f"{Fore.MAGENTA}RDS: {db['DBInstanceIdentifier']} | Status: {db['DBInstanceStatus']}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list RDS instances")
