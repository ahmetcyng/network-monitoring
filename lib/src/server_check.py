from lib import json
from lib.os import os

class ServerStatusCheck:
    def __init__(self, ip):
        self.ip = ip

    def is_server_up(self):
        ping_response = os.system(f"ping -c 1 {self.ip}")
        if int(ping_response) == 0:
            return True
        else:
            return False

    def is_server_known(self):
        with open("json/known_servers.json", "r") as known_servers_file:
            known_servers = json.load(known_servers_file)

        known_ip_list = list(known_servers.keys())
        if(self.ip in known_ip_list):
            return True
        else:
            return False