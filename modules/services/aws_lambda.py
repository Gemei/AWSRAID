from colorama import Fore
import json
from modules.utils import custom_serializer


def lambda_init_enum(lambda_client):
    list_lambda_functions(lambda_client)

def list_lambda_functions(lambda_client):
    print(f"{Fore.GREEN}Enumerating Lambda Functions...")
    try:
        functions = lambda_client.list_functions().get("Functions", [])
        for function in functions:
            print(f"{Fore.MAGENTA}Function: {function['FunctionName']} | Runtime: {function['Runtime']}")
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
                print(f"{Fore.MAGENTA}Function: {function['FunctionName']} | \nResponse:\n {json.dumps(response_payload, indent=4, sort_keys=True, default=custom_serializer)}")
            except:
                print(f"{Fore.LIGHTBLACK_EX}Failed to invoke Lambda functions")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list Lambda functions")
