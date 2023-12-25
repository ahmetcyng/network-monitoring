from lib import json
from lib.paramiko import paramiko

class Connection:
    def __init__(self):
        with open("json/connected_server.json", "r") as connected_server_file:
            connected_server_json = json.load(connected_server_file)
        
        self.ip = connected_server_json["ip"]
        self.ssh_port = connected_server_json["ssh_port"]
        self.username = connected_server_json["username"]
        self.password = connected_server_json["password"]
        self.root_password = connected_server_json["root_password"]

    def create_session(self):
        try:
            self.client_session = paramiko.SSHClient()
            self.client_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client_session.connect(self.ip, self.ssh_port, self.username, self.password)

            self.client_session

        except:
            return "SshConnectionError"

    def close_session(self):
        self.client_session.close()

    def run_command(self, command):
        self.create_session()
        stdin, stdout, stderr  = self.client_session.exec_command(command=command, get_pty=True)
        stdin.write(f"{self.root_password}\n")
        stdin.flush()

        error = stderr.readlines()
        output = stdout.readlines()

        return output, error
