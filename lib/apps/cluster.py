class Cluster:
    def __init__(self, service_name, operation):
        self.service_name = service_name
        self.operation = operation

        self.services_list = ["pcsd", "pacemaker", "corosync"]
        self.pcs_services_list = ["scheduler", "response", "statistic", "geo2G", "geo3G", "geo4G", "BSCMOD", "RNCMOD", "MMEMOD", "NOKMOD"]
    

    def make_command(self):
        if(self.service_name == "pcs"):
            if(self.operation == "status"):
                command = "sudo pcs status"  
            
            elif(self.operation == "start"):
                command = "sudo pcs cluster start"
            
            elif(self.operation == "standby" or self.operation == "unstandby"):
                command = f"pcs cluster {self.operation}"

            else:
                return "Error"
        
        elif(self.service_name in self.services_list):
            if(self.operation == "status"):
                command = f"systemctl status {self.service_name}"

            elif(self.operation == "start"):
                command = f"sudo systemctl start {self.service_name}"

            elif(self.operation == "stop"):
                command = f"sudo systemctl stop {self.service_name}"

            else:
                return "Error"

        elif(self.service_name in self.pcs_services_list):
            if(self.operation == "enable"):
                command = f"sudo pcs resource enable {self.service_name}"

            elif(self.operation == "disable"):
                command = f"sudo pcs resource disable {self.service_name}"

            else:
                return "Error"

        else:
            return "UnknownServiceError"
        
        return command

