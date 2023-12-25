from lib import json
from lib.src import server_check

class ServerConnection:
    def __init__(self, ip, port, username, password, root_password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.root_password = root_password

    def connect(self):
        server_status = server_check.ServerStatusCheck(ip=self.ip)
        is_server_up = server_status.is_server_up()
        is_server_known = server_status.is_server_known()

        if(is_server_known):
            if(is_server_up):
                with open("json/known_servers.json", "r") as json_file:
                    server_json = json.load(json_file)
                
                os_name = server_json[self.ip]["os"]
                services = list(server_json[self.ip]["services"].keys())
                service_status_dict = {}
                for service in services:
                    service_status_dict[service] = server_json[self.ip]["services"][service]["status"]

                with open("json/connected_server.json", "w") as json_file:
                    server_json = {}
                    server_json["ip"] = self.ip
                    server_json["ssh_port"] = self.port
                    server_json["username"] = self.username
                    server_json["password"] = self.password
                    server_json["root_password"] = self.root_password

                    json.dump(server_json, json_file, indent=4, sort_keys=True)

                return [services, [self.ip, os_name], service_status_dict]
            else:
                print("server ayakta degil")
        else:
            print("server bilinmiyor")
