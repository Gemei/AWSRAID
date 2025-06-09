from colorama import Fore
import json, sys
from modules.utils import custom_serializer
import modules.globals as my_globals

def elastic_beanstalk_init_enum(victim_session, attacker_session):
    list_elastic_beanstalk(victim_session)

def list_elastic_beanstalk(victim_session):
    print(f"{Fore.GREEN}Enumerating Elastic Beanstalk Applications...")
    for region in my_globals.aws_regions:
        try:
            eb_client = victim_session.client("elasticbeanstalk", region_name=region)
            apps = eb_client.describe_applications().get("Applications", [])
            if not apps:
                continue
            for app in apps:
                print(f"{Fore.MAGENTA}\nRegion: {region} | Application: {app['ApplicationName']}")
                try:
                    envs = eb_client.describe_environments(ApplicationName=app['ApplicationName']).get("Environments", [])
                    print(f"{Fore.YELLOW}Environments:\n{json.dumps(envs, indent=4, sort_keys=True, default=custom_serializer)}")
                except:
                    print(f"{Fore.LIGHTBLACK_EX}Failed to describe environments for application {app['ApplicationName']}")
        except:
            sys.stdout.write("\r\033[K")
            sys.stdout.write(f"{Fore.LIGHTBLACK_EX}Failed to list Elastic Beanstalk applications in region {region}")
            sys.stdout.flush()
    print("")