import json,sys,os
from colorama import Fore, Style
from modules.utils import custom_serializer, create_bucket_dirs, delete_bucket_dirs

def s3_init_enum(s3_client, s3_unsigned_client, buckets):
    list_buckets(s3_client)
    download_private_bucket(s3_client, buckets)
    list_public_buckets(s3_unsigned_client, buckets)
    download_public_bucket(s3_unsigned_client, buckets)
    get_bucket_policy(s3_client, buckets)

def list_buckets(s3_client):
    try:
        print(f"{Fore.GREEN}Listing S3 Buckets...{Style.RESET_ALL}")
        buckets = s3_client.list_buckets().get("Buckets", [])
        for bucket in buckets:
            print(f"{Fore.MAGENTA}Found bucket: {bucket['Name']}{Style.RESET_ALL}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list S3 buckets{Style.RESET_ALL}")

def download_private_bucket(s3_client, buckets):
    download_bucket_objects(s3_client, buckets)

def download_public_bucket(s3_unsigned_client, buckets):
    download_bucket_objects(s3_unsigned_client, buckets)

def list_public_buckets(unsigned_s3_client, buckets):
    if buckets:
        print(f"{Fore.GREEN}Checking public S3 buckets without signing...{Style.RESET_ALL}")
        for bucket in buckets:
            try:
                response = unsigned_s3_client.list_objects_v2(Bucket=bucket)
                if 'Contents' in response:
                    print(f"{Fore.MAGENTA}Public access detected on: {bucket}{Style.RESET_ALL}")
                    for obj in response['Contents'][:5]:
                        print(f"{Fore.MAGENTA}- {obj['Key']}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.LIGHTBLACK_EX}No public content or access denied for: {bucket}{Style.RESET_ALL}")
            except:
                print(f"{Fore.LIGHTBLACK_EX}Failed to access bucket {bucket} anonymously{Style.RESET_ALL}")
    else:
        print(f"{Fore.LIGHTBLACK_EX}No buckets provided, skipping public buckets check")

def get_bucket_policy(s3_client, buckets):
    if buckets:
        for bucket in buckets:
            try:
                print(f"{Fore.CYAN}Getting policy for bucket: {bucket}{Style.RESET_ALL}")
                response = s3_client.get_bucket_policy(Bucket=bucket)
                policy = json.loads(response['Policy'])
                print(f"{Fore.MAGENTA}{json.dumps(policy, indent=4, sort_keys=True, default=custom_serializer)}{Style.RESET_ALL}")
            except:
                print(f"{Fore.LIGHTBLACK_EX}Can't get bucket policy: {bucket}{Style.RESET_ALL}")
    else:
        print(f"{Fore.LIGHTBLACK_EX}No buckets provided, skipping bucket policy check")

def download_bucket_objects(s3_client, buckets):
    if not buckets:
        print(f"{Fore.LIGHTBLACK_EX}No buckets provided, skipping download bucket objects{Style.RESET_ALL}")
        return

    for bucket in buckets:
        try:
            print(f"{Fore.CYAN}Processing bucket: {bucket}{Style.RESET_ALL}")
            create_bucket_dirs(bucket)
            os.chdir(bucket)
            bucket_objects = s3_client.list_objects_v2(Bucket=bucket)
            contents = bucket_objects.get("Contents", [])
            if not contents:
                print(f"{Fore.LIGHTBLACK_EX}No objects found in bucket: {bucket}{Style.RESET_ALL}")
                os.chdir("..")
                continue
            total_files = len(contents)
            for i, bucket_contents in enumerate(contents, start=1):
                file_name = str(bucket_contents["Key"])
                sys.stdout.write(f"\r{Fore.MAGENTA}[{i}/{total_files}] Downloading {file_name}{Style.RESET_ALL}   ")
                sys.stdout.flush()
                try:
                    with open(file_name, "wb") as file:
                        s3_client.download_fileobj(bucket, file_name, file)
                except:
                    print(f"\n{Fore.LIGHTBLACK_EX}Failed to download {file_name} from {bucket}{Style.RESET_ALL}")
            print()
            os.chdir("..")
        except:
            print(f"{Fore.LIGHTBLACK_EX}Can't list bucket: {bucket}{Style.RESET_ALL}")
            os.chdir("..")
            delete_bucket_dirs(bucket)