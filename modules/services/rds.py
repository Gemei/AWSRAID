from colorama import Fore, Style

def enumerate_rds_instances(rds_client):
    print(f"{Fore.GREEN}Enumerating RDS Instances...{Style.RESET_ALL}")
    try:
        dbs = rds_client.describe_db_instances().get("DBInstances", [])
        for db in dbs:
            print(f"{Fore.MAGENTA}RDS: {db['DBInstanceIdentifier']} | Status: {db['DBInstanceStatus']}{Style.RESET_ALL}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list RDS instances{Style.RESET_ALL}")
