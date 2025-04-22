import sys
from colorama import Fore, init
from modules.config_loader import load_config
from modules.aws_clients import *
from modules.services.sts import sts_init_enum
from modules.services.iam import iam_init_enum
from modules.services.ec2 import ec2_init_enum
from modules.services.ebs import ebs_init_enum
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
from modules.utils import validate_config

init(autoreset=True)

config = load_config(my_globals.CONFIG_FILE)

def main():
    print(f"{Fore.GREEN}Starting AWS Enumeration Script...")
    validate_config(config)

    victim_session, victim_clients = initialize_aws_victim_clients(my_globals.victim_access_key, my_globals.victim_secret_access_key, my_globals.victim_session_token, my_globals.victim_region)
    attacker_session, attacker_clients = initialize_aws_attacker_clients(my_globals.attacker_access_key, my_globals.attacker_secret_access_key, my_globals.attacker_region)
    initialize_aws_unsigned_s3_client()

    functions = [
        sts_init_enum,
        iam_init_enum,
        ec2_init_enum,
        ebs_init_enum,
        rds_init_enum,
        cognito_init_enum,
        macie_init_enum,
        ssm_init_enum,
        elastic_beanstalk_init_enum,
        secrets_manager_init_enum,
        lambda_init_enum,
        sqs_init_enum,
        s3_init_enum,
        code_commit_init_enum,
    ]

    for function in functions:
        client_name = function.__name__.replace("_init_enum", "_client")

        victim_client = victim_clients.get(client_name) if victim_clients else None
        attacker_client = attacker_clients.get(client_name) if attacker_clients else None

        if function is ebs_init_enum:
            ebs_init_enum(
                victim_clients.get("ec2_client") if victim_clients else None,
                victim_clients.get("sts_client") if victim_clients else None,
                attacker_clients.get("ec2_client") if attacker_clients else None,
            )
        elif function is s3_init_enum:
            s3_init_enum(
                victim_clients.get("s3_client") if victim_clients else None,
                attacker_session if attacker_clients else None,
            )
        else:
            function(victim_client, attacker_client)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCtrl+C pressed. Exiting.")
        sys.exit(0)