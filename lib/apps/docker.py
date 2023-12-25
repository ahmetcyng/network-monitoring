from lib.apps.connectServer import Connection

class Docker:
    def __init__(self) -> None:
        self.connection = Connection
        self.connection.create_session()

    def ps(self):
        command = "sudo docker ps"
        stdout, stderr = self.connection.run_command(command=command)
        command_output = stdout
        error_message = stderr

    def image(self):
        command = "docker image ls"
        stdout, stderr = self.connection.run_command(command=command)
        command_output = stdout
        error_message = stderr

    def container(self):
        command = "docker container ls"
        stdout, stderr = self.connection.run_command(command=command)
        command_output = stdout
        error_message = stderr

