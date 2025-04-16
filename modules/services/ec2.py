from colorama import Fore, Style

def enumerate_ec2(ec2_client):
    print(f"{Fore.GREEN}Enumerating EC2 Instances...{Style.RESET_ALL}")
    try:
        reservations = ec2_client.describe_instances().get("Reservations", [])
        for reservation in reservations:
            for instance in reservation.get("Instances", []):
                print(f"{Fore.MAGENTA}Instance ID: {instance['InstanceId']} | State: {instance['State']['Name']}{Style.RESET_ALL}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list EC2 instances{Style.RESET_ALL}")
