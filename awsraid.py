import sys
from colorama import Fore, init
from modules.config_loader import load_config
from modules.aws_clients import *
from modules.services.sts import sts_init_enum
from modules.services.iam import iam_init_enum
from modules.services.ec2 import ec2_init_enum
from modules.services.rds import rds_init_enum
from modules.services.cognito import cognito_init_enum
from modules.services.macie import macie_init_enum
from modules.services.ssm import ssm_init_enum
from modules.services.elastic_beanstalk import elastic_beanstalk_init_enum
from modules.services.secrets_manager import secrets_manager_init_enum
from modules.services.aws_lambda import lambda_init_enum
from modules.services.sqs import sqs_init_enum
from modules.services.s3 import s3_init_enum
from modules.services.code_commit import code_commit_init_enum
from modules.utils import validate_config, print_banner

init(autoreset=True)

SERVICE_MAP = {
    sts_init_enum: "sts",
    iam_init_enum: "iam",
    ec2_init_enum: "ec2",
    rds_init_enum: "rds",
    cognito_init_enum: "cognito-idp",
    macie_init_enum: "macie2",
    ssm_init_enum: "ssm",
    elastic_beanstalk_init_enum: "elasticbeanstalk",
    secrets_manager_init_enum: "secretsmanager",
    lambda_init_enum: "lambda",
    sqs_init_enum: "sqs",
    s3_init_enum: "s3",
    code_commit_init_enum: "codecommit",
}

config = load_config(my_globals.CONFIG_FILE)

def main():
    print_banner()
    print(f"{Fore.GREEN}Starting AWS Enumeration Script...")
    no_victim_credentials_data = validate_config(config)

    victim_session, victim_clients = initialize_aws_regionless_victim_clients(my_globals.victim_access_key, my_globals.victim_secret_access_key, my_globals.victim_session_token)
    attacker_session, attacker_clients = initialize_aws_regionless_attacker_clients(my_globals.attacker_access_key, my_globals.attacker_secret_access_key, my_globals.attacker_region)

    # For public access buckets
    initialize_aws_unsigned_s3_client()

    # These functions require a region to be set during client creation
    region_functions = [
        secrets_manager_init_enum,
        ec2_init_enum,
        lambda_init_enum,
        rds_init_enum,
        cognito_init_enum,
        macie_init_enum,
        ssm_init_enum,
        elastic_beanstalk_init_enum,
        sqs_init_enum,
        code_commit_init_enum,
    ]

    # These functions do not require a region to be set during client creation
    regionless_functions = [sts_init_enum, iam_init_enum, s3_init_enum]

    # These functions would run if the user has only provided a public s3 bucket or AWS account ID
    unauthenticated_functions = [iam_init_enum, s3_init_enum]

    if not no_victim_credentials_data:
        for function in regionless_functions:
            service = SERVICE_MAP[function]
            function(victim_clients.get(service), attacker_clients.get(service))

        for function in region_functions:
            function(victim_session, attacker_session)
    else:
        for function in unauthenticated_functions:
            function(None, attacker_session)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"{Fore.RED}\n\n[!] Caught Ctrl+C (KeyboardInterrupt)")
        print(f"{Fore.RED}Exiting...")
        sys.exit(0)