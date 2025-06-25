import modules.globals as my_globals
from colorama import Fore
import base64
from modules.logger import *

def ec2_init_enum(victim_session, attacker_session):
    enable_print_logging()
    if victim_session:
        enumerate_ec2(victim_session)
        list_ebs_volumes(victim_session)
        list_ebs_snapshots(victim_session)
    if attacker_session and my_globals.victim_aws_account_ID:
        list_ebs_public_snapshots(attacker_session)

def enumerate_ec2(victim_session):
    print(f"{Fore.GREEN}[+] Enumerating EC2 Instances:")
    for region in my_globals.aws_regions:
        try:
            ec2_client = victim_session.client("ec2", region)
            reservations = ec2_client.describe_instances().get("Reservations", [])
            for reservation in reservations:
                for instance in reservation.get("Instances", []):
                    print(f"{Fore.MAGENTA} | Region {region} | Instance ID: {instance['InstanceId']} | State: {instance['State']['Name']}")
                    print(f"{Fore.CYAN} | Instance information:")
                    describe_ec2_instance(instance)
                    print(f"{Fore.CYAN} | Instance userdata:")
                    get_userdata(ec2_client, instance)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            sys.stderr.write("\r\033[K")  # \033[K clears from cursor to end of line
            sys.stderr.write(f"{Fore.LIGHTBLACK_EX} | Failed to list EC2 instances in region {region}")
            sys.stderr.flush()
            log_error(f"\n | Error:{e}")
    print("")

def describe_ec2_instance(instance):
    try:
        instance_id = instance['InstanceId']
        instance_type = instance.get('InstanceType', 'N/A')
        public_ip = instance.get('PublicIpAddress', 'N/A')
        private_ip = instance.get('PrivateIpAddress', 'N/A')
        state = instance.get('State', {}).get('Name', 'N/A')
        key_name = instance.get('KeyName', 'N/A')
        iam_instance_profile = instance.get('IamInstanceProfile', {}).get('Arn', 'N/A')
        tags = instance.get('Tags', [])

        print(f"{Fore.YELLOW} | Details for Instance {instance_id}:")
        print(f"{Fore.YELLOW}  | Type: {instance_type}")
        print(f"{Fore.YELLOW}  | State: {state}")
        print(f"{Fore.YELLOW}  | Public IP: {public_ip}")
        print(f"{Fore.YELLOW}  | Private IP: {private_ip}")
        print(f"{Fore.YELLOW}  | Key Name: {key_name}")
        print(f"{Fore.YELLOW}  | Instance Profile: {iam_instance_profile}")
        if tags:
            print(f"{Fore.YELLOW}  | Tags:")
            for tag in tags:
                print(f"{Fore.YELLOW}   | {tag['Key']}: {tag['Value']}")
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"{Fore.LIGHTBLACK_EX} | Failed to describe EC2 instance: {instance_id}")
        log_error(f"Failed to describe EC2 instance: {instance_id}\n | Error:{e}")

def get_userdata(ec2_client, instance):
    try:
        instance_id = instance['InstanceId']
        user_data_resp = ec2_client.describe_instance_attribute(
            InstanceId=instance_id,
            Attribute='userData'
        )
        user_data = user_data_resp.get('UserData', {}).get('Value')
        if user_data:
            decoded_user_data = base64.b64decode(user_data).decode('utf-8')
            print(f"{Fore.YELLOW} | User Data:\n  {decoded_user_data}")
        else:
            print(f"{Fore.YELLOW} | User Data: None")
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"{Fore.LIGHTBLACK_EX} | Failed to get EC2 instance {instance_id} userdata")
        log_error(f"Failed to get EC2 instance {instance_id} userdata\n | Error:{e}")

def list_ebs_volumes(victim_session):
    print(f"{Fore.GREEN}[+] Enumerating EBS Volumes:")
    for region in my_globals.aws_regions:
        try:
            ec2_client = victim_session.client("ec2", region)
            volumes = ec2_client.describe_volumes().get("Volumes", [])
            for volume in volumes:
                print(f"{Fore.MAGENTA} | Region {region} | Volume ID: {volume['VolumeId']} | State: {volume['State']}")
        except KeyboardInterrupt:
            raise
        except Exception as e:
            sys.stderr.write("\r\033[K")  # \033[K clears from cursor to end of line
            sys.stderr.write(f"{Fore.LIGHTBLACK_EX} | Failed to list EBS volumes in region {region}")
            sys.stderr.flush()
            log_error(f"\n | Error:{e}")
    print("")

def list_ebs_snapshots(victim_session):
    print(f"{Fore.GREEN}[+] Enumerating EBS Snapshots:")
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
        except Exception as e:
            sys.stderr.write("\r\033[K")  # \033[K clears from cursor to end of line
            sys.stderr.write(f"{Fore.LIGHTBLACK_EX} | Failed to list EBS snapshots in region {region}")
            sys.stderr.flush()
            log_error(f"\n | Error:{e}")
    print("")

def list_ebs_public_snapshots(attacker_session):
    print(f"{Fore.GREEN}[+] Enumerating Public EBS Snapshots for Account: {my_globals.victim_aws_account_ID}:")
    for region in my_globals.aws_regions:
        try:
            attacker_ec2_client = attacker_session.client("ec2", region)
            response = attacker_ec2_client.describe_snapshots(OwnerIds=[my_globals.victim_aws_account_ID], RestorableByUserIds=['all'])
            snapshots = response.get('Snapshots', [])
            if snapshots:
                for snapshot in snapshots:
                    print(f"{Fore.MAGENTA} | Region: {region} | Snapshot ID: {snapshot['SnapshotId']}")
            else:
                sys.stdout.write("\r\033[K")  # \033[K clears from cursor to end of line
                sys.stdout.write(f"{Fore.LIGHTBLACK_EX} | No public EBS snapshots found in region {region}")
                sys.stdout.flush()
        except KeyboardInterrupt:
            raise
        except Exception as e:
            sys.stderr.write("\r\033[K")  # \033[K clears from cursor to end of line
            sys.stderr.write(f"{Fore.LIGHTBLACK_EX} | Failed to list public EBS snapshots in region {region}")
            sys.stderr.flush()
            log_error(f"\n | Error:{e}")
    print("")