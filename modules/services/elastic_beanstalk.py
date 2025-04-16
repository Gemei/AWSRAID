from colorama import Fore, Style

def enumerate_elastic_beanstalk(elasticbeanstalk_client):
    print(f"{Fore.GREEN}Enumerating Elastic Beanstalk Applications...{Style.RESET_ALL}")
    try:
        apps = elasticbeanstalk_client.describe_applications().get("Applications", [])
        if not apps:
            raise Exception()
        for app in apps:
            print(f"{Fore.MAGENTA}Application: {app['ApplicationName']}{Style.RESET_ALL}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list Elastic Beanstalk applications{Style.RESET_ALL}")
