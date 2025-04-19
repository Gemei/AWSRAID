import json,sys,os
import shutil
from colorama import Fore
from modules.utils import custom_serializer


def s3_init_enum(s3_client, s3_unsigned_client, buckets):
    found_buckets = list_buckets(s3_client)
    if found_buckets:
        buckets = list(buckets or []) # Prevent list type error
        buckets += found_buckets
    download_private_bucket(s3_client, buckets)
    list_public_buckets(s3_unsigned_client, buckets)
    download_public_bucket(s3_unsigned_client, buckets)
    get_bucket_policy(s3_client, buckets)

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
    if buckets:
        print(f"{Fore.GREEN}Checking public S3 buckets without signing...")
        for bucket in buckets:
            try:
                response = unsigned_s3_client.list_objects_v2(Bucket=bucket)
                if 'Contents' in response:
                    print(f"{Fore.MAGENTA}Public access detected on: {bucket}")
                    for obj in response['Contents'][:5]:
                        print(f"{Fore.MAGENTA}- {obj['Key']}")
                else:
                    print(f"{Fore.LIGHTBLACK_EX}No public content or access denied for: {bucket}")
            except:
                print(f"{Fore.LIGHTBLACK_EX}Failed to access bucket {bucket} anonymously")
    else:
        print(f"{Fore.LIGHTBLACK_EX}No buckets provided, skipping public buckets check")

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
            shutil.rmtree(bucket)
    except:
        pass

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
                sys.stdout.write(f"\r{Fore.MAGENTA}[{i}/{total_files}] Downloading {file_name}   ")
                sys.stdout.flush()
                try:
                    with open(file_name, "wb") as file:
                        s3_client.download_fileobj(bucket, file_name, file)
                except KeyboardInterrupt:
                    print("\nCtrl+C pressed. Exiting.")
                    sys.exit(0)
                except:
                    # Clear the progress line first
                    sys.stdout.write(" " * shutil.get_terminal_size((80, 20)).columns + "\r")
                    print(f"{Fore.LIGHTBLACK_EX}Failed to download {file_name} from {bucket}")
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
