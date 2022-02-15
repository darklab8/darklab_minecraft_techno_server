import os
import argparse

my_parser = argparse.ArgumentParser(description='')
my_parser.add_argument('--dockerconfigjson',
                       type=str,
                       help='dockerconfigjson') 
args = my_parser.parse_args()

def shell(cmd):
    print(cmd)
    status_code = os.system(cmd)

    if status_code != 0:
        exit(status_code)


shell(f'helm upgrade --install --create-namespace --namespace minecraft-techno-prod minecraft-server . --set dockerconfigjson={args.dockerconfigjson}')
