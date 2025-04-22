import modules.globals as my_globals
from colorama import Fore

def ebs_init_enum(victim_ec2_client, victim_sts_client, attacker_ec2_client):
    if victim_ec2_client and victim_sts_client:
        list_ebs_volumes(victim_ec2_client)
        list_ebs_snapshots(victim_ec2_client, victim_sts_client)
    if attacker_ec2_client and my_globals.victim_aws_account_ID:
        list_ebs_public_snapshots(attacker_ec2_client, my_globals.victim_aws_account_ID)

def list_ebs_volumes(ec2_client):
    print(f"{Fore.GREEN}Enumerating EBS Volumes...")
    try:
        volumes = ec2_client.describe_volumes().get("Volumes", [])
        for volume in volumes:
            print(f"{Fore.MAGENTA}Volume ID: {volume['VolumeId']} | State: {volume['State']}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list EBS volumes")

def list_ebs_snapshots(ec2_client, sts_client):
    print(f"{Fore.GREEN}Enumerating EBS Snapshots...")
    try:
        aws_account_id = sts_client.get_caller_identity()['Account']
        response = ec2_client.describe_snapshots(OwnerIds=[aws_account_id])
        if response:
            for snapshot in response.get('Snapshots', []):
                print(f"{Fore.MAGENTA}Snapshot ID: {snapshot['SnapshotId']}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list EBS Snapshots")

def list_ebs_public_snapshots(attacker_ec2_client, aws_account_id):
    print(f"{Fore.GREEN}Enumerating Public EBS Snapshots for Account: {aws_account_id}...")
    try:
        response = attacker_ec2_client.describe_snapshots(OwnerIds=[aws_account_id], RestorableByUserIds=['all'])
        snapshots = response.get('Snapshots', [])
        if snapshots:
            for snapshot in snapshots:
                print(f"{Fore.MAGENTA}Snapshot ID: {snapshot['SnapshotId']}")
        else:
            print(f"{Fore.LIGHTBLACK_EX}No public snapshots found for AWS account: {aws_account_id}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list public EBS Snapshots for account: {aws_account_id}")