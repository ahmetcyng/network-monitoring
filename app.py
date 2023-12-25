from lib.Flask.src.flask import Flask, json, render_template, request, flash
from lib import json
from lib.paramiko import paramiko

from lib.apps.cluster import Cluster
from lib.apps.rabbitmq import RabbitMQ
from lib.apps.docker import Docker
from lib.apps.service import Service
from lib.apps.manuelTest import ManuelTest
from lib.apps.traceDump import TraceDump

from lib.src.server_configuration import ServerConfiguration
from lib.src.server_connect import ServerConnection
from lib.src.known_servers import KnownServers

app = Flask(__name__)
app.secret_key = "super secret key"


@app.route("/", methods=["POST","GET"])
def main():
    known_server = KnownServers()
    ip_list, status_list = known_server.server_detail()

    if(request.method == "POST"):
        arg = list(request.args.keys())[0]
        if(arg == "app_name"):
            app_name = request.args.get(arg)

            if(app_name == "cluster"):
                service_name = list(request.form.keys())[0]
                operation = request.form.get(service_name)
            
                cluster = Cluster(service_name=service_name, operation=operation)
                command = cluster.make_command()

                return render_template("cluster.html")

            elif(app_name == "rabbitmq"):
                service_name = list(request.form.keys())[0]
                operation = request.form.get(service_name)

                rabbitmq = RabbitMQ(service_name=service_name, operation=operation)
                command = rabbitmq.make_command()

                return render_template("rabbitmq.html")

            elif(app_name == "docker"):
                pass

            elif(app_name == "service"):
                service_name = list(request.form.keys())[0]
                operation = request.form.get(service_name)

                service = Service(service_name=service_name, operation=operation)
                command = service.make_command()

                return render_template("service.html")

            elif(app_name == "manuel-test"):
                service_name = list(request.form.keys())[0]
                operation = request.form.get(service_name)

                manuel_test = ManuelTest(service_name=service_name, operation=operation)
                command = manuel_test.make_command()
                
                return render_template("manuel-test.html")

            elif(app_name == "trace-dump"):
                path = request.form.get("path_textbox")
                raw_data = list(request.form.keys())[1].split(":")
                network_interface = raw_data[0]
                port = raw_data[1]
                operation = request.form.get(list(request.form.keys())[1])

                trace_dump = TraceDump(interface=network_interface, port=port, path=path, operation=operation)
                command = trace_dump.make_command()

                return render_template("trace-dump.html")

        elif(arg == "form_id"):
            form_id = request.args.get(arg)

            if(form_id == "1"):
                ip_address = request.form.get("ip_address")
                ssh_port = request.form.get("ssh_port")
                username = request.form.get("username")
                password = request.form.get("password")
                root_password = request.form.get("root_password")

                server_connection = ServerConnection(ip=ip_address, port=ssh_port, username=username, password=password, root_password = root_password)
                services, server_data, service_status_dict = server_connection.connect()

                known_server = KnownServers()
                ip_list, status_list = known_server.server_detail()
                connected_server_detail = known_server.connected_server_detail(ip=ip_address)

                return render_template("index.html", ip_list=ip_list, status_list=status_list, server_data=server_data, services=services, service_status=service_status_dict, server_hardware = connected_server_detail)

            elif(form_id == "2"):
                ip_address = request.form.get("ip_address")
                ssh_port = request.form.get("ssh_port")
                username = request.form.get("username")
                password = request.form.get("password")
                root_password = request.form.get("root_password")

                server_configuration = ServerConfiguration(ip=ip_address, port=ssh_port, username=username, password=password, root_password = root_password)
                server_configuration.configure()

                known_server = KnownServers()
                ip_list, status_list = known_server.server_detail()

                message = "Server Basariyla Eklendi"
                flash(message)

                return render_template("index.html", ip_list=ip_list, status_list=status_list)

            elif(form_id == "3"):
                return render_template("cluster.html")

            elif(form_id == "4"):
                return render_template("rabbitmq.html")

            elif(form_id == "5"):
                return render_template("docker.html")

            elif(form_id == "6"):
                return render_template("service.html")

            elif(form_id == "7"):
                return render_template("manuel-test.html")

            elif(form_id == "8"):
                return render_template("trace-dump.html")

            elif(form_id == "9"):
                raw_data = list(request.form.keys())[0].split(":")
                service_name = raw_data[0]
                server_ip = raw_data[1]
                service_operation = request.form.get(list(request.form.keys())[0])

                with open("json/connected_server.json", "r") as json_file:
                    server_json = json.load(json_file)
                    ip_address = server_json["ip"]
                    port = server_json["ssh_port"]
                    username = server_json["username"]
                    password = server_json["password"]
                    root_password = server_json["root_password"]

                if(ip_address == server_ip):
                    client_session = paramiko.SSHClient()
                    client_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client_session.connect(ip_address, port, username, password)
                    
                    with open("json/known_servers.json", "r") as json_file:
                        server_json = json.load(json_file)

                    os_name = server_json[ip_address]["os"]
                    services = list(server_json[ip_address]["services"].keys())
                    service_status_dict = {}
                    for service in services:
                        service_status_dict[service] = server_json[ip_address]["services"][service]["status"]

                    server_data = [ip_address, os_name]

                    if(service_operation == "status"):
                        command = f"systemctl status {service_name}"
                        stdin, stdout, stderr = client_session.exec_command(command=command)
                        output = stdout.readlines()
                        error = stderr.readlines()
                        if(len(error) > 0):
                            print(error)
                        else:
                            status_msg = ""
                            for i in range(3):
                                status_msg += output[i].replace("\n","")

                            flash(status_msg)

                        

                    elif(service_operation == "start"):
                        command = f"sudo systemctl start {service_name}"
                        stdin, stdout, stderr = client_session.exec_command(command=command, get_pty=True)
                        stdin.write(f"{root_password}\n")
                        stdin.flush()
                        output = stdout.readlines()

                    elif(service_operation == "stop"):
                        command = f"sudo systemctl stop {service_name}"
                        stdin, stdout, stderr = client_session.exec_command(command=command, get_pty=True)
                        stdin.write(f"{root_password}\n")
                        stdin.flush()
                        output = stdout.readlines()

                    else:
                        print("UnknownCommandError")
                    
                    return render_template("index.html", ip_list=ip_list, status_list=status_list, server_data=server_data, services=services, service_status=service_status_dict)
                
                else:
                        print("NoMatchIpAddressError")

            else:
                print("FormIdError")
        
    return render_template("index.html", ip_list=ip_list, status_list=status_list )


if __name__ == "__main__":
    app.run(debug=True)

