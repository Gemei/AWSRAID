from colorama import Fore, Style

def ec2_init_enum(ec2_client):
    enumerate_ec2(ec2_client)

def enumerate_ec2(ec2_client):
    print(f"{Fore.GREEN}Enumerating EC2 Instances...{Style.RESET_ALL}")
    try:
        reservations = ec2_client.describe_instances().get("Reservations", [])
        for reservation in reservations:
            for instance in reservation.get("Instances", []):
                print(f"{Fore.MAGENTA}Instance ID: {instance['InstanceId']} | State: {instance['State']['Name']}{Style.RESET_ALL}")
                describe_ec2_instance(instance)
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list EC2 instances{Style.RESET_ALL}")

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
        print(f"{Fore.YELLOW}  Private IP: {private_ip}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  Key Name: {key_name}{Style.RESET_ALL}")
        if tags:
            print(f"{Fore.YELLOW}  Tags:")
            for tag in tags:
                print(f"{Fore.YELLOW}    {tag['Key']}: {tag['Value']}{Style.RESET_ALL}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to describe EC2 instance{Style.RESET_ALL}")

