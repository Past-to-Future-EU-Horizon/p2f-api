from uuid import uuid4
from time import sleep
from subprocess import run
from secrets import token_urlsafe
from random import randint
import socket
import errno
from typing import List, Dict
import docker
from shared import consortium_user_email, p2f_admin_email, unauthorized_user_email
from shared import result_print
from shared import is_token_valid
from test_request_token import test_token_requesttoken, extract_token
from test_datasets_token import insert_dataset_user, list_datasets_utility
from generate_data import generate_dataset, generate_locations
from generate_data import generate_data_types

test_run_id = uuid4()
postgres_container_name = f"p2f_postgres_{str(hex(test_run_id.fields[-1]))[2:]}"
p2f_container_name = f"p2f_api_{str(hex(test_run_id.fields[-1]))[2:]}"
network_name = f"p2f_network_test_{str(hex(test_run_id.fields[-1]))[2:]}"

def random_port_wcheck():
    port_available = False
    while port_available is False:
        port = randint(8000, 9999)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(("127.0.0.1", port))
            port_available = True
        except socket.error as e:
            errrrrrrrr = e
        finally:
            s.close()
    return port
p2f_container_port = random_port_wcheck()

client = docker.from_env()

# Setup network
test_network = client.networks.create(
    name=network_name,
    driver="bridge",
    enable_ipv6=False,
    attachable=True,
)

# Setup container
p2f_environments = {"POSTGRES_PASSWORD": token_urlsafe(64)[:20],
                    "POSTGRES_USER": "p2f_fastapi",
                    "POSTGRES_DB": "p2f",
                    "P2F_ADMIN_EMAIL_ADDRESS": p2f_admin_email,
                    "P2F_EMAIL_ADDRESS": "p2f@example.com",
                    "P2F_EMAIL_CIDR": "",
                    "P2F_EMAIL_IP_ACTIVE": "False",
                    "P2F_EMAIL_SA_PASSWORD": token_urlsafe(64)[:20],
                    "P2F_EMAIL_SA_PORT": "587",
                    "P2F_EMAIL_SA_SERVER": "smtp.example.com",
                    "P2F_EMAIL_SA_USERNAME": "sa_P2F_EMAIL",
                    "P2F_HASH_COUNT": "2000",
                    "P2F_SALT": token_urlsafe(64),
                    "P2F_TOKEN_DEBUG": "True",
                    "P2F_TOKEN_LENGTH": "64",
                    "P2F_TOKEN_TTL": "86400",
                    "P2F_PORTAL_EMAIL_ADDRESS": "portal@example.com",
                    "P2F_PORTAL_TOKEN": token_urlsafe(64)[:64],
                    }
p2f_environments["PG_USER"] = p2f_environments["POSTGRES_USER"]
p2f_environments["PG_PASS"] = p2f_environments["POSTGRES_PASSWORD"]
p2f_environments["PG_HOST"] = postgres_container_name
p2f_environments["PG_PORT"] = "5432"
p2f_environments["PG_DB"] = p2f_environments["POSTGRES_DB"]

print(p2f_environments)

postgres_images = client.images.list("postgres:18-trix*")
postgres_image = postgres_images[0]

# TODO Remove ports and connect tests directly into docker network
p2f_postgres = client.containers.run(image=postgres_image, 
                                     name=postgres_container_name,
                                    #  ports={5432:5432},
                                     remove=True,
                                     detach=True,
                                     environment=p2f_environments,
                                     network=test_network.name)

def highest_epoch_seconds(history: List[Dict]) -> int:
    rv = 0
    for h in history:
        if h["Created"] > rv:
            rv = h["Created"]
    return rv

p2f_api_images = client.images.list("p2f-api*")
p2f_api_image_ages = {highest_epoch_seconds(x.history()): x.id.split(":")[-1]  for x in p2f_api_images}
p2f_api_image = p2f_api_image_ages[max(p2f_api_image_ages.keys())]

p2f_api = client.containers.run(image=p2f_api_image,
                                name=p2f_container_name,
                                remove=True,
                                detach=True,
                                network=test_network.name, 
                                ports={8084:p2f_container_port},
                                # hostname="p2f-api", 
                                environment=p2f_environments)

# print("Starting a 5 second sleep to let the API get started")
# sleep(5) # Let the API get started

def get_logs_cmd(container=p2f_api):
    print(["docker", "logs", container.short_id])
    logs = run(["docker", "logs", container.short_id], capture_output=True)
    logs = logs.stdout.decode("utf8")
    return logs

def get_logs_docker(container=p2f_api):
    logs = container.logs()
    logs = logs.decode("utf8")
    return logs

logs_http_started = False

while logs_http_started is False:
    logs = get_logs_docker(p2f_api)
    for line in logs.split("\n"):
        if """INFO:     Uvicorn running on""" in line:
            result_print(email="Server", test="API STARTUP", success=True)
            logs_http_started = True

# Add Consortium Member 
add_user = p2f_api.exec_run(["python", "adminutils/insert_addresses.py", "-i", consortium_user_email])
# print(add_user.output.decode("utf8"))

# Request Token
## Admin
test_token_requesttoken(port=p2f_container_port, email=p2f_admin_email)
sleep(2)
token_logs = get_logs_docker(p2f_api)
p2f_admin_token = extract_token(logs=token_logs, email=p2f_admin_email)
result_print(email=p2f_admin_email, 
             test="VALID USER TOKEN", 
             success=is_token_valid(token=p2f_admin_token, email=p2f_admin_email))
## Consortium User
test_token_requesttoken(port=p2f_container_port, email=consortium_user_email)
sleep(2)
token_logs = get_logs_docker(p2f_api)
consortium_user_token = extract_token(logs=token_logs, email=consortium_user_email)
result_print(email=consortium_user_email, 
             test="VALID USER TOKEN", 
             success=is_token_valid(token=consortium_user_token, email=consortium_user_email))
## Random Person
test_token_requesttoken(port=p2f_container_port, email=unauthorized_user_email)
sleep(2)
token_logs = get_logs_docker(p2f_api)
unauthorized_user_token = extract_token(logs=token_logs, email=unauthorized_user_email)
result_print(email=unauthorized_user_email, 
             test="INVALID USER TOKEN", 
             success=is_token_valid(token=unauthorized_user_token, email=unauthorized_user_email))

# Datasets Tests
insert_dataset_user(email=p2f_admin_email, token=p2f_admin_token, port=p2f_container_port)
insert_dataset_user(email=consortium_user_email, token=consortium_user_token, port=p2f_container_port)
insert_dataset_user(email=unauthorized_user_email, token=unauthorized_user_token, port=p2f_container_port)
datasets = list_datasets_utility(email=p2f_admin_email, 
                                 token=p2f_admin_token,
                                 port=p2f_container_port)
datasets = {x.dataset_id: generate_dataset(x.dataset_id) for x in datasets}
# print(datasets)
# Records Tests

##   Data Loading Tests
## # Locations
locations = generate_locations(n=10)
## # Species
## # Data Types
data_types = generate_data_types(n=10)
## # Time Slices

# Numeric Tests

##   Metadata Tests
## # Datasets Location Tests
## # Datasets Seasonality Tests
## # Datasets Git Repository Tests
## # Datasets Time Coverage Tests
## # Datasets Species Tests
## # Datasets Data Types Tests
## # Datasets Time Slices Tests
## # Datasets Tags & Keywords Tests
## # Records Location Tests
## # Records Species Tests
## # Records Season Tests
## # Records Data Types Tests
## # Records References Tests
## # Records Age Tests

with open(f"tests/test_apilogs_{test_run_id}.txt", "w") as f:
    f.write(p2f_api.logs().decode("utf8"))

p2f_api.stop()
p2f_postgres.stop()
test_network.remove()