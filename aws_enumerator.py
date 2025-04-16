from colorama import init, Fore, Style
from modules.config_loader import load_config
from modules.aws_clients import initialize_aws_clients
from modules.services.sts import whoami
from modules.services.iam import enumerate_iam_roles, enumerate_current_user_policies
from modules.services.ec2 import enumerate_ec2
from modules.services.ebs import enumerate_ebs_volumes, enumerate_ebs_snapshots
from modules.services.rds import enumerate_rds_instances
from modules.services.cognito import enumerate_cognito_users
from modules.services.macie import enumerate_macie_findings
from modules.services.ssm import enumerate_ssm_parameters
from modules.services.elastic_beanstalk import enumerate_elastic_beanstalk
from modules.services.secrets_manager import enumerate_secrets_manager
from modules.services.aws_lambda import enumerate_lambda
from modules.services.sqs import enumerate_sqs
from modules.services.s3 import download_bucket, enumerate_public_buckets, bucket_policy

init(autoreset=True)

CONFIG_FILE = "enum_config.json"
config = load_config(CONFIG_FILE)

access_key = config.get("access_key")
secret_access_key = config.get("secret_access_key")
session_token = config.get("session_token") or None
region = config.get("region", "us-east-1")
buckets = config.get("buckets", []) or None

session, clients = initialize_aws_clients(access_key, secret_access_key, session_token, region)
globals().update(clients)

def main():
    print(f"{Fore.GREEN}Starting AWS Enumeration Script...{Style.RESET_ALL}")
    whoami(clients["sts_client"])
    enumerate_iam_roles(clients["iam_client"])
    enumerate_current_user_policies(clients["sts_client"], clients["iam_client"])
    enumerate_ec2(clients["ec2_client"])
    enumerate_ebs_volumes(clients["ec2_client"])
    enumerate_ebs_snapshots(clients["ec2_client"], clients["sts_client"])
    enumerate_rds_instances(clients["rds_client"])
    enumerate_cognito_users(clients["cognito_client"])
    enumerate_macie_findings(clients["macie_client"])
    enumerate_ssm_parameters(clients["ssm_client"])
    enumerate_elastic_beanstalk(clients["elasticbeanstalk_client"])
    enumerate_secrets_manager(clients["secrets_client"])
    enumerate_lambda(clients["lambda_client"])
    enumerate_sqs(clients["sqs_client"])
    download_bucket(clients["s3_client"], buckets)
    enumerate_public_buckets(clients["unsigned_s3_client"], buckets)
    bucket_policy(clients["s3_client"], buckets)

if __name__ == "__main__":
    main()