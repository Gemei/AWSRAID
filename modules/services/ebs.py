from colorama import Fore, Style

def ebs_init_enum(ec2_client, sts_client):
    enumerate_ebs_volumes(ec2_client)
    enumerate_ebs_snapshots(ec2_client, sts_client)

def enumerate_ebs_volumes(ec2_client):
    print(f"{Fore.GREEN}Enumerating EBS Volumes...{Style.RESET_ALL}")
    try:
        volumes = ec2_client.describe_volumes().get("Volumes", [])
        for volume in volumes:
            print(f"{Fore.MAGENTA}Volume ID: {volume['VolumeId']} | State: {volume['State']}{Style.RESET_ALL}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list EBS volumes{Style.RESET_ALL}")

def enumerate_ebs_snapshots(ec2_client, sts_client):
    print(f"{Fore.GREEN}Enumerating EBS Snapshots...{Style.RESET_ALL}")
    try:
        aws_account_id = sts_client.get_caller_identity()['Account']
        response = ec2_client.describe_snapshots(OwnerIds=[aws_account_id], RestorableByUserIds=['all'])
        if response:
            for snapshot in response.get('Snapshots', []):
                print(f"{Fore.MAGENTA}Snapshot ID: {snapshot['SnapshotId']}{Style.RESET_ALL}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list EBS Snapshots{Style.RESET_ALL}")
