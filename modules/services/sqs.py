import json
from colorama import Fore, Style
from modules.utils import custom_serializer

def enumerate_sqs(sqs_client):
    print(f"{Fore.GREEN}Enumerating SQS Queues...{Style.RESET_ALL}")
    try:
        queues = sqs_client.list_queues().get("QueueUrls", [])
        for queue_url in queues:
            print(f"{Fore.MAGENTA}Queue URL: {queue_url}{Style.RESET_ALL}")
            try:
                response = sqs_client.receive_message(
                    QueueUrl=queue_url,
                    AttributeNames=['All'],
                    MaxNumberOfMessages=10,
                    MessageAttributeNames=['All'],
                    VisibilityTimeout=30,
                    WaitTimeSeconds=10
                )
                messages = response.get('Messages', [])
                print(f"{Fore.MAGENTA}Messages: {json.dumps(messages, indent=4, sort_keys=True, default=custom_serializer)}{Style.RESET_ALL}")
            except:
                print(f"{Fore.LIGHTBLACK_EX}Failed to receive SQS messages{Style.RESET_ALL}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list SQS queues{Style.RESET_ALL}")
