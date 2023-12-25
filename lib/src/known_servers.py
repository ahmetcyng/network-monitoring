from lib import json

class KnownServers:
    def __init__(self):
        with open("json/known_servers.json", "r") as json_file:
            self.knwon_server_detail = json.load(json_file)
    
    def server_detail(self):
        known_ip_list = list(self.knwon_server_detail.keys())
        knwon_server_status_detail = []
        for i in known_ip_list:
            knwon_server_status_detail.append(self.knwon_server_detail[i]["status"])
        
        return [known_ip_list, knwon_server_status_detail]

    def connected_server_detail(self, ip):
        os = self.knwon_server_detail[ip]["os"]
        disk_usage = self.knwon_server_detail[ip]["disk_usage"]
        memory = self.knwon_server_detail[ip]["memory"]

        return [ip, os, disk_usage, memory]