import json
from colorama import Fore, Style

from modules.utils import custom_serializer


def iam_init_enum(iam_client, sts_client):
    list_iam_policies(iam_client)
    list_iam_roles(iam_client)
    list_current_user_policies(iam_client, sts_client)

def list_iam_policies(iam_client):
    print(f"{Fore.GREEN}Listing IAM Policies...{Style.RESET_ALL}")
    try:
        policies = iam_client.list_policies(Scope='All').get("Policies", [])
        for policy in policies:
            print(f"{Fore.CYAN}Policy: {policy['PolicyName']} | ARN: {policy['Arn']}{Style.RESET_ALL}")
            describe_iam_policy(iam_client, policy['Arn'])
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list IAM policies{Style.RESET_ALL}")

def list_iam_roles(iam_client):
    print(f"{Fore.GREEN}Enumerating IAM Roles...{Style.RESET_ALL}")
    try:
        roles = iam_client.list_roles().get("Roles", [])
        for role in roles:
            print(f"{Fore.CYAN}Role: {role['RoleName']} | ARN: {role['Arn']}{Style.RESET_ALL}")
            describe_iam_role(iam_client, role['RoleName'])
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list IAM roles{Style.RESET_ALL}")

def list_current_user_policies(iam_client, sts_client):
    print(f"{Fore.GREEN}Enumerating Current User Policies...{Style.RESET_ALL}")
    try:
        user_arn = sts_client.get_caller_identity()["Arn"]
        user_name = user_arn.split("/")[-1]
        print(f"{Fore.CYAN}User: {user_name}{Style.RESET_ALL}")
    except:
        print(f"{Fore.LIGHTRED_EX}Failed to call sts to get current user{Style.RESET_ALL}")
        return

    try:
        inline_policies = iam_client.list_user_policies(UserName=user_name).get("PolicyNames", [])
        if inline_policies:
            print(f"{Fore.MAGENTA}Inline Policies:{Style.RESET_ALL}")
            for policy_name in inline_policies:
                policy_doc = iam_client.get_user_policy(UserName=user_name, PolicyName=policy_name)
                print(f"{Fore.MAGENTA}- {policy_name}: {json.dumps(policy_doc['PolicyDocument'], indent=2)}{Style.RESET_ALL}")
        else:
            print(f"{Fore.LIGHTBLACK_EX}No inline policies found.{Style.RESET_ALL}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to enumerate user inline policies{Style.RESET_ALL}")

    try:
        attached_policies = iam_client.list_attached_user_policies(UserName=user_name).get("AttachedPolicies", [])
        if attached_policies:
            print(f"{Fore.MAGENTA}Attached Policies:{Style.RESET_ALL}")
            for policy in attached_policies:
                print(f"{Fore.MAGENTA}- {policy['PolicyName']} (ARN: {policy['PolicyArn']}){Style.RESET_ALL}")
                describe_iam_policy(iam_client, policy['PolicyArn'])
        else:
            print(f"{Fore.LIGHTBLACK_EX}No attached policies found.{Style.RESET_ALL}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to enumerate user attached policies{Style.RESET_ALL}")

def describe_iam_policy(iam_client, policy_arn):
    try:
        version_id = iam_client.get_policy(PolicyArn=policy_arn)["Policy"]["DefaultVersionId"]
        policy_doc = iam_client.get_policy_version(PolicyArn=policy_arn, VersionId=version_id)["PolicyVersion"]["Document"]
        print(f"{Fore.YELLOW}{json.dumps(policy_doc, indent=4, sort_keys=True, default=custom_serializer)}{Style.RESET_ALL}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to describe policy {policy_arn}{Style.RESET_ALL}")

def describe_iam_role(iam_client, role_name):
    try:
        role_detail = iam_client.get_role(RoleName=role_name)["Role"]
        print(f"{Fore.YELLOW}{json.dumps(role_detail['AssumeRolePolicyDocument'], indent=4, sort_keys=True, default=custom_serializer)}{Style.RESET_ALL}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to describe role {role_name}{Style.RESET_ALL}")