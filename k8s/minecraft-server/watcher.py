import redis
import os
import subprocess
import hashlib
import requests
import re
from datetime import datetime
import time
datetime.utcnow()

REDIS_PASS = os.environ["REDIS_PASS"]
REDIS_HOST = "redis-watcher"
WATCHER_WEBHOOK = os.environ["WATCHER_WEBHOOK"]

redis_conn = redis.Redis(host=REDIS_HOST, password=REDIS_PASS, port=6379, db=0)

def current_time():
    return '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.utcnow()) + ": "

def hash_string(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

def emit_event(hashing: str, printing: str):
    was_seen = redis_conn.get(hash_string(hashing)) != None

    if was_seen:
        print("it was seen before")
        return

    print("was not seen")
    redis_conn.set(hash_string(hashing), printing)
    content = {"content": printing}
    requests.post(WATCHER_WEBHOOK, data=content)

def get_strings():
    result = subprocess.run(
        f"kubectl logs --namespace=minecraft-techno-prod --tail=20 deploy/minecraft-techno-deploy",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
    )
    text = result.stdout
    strings = text.decode("utf-8").split('\n')
    return strings

def check_logs():
    strings = get_strings()
    for string in strings:

        result = re.search("\[([0-9][0-9]:[0-9][0-9]:[0-9][0-9]) INFO\]: ([a-zA-Z]+) left the game", string)
        if result is not None:
            match = result.string
            time = result.group(1)
            playername = result.group(2)
            emit_event(hashing=match, printing=f"[{time}]: **{playername}** left the game")

        result = re.search("\[([0-9][0-9]:[0-9][0-9]:[0-9][0-9]) INFO\]: Player GCEntityPlayerMP\['([a-zA-Z0-9]+)'.+connected. Sending ping", string)
        if result is not None:
            match = result.string
            time = result.group(1)
            playername = result.group(2)
            emit_event(hashing=match, printing=f"[{time}]: **{playername}** entered the game")

        result = re.search('\[([0-9][0-9]:[0-9][0-9]:[0-9][0-9]) INFO\]: <([a-zA-Z0-9]+)> ([.^(a-zA-Z0-9? )]+)', string)
        if result is not None:
            match=result.string
            time=  result.group(1)
            playername = result.group(2)
            text = result.group(3)
            emit_event(hashing=match, printing=f"[{time}] **{playername}** says: {text}")

if __name__=="__main__":
    while True:
        try:
            check_logs()
        except Exception as er:
            print("something went terribly wrong")
            print(er)
        time.sleep(5)
