CONFIG_FILE = "enum_config.json"
user_name_wordlist = "wordlists/pacu_usernames_word_list.txt"
role_name_wordlist = "wordlists/pacu_role_names_word_list.txt"

start_username_brute_force = False
start_role_name_brute_force = False

victim_access_key = ""
victim_secret_access_key = ""
victim_session_token = ""
victim_buckets = ""
victim_aws_account_ID = ""
victim_aws_username = ""
victim_groups = ""
victim_roles = ""
victim_regions = []

attacker_access_key = ""
attacker_secret_access_key = ""
attacker_region = ""
attacker_IAM_role_name = ""
attacker_S3_role_arn = ""

unsigned_s3_client = ""

aws_regions = [
    "af-south-1",
    "ap-east-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-south-1",
    "ap-south-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-southeast-3",
    "ap-southeast-4",
    "ap-southeast-5",
    "ap-southeast-7",
    "ca-central-1",
    "ca-west-1",
    "eu-central-1",
    "eu-central-2",
    "eu-north-1",
    "eu-south-1",
    "eu-south-2",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "il-central-1",
    "me-central-1",
    "me-south-1",
    "mx-central-1",
    "sa-east-1",
    "us-east-1",
    "us-east-2",
    "us-gov-east-1",
    "us-gov-west-1",
    "us-west-1",
    "us-west-2",
]