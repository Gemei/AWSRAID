from colorama import Fore


def ebs_init_enum(ec2_client, sts_client):
    list_ebs_volumes(ec2_client)
    list_ebs_snapshots(ec2_client, sts_client)

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
        response = ec2_client.describe_snapshots(OwnerIds=[aws_account_id], RestorableByUserIds=['all'])
        if response:
            for snapshot in response.get('Snapshots', []):
                print(f"{Fore.MAGENTA}Snapshot ID: {snapshot['SnapshotId']}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list EBS Snapshots")
