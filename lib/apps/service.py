class Service:
    def __init__(self, service_name, operation):
        self.service_name = service_name
        self.operation = operation

        self.services_list = ["scheduler", "Response_Worker", "statistic_mod", "geo2g", "geo3g", "geo4g", "bsc_mod", "rnc_mod", "mme_mod", "nok_mod"]

    def make_command(self):
        if(self.service_name in self.services_list):
            if(self.operation == "status"):
                command = f"systemctl status {self.service_name}"
            
            elif(self.operation == "start"):
                command = f"sudo systemctl start {self.service_name}"
            
            elif(self.operation == "stop"):
                command = f"sudo systemctl stop {self.service_name}"
            
            else:
                return "UnknownOperationError"
        else:
            return "UnknownServiceNameError"

        return command

