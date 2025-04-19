import json
from colorama import Fore
from modules.utils import custom_serializer


def iam_init_enum(iam_client, sts_client):
    try:
        sts_info = sts_client.get_caller_identity()

        user_name = sts_info["Arn"].split("/")[-1]
        aws_id = sts_info["Account"]
        
        list_iam_policies(iam_client, aws_id)
        list_iam_roles(iam_client, aws_id)
        list_current_user_policies(iam_client, user_name)
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to call sts to get current user and AWS account ID.")


def list_iam_policies(iam_client, aws_id):
    print(f"{Fore.GREEN}Listing IAM Policies...")
    try:
        policies = iam_client.list_policies(Scope='All').get("Policies", [])
        for policy in policies:
            if(aws_id in policy['Arn']): # Only print customer managed policies
                print(f"{Fore.CYAN}Policy: {policy['PolicyName']} | ARN: {policy['Arn']}")
                describe_iam_policy(iam_client, policy['Arn'])
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list IAM policies")

def list_iam_roles(iam_client, aws_id):
    print(f"{Fore.GREEN}Enumerating IAM Roles...")
    try:
        roles = iam_client.list_roles().get("Roles", [])
        for role in roles:
            if (aws_id in role['Arn']):  # Only print customer managed roles
                print(f"{Fore.CYAN}Role: {role['RoleName']} | ARN: {role['Arn']}")
                describe_iam_role(iam_client, role['RoleName'])
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list IAM roles")

def list_current_user_policies(iam_client, user_name):
    print(f"{Fore.GREEN}Enumerating Current User Policies...")
    try:
        inline_policies = iam_client.list_user_policies(UserName=user_name).get("PolicyNames", [])
        if inline_policies:
            print(f"{Fore.MAGENTA}Inline Policies:")
            for policy_name in inline_policies:
                policy_doc = iam_client.get_user_policy(UserName=user_name, PolicyName=policy_name)
                print(f"{Fore.MAGENTA}- {policy_name}: {json.dumps(policy_doc['PolicyDocument'], indent=2)}")
        else:
            print(f"{Fore.LIGHTBLACK_EX}No inline policies found.")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to enumerate user inline policies")

    try:
        attached_policies = iam_client.list_attached_user_policies(UserName=user_name).get("AttachedPolicies", [])
        if attached_policies:
            print(f"{Fore.MAGENTA}Attached Policies:")
            for policy in attached_policies:
                print(f"{Fore.MAGENTA}- {policy['PolicyName']} (ARN: {policy['PolicyArn']})")
                describe_iam_policy(iam_client, policy['PolicyArn'])
        else:
            print(f"{Fore.LIGHTBLACK_EX}No attached policies found.")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to enumerate user attached policies")

def describe_iam_policy(iam_client, policy_arn):
    try:
        version_id = iam_client.get_policy(PolicyArn=policy_arn)["Policy"]["DefaultVersionId"]
        policy_doc = iam_client.get_policy_version(PolicyArn=policy_arn, VersionId=version_id)["PolicyVersion"]["Document"]
        print(f"{Fore.YELLOW}{json.dumps(policy_doc, indent=4, sort_keys=True, default=custom_serializer)}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to describe policy {policy_arn}")

def describe_iam_role(iam_client, role_name):
    try:
        role_detail = iam_client.get_role(RoleName=role_name)["Role"]
        print(f"{Fore.YELLOW}{json.dumps(role_detail['AssumeRolePolicyDocument'], indent=4, sort_keys=True, default=custom_serializer)}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to describe role {role_name}")