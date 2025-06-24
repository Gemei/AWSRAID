from colorama import Fore
import json
from modules.utils import custom_serializer
import modules.globals as my_globals
from botocore.config import Config
from modules.logger import *

def code_commit_init_enum(victim_session, attacker_session):
    enable_print_logging()
    list_code_commit_repos(victim_session)

def list_code_commit_repos(victim_session):
    print(f"{Fore.GREEN}Enumerating CodeCommit Repositories...")
    config = Config(connect_timeout=5, read_timeout=10, retries={'max_attempts': 1})
    for region in my_globals.aws_regions:
        try:
            code_commit_client = victim_session.client("codecommit", region_name=region, config=config)
            repos = code_commit_client.list_repositories().get("repositories", [])
            for repo in repos:
                print(f"{Fore.MAGENTA}Region: {region} | Repository: {repo['repositoryName']} | ID: {repo['repositoryId']}")
                try:
                    repo_details = code_commit_client.get_repository(repositoryName=repo['repositoryName']).get("repositoryMetadata", {})
                    print(f"{Fore.YELLOW}{json.dumps(repo_details, indent=4, sort_keys=True, default=custom_serializer)}")
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"{Fore.LIGHTBLACK_EX}Failed to get repository metadata for {repo['repositoryName']}")
                    log_error(f"Failed to get repository metadata for {repo['repositoryName']}\n | Error:{e}")
                try:
                    branches = code_commit_client.list_branches(repositoryName=repo['repositoryName']).get("branches", [])
                    print(f"{Fore.YELLOW}{repo['repositoryName']} branches:\n{json.dumps(branches, indent=4, sort_keys=True, default=custom_serializer)}")
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"{Fore.LIGHTBLACK_EX}Failed to list branches for {repo['repositoryName']}")
                    log_error(f"Failed to list branches for {repo['repositoryName']}\n | Error:{e}")
        except KeyboardInterrupt:
            raise
        except Exception as e:
            sys.stdout.write("\r\033[K")
            sys.stdout.write(f"{Fore.LIGHTBLACK_EX}Failed to list CodeCommit repositories in region {region}")
            sys.stdout.flush()
            log_error(f"Failed to list CodeCommit repositories in region {region}\n | Error:{e}")
    print("")