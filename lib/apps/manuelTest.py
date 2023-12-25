from lib.Flask.src.flask import json

class ManuelTest:
    def __init__(self, service_name, operation):
        self.service_name = service_name
        self.operation = operation
        self.python_path = "/usr/bin/python3"

        with open("./json/module_path.json", "r") as path_json_file:
            path_json = json.load(path_json_file)
        
        self.module_path = path_json[self.service_name]

    def make_command(self):
        if(self.operation == "start"):
            command = f"nohup {self.python_path} {self.module_path}{self.service_name}.py &"

        elif(self.operation == "stop"):
            command = f"ps | grep {self.service_name}".split()
        
        else:
            print("Error")

        return command
            
    