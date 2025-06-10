import modules.globals as my_globals
from colorama import Fore
import sys

def ec2_init_enum(victim_session, attacker_session):
    enumerate_ec2(victim_session)
    if victim_session:
        list_ebs_volumes(victim_session)
        list_ebs_snapshots(victim_session)
    if attacker_session and my_globals.victim_aws_account_ID:
        list_ebs_public_snapshots(attacker_session)

def enumerate_ec2(victim_session):
    print(f"{Fore.GREEN}Enumerating EC2 Instances...")
    for region in my_globals.aws_regions:
        try:
            ec2_client = victim_session.client("ec2", region),
            reservations = ec2_client.describe_instances().get("Reservations", [])
            for reservation in reservations:
                for instance in reservation.get("Instances", []):
                    print(f"{Fore.MAGENTA}\nRegion {region} | Instance ID: {instance['InstanceId']} | State: {instance['State']['Name']}")
                    describe_ec2_instance(instance)
        except KeyboardInterrupt:
            raise
        except:
            sys.stdout.write("\r\033[K")  # \033[K clears from cursor to end of line
            sys.stdout.write(f"{Fore.LIGHTBLACK_EX}Failed to list EC2 instances in region {region}")
            sys.stdout.flush()
    print("")

def describe_ec2_instance(instance):
    try:
        instance_id = instance['InstanceId']
        instance_type = instance.get('InstanceType', 'N/A')
        public_ip = instance.get('PublicIpAddress', 'N/A')
        private_ip = instance.get('PrivateIpAddress', 'N/A')
        state = instance.get('State', {}).get('Name', 'N/A')
        key_name = instance.get('KeyName', 'N/A')
        tags = instance.get('Tags', [])

        print(f"{Fore.YELLOW}Details for Instance {instance_id}:")
        print(f"{Fore.YELLOW}  Type: {instance_type}")
        print(f"{Fore.YELLOW}  State: {state}")
        print(f"{Fore.YELLOW}  Public IP: {public_ip}")
        print(f"{Fore.YELLOW}  Private IP: {private_ip}")
        print(f"{Fore.YELLOW}  Key Name: {key_name}")
        if tags:
            print(f"{Fore.YELLOW}  Tags:")
            for tag in tags:
                print(f"{Fore.YELLOW}    {tag['Key']}: {tag['Value']}")
    except KeyboardInterrupt:
        raise
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to describe EC2 instance")

def list_ebs_volumes(victim_session):
    print(f"{Fore.GREEN}Enumerating EBS Volumes...")
    for region in my_globals.aws_regions:
        try:
            ec2_client = victim_session.client("ec2", region)
            volumes = ec2_client.describe_volumes().get("Volumes", [])
            for volume in volumes:
                print(f"{Fore.MAGENTA}\nRegion {region} | Volume ID: {volume['VolumeId']} | State: {volume['State']}")
        except KeyboardInterrupt:
            raise
        except:
            sys.stdout.write("\r\033[K")  # \033[K clears from cursor to end of line
            sys.stdout.write(f"{Fore.LIGHTBLACK_EX}Failed to list EBS volumes in region {region}")
            sys.stdout.flush()
    print("")
def list_ebs_snapshots(victim_session):
    print(f"{Fore.GREEN}Enumerating EBS Snapshots...")
    for region in my_globals.aws_regions:
        try:
            ec2_client = victim_session.client("ec2", region)
            aws_account_id = my_globals.victim_aws_account_ID
            response = ec2_client.describe_snapshots(OwnerIds=[aws_account_id])
            if response:
                for snapshot in response.get('Snapshots', []):
                    print(f"{Fore.MAGENTA}Snapshot ID: {snapshot['SnapshotId']}")
        except KeyboardInterrupt:
            raise
        except:
            sys.stdout.write("\r\033[K")  # \033[K clears from cursor to end of line
            sys.stdout.write(f"{Fore.LIGHTBLACK_EX}Failed to list EBS snapshots in region {region}")
            sys.stdout.flush()
    print("")
def list_ebs_public_snapshots(attacker_session):
    print(f"{Fore.GREEN}Enumerating Public EBS Snapshots for Account: {my_globals.victim_aws_account_ID}...")
    for region in my_globals.aws_regions:
        try:
            attacker_ec2_client = attacker_session.client("ec2", region)
            response = attacker_ec2_client.describe_snapshots(OwnerIds=[my_globals.victim_aws_account_ID], RestorableByUserIds=['all'])
            snapshots = response.get('Snapshots', [])
            if snapshots:
                for snapshot in snapshots:
                    print(f"{Fore.MAGENTA}\nRegion: {region} | Snapshot ID: {snapshot['SnapshotId']}")
            else:
                sys.stdout.write("\r\033[K")  # \033[K clears from cursor to end of line
                sys.stdout.write(f"{Fore.LIGHTBLACK_EX}No public snapshots found in region {region}")
                sys.stdout.flush()
        except KeyboardInterrupt:
            raise
        except:
            sys.stdout.write("\r\033[K")  # \033[K clears from cursor to end of line
            sys.stdout.write(f"{Fore.LIGHTBLACK_EX}Failed to list public EBS snapshots in region {region}")
            sys.stdout.flush()
    print("")