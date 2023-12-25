from lib.paramiko import paramiko
from lib import json
from lib.src import server_check

class ServerConfiguration:
    def __init__(self, ip, port, username, password, root_password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.root_passowrd = root_password

    def get_server_info(self):       
        client_session = paramiko.SSHClient()
        client_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client_session.connect(self.ip, self.port, self.username, self.password)

        if(client_session != "SshError"):
            output_range = 0
            service_command = "sudo netstat -t6nlp | grep tcp6"
            stdin, stdout, stderr = client_session.exec_command(command=service_command, get_pty=True)

            stdin.write(f"{self.root_passowrd}\n")
            stdin.flush()
            output_range = 2

            command_output = stdout.readlines()
            services_dict = {}

            for i in command_output[output_range:]:
                service_raw_data = i.split()
                port = ''.join(ch for ch in service_raw_data[3] if ch.isalnum())
                service_name = service_raw_data[6].split("/")[1]
                service_name = ''.join(ch for ch in service_name if ch.isalnum())
                services_dict[service_name] = {
                    "port": port,
                    "status": "up"
                }
        
            commands_list = ["cat /etc/*release | grep PRETTY_NAME", "free -m | grep Mem", "df / | grep /"]
            commands_output_list = []

            for command in commands_list:
                stdin, stdout, stderr = client_session.exec_command(command=command)
                command_output = stdout.readlines()
                output = ' '.join(command_output).replace("\n", "")
                commands_output_list.append(output)

                stdin.close()

            os_name = commands_output_list[0].split("=")[1]
            memory = commands_output_list[1].split()[1]
            disk_usage = commands_output_list[2].split()[-2]

            return os_name, memory, disk_usage, services_dict

    def configure(self):
        server_status = server_check.ServerStatusCheck(ip=self.ip)
        is_server_up = server_status.is_server_up()
        is_server_known = server_status.is_server_known()

        os_name, memory, disk_usage, service_dict = self.get_server_info()

        if(is_server_up):
            if(not is_server_known):
                with open("json/known_servers.json", "r+") as json_file:
                    server_json = json.load(json_file)
                    server_json[self.ip] = {
                        "os": os_name,
                        "status": "up",
                        "memory": memory,
                        "disk_usage": disk_usage,
                        "services": service_dict
                    }
                    json_file.seek(0)
                    json.dump(server_json, json_file, indent=4, sort_keys=True)
                    json_file.truncate()
            else:
                print("Server biliniyor")
        else:
            print("Server ayakta degil")
