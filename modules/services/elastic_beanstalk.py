from colorama import Fore


def eb_init_enum(elasticbeanstalk_client):
    list_elastic_beanstalk(elasticbeanstalk_client)

def list_elastic_beanstalk(elasticbeanstalk_client):
    print(f"{Fore.GREEN}Enumerating Elastic Beanstalk Applications...")
    try:
        apps = elasticbeanstalk_client.describe_applications().get("Applications", [])
        if not apps:
            raise Exception()
        for app in apps:
            print(f"{Fore.MAGENTA}Application: {app['ApplicationName']}")
    except:
        print(f"{Fore.LIGHTBLACK_EX}Failed to list Elastic Beanstalk applications")
