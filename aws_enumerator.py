import sys

from colorama import Fore, init
from modules.config_loader import load_config
from modules.aws_clients import initialize_aws_victim_clients, initialize_aws_attacker_clients
from modules.services.sts import sts_init_enum
from modules.services.iam import iam_init_enum
from modules.services.ec2 import ec2_init_enum
from modules.services.ebs import ebs_init_enum
from modules.services.rds import rds_init_enum
from modules.services.cognito import cognito_init_enum
from modules.services.macie import macie_init_enum
from modules.services.ssm import ssm_init_enum
from modules.services.elastic_beanstalk import eb_init_enum
from modules.services.secrets_manager import secrets_manager_init_enum
from modules.services.aws_lambda import lambda_init_enum
from modules.services.sqs import sqs_init_enum
from modules.services.s3 import s3_init_enum
from modules.services.code_commit import code_commit_init_enum
from modules.utils import validate_config

init(autoreset=True)

CONFIG_FILE = "enum_config.json"
config = load_config(CONFIG_FILE)

victim_access_key = config.get("victim_access_key") or None
victim_secret_access_key = config.get("victim_secret_access_key") or None
victim_session_token = config.get("victim_session_token") or None
victim_region = config.get("victim_region", "us-east-1")
victim_buckets = config.get("victim_buckets") or None
victim_aws_account_ID = config.get("victim_aws_account_ID") or None

attacker_access_key = config.get("attacker_access_key") or None
attacker_secret_access_key = config.get("attacker_secret_access_key") or None
attacker_region = config.get("attacker_region", "us-east-1")
attacker_IAM_role = config.get("attacker_IAM_role_name") or None
attacker_S3_role = config.get("attacker_S3_role_arn") or None

def main():
    print(f"{Fore.GREEN}Starting AWS Enumeration Script...")
    validate_config(config)

    victim_session, victim_clients = initialize_aws_victim_clients(victim_access_key, victim_secret_access_key, victim_session_token, victim_region)
    attacker_session, attacker_clients = initialize_aws_attacker_clients(attacker_access_key, attacker_secret_access_key, attacker_region)

    sts_init_enum(victim_clients["sts_client"])
    iam_init_enum(victim_clients["iam_client"], victim_clients["sts_client"])
    ec2_init_enum(victim_clients["ec2_client"])
    ebs_init_enum(victim_clients["ec2_client"], victim_clients["sts_client"], attacker_clients["attacker_ec2_client"], victim_aws_account_ID)
    rds_init_enum(victim_clients["rds_client"])
    cognito_init_enum(victim_clients["cognito_client"])
    macie_init_enum(victim_clients["macie_client"])
    ssm_init_enum(victim_clients["ssm_client"])
    eb_init_enum(victim_clients["elasticbeanstalk_client"])
    secrets_manager_init_enum(victim_clients["secrets_client"])
    lambda_init_enum(victim_clients["lambda_client"])
    sqs_init_enum(victim_clients["sqs_client"])
    s3_init_enum(victim_clients["s3_client"], victim_clients["unsigned_s3_client"], victim_buckets)
    code_commit_init_enum(victim_clients["codecommit_client"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCtrl+C pressed. Exiting.")
        sys.exit(0)