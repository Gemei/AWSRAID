from colorama import Fore
import json
from modules.utils import custom_serializer
import modules.globals as my_globals
from botocore.config import Config
from modules.logger import *

def elastic_beanstalk_init_enum(victim_session, attacker_session):
    enable_print_logging()
    list_elastic_beanstalk(victim_session)

def list_elastic_beanstalk(victim_session):
    print(f"{Fore.GREEN}[+] Enumerating Elastic Beanstalk Applications:")
    config = Config(connect_timeout=5, read_timeout=10, retries={'max_attempts': 1})
    for region in my_globals.aws_regions:
        try:
            eb_client = victim_session.client("elasticbeanstalk", region_name=region, config=config)
            apps = eb_client.describe_applications().get("Applications", [])
            if not apps:
                sys.stdout.write("\r\033[K")
                sys.stdout.write(f"{Fore.LIGHTBLACK_EX}No applications found in region {region}")
                sys.stdout.flush()
                continue
            for app in apps:
                print(f"{Fore.MAGENTA} | Region: {region} | Application: {app['ApplicationName']}")
                try:
                    envs = eb_client.describe_environments(ApplicationName=app['ApplicationName']).get("Environments", [])
                    print(f"{Fore.YELLOW} | Environments:\n{json.dumps(envs, indent=4, sort_keys=True, default=custom_serializer)}")
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"{Fore.LIGHTBLACK_EX} | Failed to describe environments for application {app['ApplicationName']}")
                    log_error(f"Failed to describe environments for application {app['ApplicationName']}\n | Error:{e}")
        except KeyboardInterrupt:
            raise
        except Exception as e:
            sys.stderr.write("\r\033[K")
            sys.stderr.write(f"{Fore.LIGHTBLACK_EX} | Failed to list Elastic Beanstalk applications in region {region}")
            sys.stderr.flush()
            log_error(f"\n | Error:{e}")
    print("")