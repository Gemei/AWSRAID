import sys

from colorama import init, Fore, Style
from modules.config_loader import load_config
from modules.aws_clients import initialize_aws_clients
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

init(autoreset=True)

CONFIG_FILE = "enum_config.json"
config = load_config(CONFIG_FILE)

access_key = config.get("access_key")
secret_access_key = config.get("secret_access_key")
session_token = config.get("session_token") or None
region = config.get("region", "us-east-1")
buckets = config.get("buckets") or None

session, clients = initialize_aws_clients(access_key, secret_access_key, session_token, region)
globals().update(clients)

def main():
    print(f"{Fore.GREEN}Starting AWS Enumeration Script...{Style.RESET_ALL}")
    sts_init_enum(clients["sts_client"])
    iam_init_enum(clients["iam_client"], clients["sts_client"])
    ec2_init_enum(clients["ec2_client"])
    ebs_init_enum(clients["ec2_client"], clients["sts_client"])
    rds_init_enum(clients["rds_client"])
    cognito_init_enum(clients["cognito_client"])
    macie_init_enum(clients["macie_client"])
    ssm_init_enum(clients["ssm_client"])
    eb_init_enum(clients["elasticbeanstalk_client"])
    secrets_manager_init_enum(clients["secrets_client"])
    #lambda_init_enum(clients["lambda_client"])
    sqs_init_enum(clients["sqs_client"])
    s3_init_enum(clients["s3_client"], clients["unsigned_s3_client"], buckets)
    code_commit_init_enum(clients["codecommit_client"])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCtrl+C pressed. Exiting.")
        sys.exit(0)