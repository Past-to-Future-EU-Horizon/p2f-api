from uuid import uuid4
from time import sleep
from subprocess import run
from secrets import token_urlsafe
from random import randint, choice
import socket
import errno
from typing import List, Dict
import docker
from shared import consortium_user_email, p2f_admin_email, unauthorized_user_email
from shared import result_print
from shared import is_token_valid
from test_request_token import test_token_requesttoken, extract_token
from test_datasets_token import insert_dataset_user, list_datasets_utility, get_dataset
from test_upload_locations import insert_locations, get_all_inserted_locations
from test_upload_datatypes import insert_datatypes, get_all_inserted_datatypes
from test_insert_numerics import insert_numericals_from_datasets
from test_get_numerics import read_numeric_stats, list_numerics_iterated, list_numerics_specific
from test_insert_records import insert_records
from test_assign_record_metadata import assign_location_record_bytable, assign_season_record_bytable
from test_get_dataset_metadata import get_locations_by_dataset_id
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

# DUMP startup logging issues
# sleep(1)
# with open(f"tests/test_apilogs_{test_run_id}_STARTUPDUMP.txt", "w") as f:
#     f.write(p2f_api.logs().decode("utf8"))

print(f"----- {test_run_id} STARTING -----------------")

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

logs_counter = 0
while logs_http_started is False:
    logs = get_logs_docker(p2f_api)
    for line in logs.split("\n"):
        if """INFO:     Uvicorn running on""" in line:
            result_print(email="Server", test="API STARTUP", success=True)
            logs_http_started = True
    logs_counter += 1
    if logs_counter % 5 == 0:
        with open(f"tests/test_apilogs_{test_run_id}.txt", "w") as f:
            f.write(p2f_api.logs().decode("utf8"))

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
with open(f"tests/test_apilogs_{test_run_id}.txt", "w") as f:
    f.write(p2f_api.logs().decode("utf8"))

datasets = list_datasets_utility(email=p2f_admin_email, 
                                 token=p2f_admin_token,
                                 port=p2f_container_port)
for dataset in datasets:
    if get_dataset(dataset_id=dataset.dataset_id,
                    email=p2f_admin_email,
                    token=p2f_admin_token,
                    port=p2f_container_port):
        result_print(email=p2f_admin_email, test="GET DATASET", success=True)
    else:
        result_print(email=p2f_admin_email, test="GET DATASET", success=False)
with open(f"tests/test_apilogs_{test_run_id}.txt", "w") as f:
    f.write(p2f_api.logs().decode("utf8"))

# Records Tests

##   Data Loading Tests
## # Locations
admin_locations = generate_locations(n=10)
member_locations = generate_locations(n=10)
unauth_locations = generate_locations(n=10)
insert_locations(locations=admin_locations, email=p2f_admin_email, token=p2f_admin_token, port=p2f_container_port)
insert_locations(locations=member_locations, email=consortium_user_email, token=consortium_user_token, port=p2f_container_port)
insert_locations(locations=unauth_locations, email=unauthorized_user_email, token=unauthorized_user_token, port=p2f_container_port)
locations_uuids = get_all_inserted_locations(email=p2f_admin_email, token=p2f_admin_token, port=p2f_container_port)
get_all_inserted_locations(email=consortium_user_email, token=consortium_user_token, port=p2f_container_port)
get_all_inserted_locations(email=unauthorized_user_email, token=unauthorized_user_token, port=p2f_container_port)



## # Species
## # Data Types
admin_datatypes = generate_data_types(n=10)
member_datatypes = generate_data_types(n=10)
unauth_datatypes = generate_data_types(n=10)
insert_datatypes(email=p2f_admin_email, token=p2f_admin_token, datatypes=admin_datatypes, port=p2f_container_port)
insert_datatypes(email=consortium_user_email, token=consortium_user_token, datatypes=member_datatypes, port=p2f_container_port)
insert_datatypes(email=unauthorized_user_email, token=unauthorized_user_token, datatypes=unauth_datatypes, port=p2f_container_port)
datatype_uuids = get_all_inserted_datatypes(email=p2f_admin_email, token=p2f_admin_token, port=p2f_container_port)
get_all_inserted_datatypes(email=consortium_user_email, token=consortium_user_token, port=p2f_container_port)
get_all_inserted_datatypes(email=unauthorized_user_email, token=unauthorized_user_token, port=p2f_container_port)
####TODO Add get datatypes with filters
## # Time Slices

datasets = {x.dataset_id: generate_dataset(x.dataset_id, location_list=locations_uuids) for x in datasets}
# print(datasets)
with open(f"tests/test_apilogs_{test_run_id}.txt", "w") as f:
    f.write(p2f_api.logs().decode("utf8"))

# Distribute datasets to users
dataset_len = int(round((len(datasets.keys())/2), 0))
admin_datasets = list(datasets.keys())[:dataset_len]
member_datasets = [x for x in datasets.keys() if x not in admin_datasets]

# Records
for dataset in admin_datasets:
    insert_records(dataset=datasets[dataset], email=p2f_admin_email, token=p2f_admin_token, port=p2f_container_port)
sleep(2)
for dataset in member_datasets:
    insert_records(dataset=datasets[dataset], email=consortium_user_email, token=consortium_user_token, port=p2f_container_port)
sleep(2)

# Numeric Tests
for dataset in admin_datasets:
    insert_numericals_from_datasets(dataset=datasets[dataset], datatypes_list=datatype_uuids, email=p2f_admin_email, token=p2f_admin_token, port=p2f_container_port)
sleep(2)
for dataset in member_datasets:
    insert_numericals_from_datasets(dataset=datasets[dataset], datatypes_list=datatype_uuids, email=consortium_user_email, token=consortium_user_token, port=p2f_container_port)
# print("STATUS: SLEEPING 30 SECONDS")
# sleep(30)
# print("STATUS: WAKING UP")
datatypes_numeric, datasets_numeric = read_numeric_stats(datatypes=datatype_uuids, datasets=list(datasets.keys()), port=p2f_container_port)
with open(f"tests/test_apilogs_{test_run_id}.txt", "w") as f:
    f.write(p2f_api.logs().decode("utf8"))
list_numerics_iterated(email=p2f_admin_email, token=p2f_admin_token, port=p2f_container_port,
                       datasets=list(datasets.keys())[:10], 
                       datatypes=datatype_uuids, 
                       record_hashes=list(datasets.values())[0]["RecordHash"].unique()[:10])
with open(f"tests/test_apilogs_{test_run_id}.txt", "w") as f:
    f.write(p2f_api.logs().decode("utf8"))

# reformat the stats results
datasets_numeric = {str(x): y.model_dump(exclude_unset=True) for x, y in datasets_numeric.items()}
datatypes_numeric = {str(x): y.model_dump(exclude_unset=True) for x, y in datatypes_numeric.items()}
# output check 
# print(datatypes_numeric, datasets_numeric)
# select the specific candidates
specific_dataset_admin = choice([x for x, y in datasets_numeric.items() if y["count_total"] > 0])
numeric_dataset_admin = choice([x for x, y in datasets_numeric[specific_dataset_admin].items() if y > 0 and "total" not in x]).replace("count_", "")
specific_dataset_member = choice([x for x, y in datasets_numeric.items() if x != specific_dataset_admin and y["count_total"] > 0])
numeric_dataset_member = choice([x for x, y in datasets_numeric[specific_dataset_member].items() if y > 0 and "total" not in x]).replace("count_", "")
specific_datatype_admin = choice([x for x, y in datatypes_numeric.items() if y["count_total"] > 0])
numeric_datatype_admin = choice([x for x, y in datatypes_numeric[specific_datatype_admin].items() if y > 0 and "total" not in x]).replace("count_", "")
specific_datatype_member = choice([x for x, y in datatypes_numeric.items() if x != specific_datatype_admin and y["count_total"] > 0])
numeric_datatype_member = choice([x for x, y in datatypes_numeric[specific_datatype_member].items() if y > 0 and "total" not in x]).replace("count_", "")
# Run the tests
list_numerics_specific(email=p2f_admin_email, token=p2f_admin_token, 
                       dataset=specific_dataset_admin, numeric_type=numeric_dataset_admin, port=p2f_container_port)
list_numerics_specific(email=consortium_user_email, token=consortium_user_token, 
                       dataset=specific_dataset_member, numeric_type=numeric_dataset_member, port=p2f_container_port)
list_numerics_specific(email=p2f_admin_email, token=p2f_admin_token, 
                       dataset=specific_datatype_admin, numeric_type=numeric_datatype_admin, port=p2f_container_port)
list_numerics_specific(email=consortium_user_email, token=consortium_user_token, 
                       dataset=specific_datatype_member, numeric_type=numeric_datatype_member, port=p2f_container_port)

## # Records Location Tests
for dataset in admin_datasets:
    assign_location_record_bytable(dataset=datasets[dataset], 
                                   email=p2f_admin_email, token=p2f_admin_token, port=p2f_container_port)
for dataset in member_datasets:
    assign_location_record_bytable(dataset=datasets[dataset], 
                                   email=consortium_user_email, token=consortium_user_token, port=p2f_container_port)
## # Records Species Tests
## # Records Season Tests
for dataset in admin_datasets:
    assign_season_record_bytable(dataset=datasets[dataset],
                                 email=p2f_admin_email, token=p2f_admin_token, port=p2f_container_port)
for dataset in member_datasets:
    assign_season_record_bytable(dataset=datasets[dataset],
                                 email=consortium_user_email, token=consortium_user_token, port=p2f_container_port)
## # Records Data Types Tests
## # Records References Tests
## # Records Age Tests

##   Metadata Tests
## # Datasets Location Tests
get_locations_by_dataset_id(dataset_ids=[str(x) for x in datasets.keys()],
                            email=p2f_admin_email, token=p2f_admin_token, port=p2f_container_port)
get_locations_by_dataset_id(dataset_ids=[str(x) for x in datasets.keys()],
                            email=consortium_user_email, token=consortium_user_token, port=p2f_container_port)
## # Datasets Seasonality Tests
## # Datasets Git Repository Tests
## # Datasets Time Coverage Tests
## # Datasets Species Tests
## # Datasets Data Types Tests
## # Datasets Time Slices Tests
## # Datasets Tags & Keywords Tests

with open(f"tests/test_apilogs_{test_run_id}.txt", "w") as f:
    f.write(p2f_api.logs().decode("utf8"))

print(f"----- {test_run_id} FINISHED -----------------")
p2f_api.stop()
# p2f_api.remove()
p2f_postgres.stop()
test_network.remove()