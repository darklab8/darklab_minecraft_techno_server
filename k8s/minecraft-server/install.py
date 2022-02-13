import os
import argparse


def shell(cmd):
    print(cmd)
    status_code = os.system(cmd)

    if status_code != 0:
        exit(status_code)


shell(f'helm upgrade --install --create-namespace --namespace minecraft-techno-prod minecraft-server .')
