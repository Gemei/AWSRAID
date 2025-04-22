import json
from colorama import Fore
from modules.utils import custom_serializer


def sqs_init_enum(victim_sqs_client, attacker_sqs_client):
    list_sqs_queues(victim_sqs_client)

def list_sqs_queues(sqs_client):
    print(f"{Fore.GREEN}Enumerating SQS Queues...")
    try:
        queues = sqs_client.list_queues().get("QueueUrls", [])
        for queue_url in queues:
            print(f"{Fore.MAGENTA}Queue URL: {queue_url}")
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
                print(f"{Fore.MAGENTA}Messages: {json.dumps(messages, indent=4, sort_keys=True, default=custom_serializer)}")
            except:
                print(f"{Fore.LIGHTBLACK_EX}Failed to receive SQS messages")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list SQS queues")
