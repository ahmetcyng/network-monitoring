class RabbitMQ:
    def __init__(self, service_name, operation):
        self.service_name = service_name
        self.operation = operation

    def make_command(self):
        if(self.service_name == "rabbitmq-server"):
            if(self.operation == "status"):
                command = "sudo systemctl status rabbitmq-server"

            elif(self.operation == "start"):
                command = "sudo systemctl start rabbitmq-server"

            elif(self.operation == "stop"):
                command = "sudo systemctl stop rabbitmq-server"

            elif(self.operation == "enable"):
                command = "sudo systemctl enable rabbitmq-server"

            elif(self.operation == "disable"):
                command = "sudo systemctl disable rabbitmq-server"

            else:
                return "Error"
        
        elif(self.service_name == "rabbitmqctl"):
            if(self.operation == "status"):
                command = "sudo rabbitmqctl status"
            
            elif(self.operation == "start_app"):
                command = "sudo rabbitmqctl start_app"

            elif(self.operation == "stop_app"):
                command = "sudo rabbitmqctl stop_app"

            else:
                return "Error"

        elif(self.service_name == "queues-option"):
            command = f"sudo rabbitmqctl list_queues"

        elif(self.service_name == "queue-name-textbox"):
            command = f"sudo rabbitmqctl purge_queue {self.operation}"

        else:
            return "Error"

        return command
