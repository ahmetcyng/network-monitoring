from lib.apps.connectServer import Connection

class TraceDump:
    def __init__(self, interface, port, path, operation):
        self.interface = interface
        self.port = port
        self.path = path
        self.operation = operation
        
    def make_command(self):
        
        if(self.operation == "start"):
            command = f"sudo tcpdump -i {self.interface} -nn -s0 -v port {self.port} -w {self.path}"
            return command
            
        elif(self.operation == "stop"):
            pass

        else:
            print("Error")

        