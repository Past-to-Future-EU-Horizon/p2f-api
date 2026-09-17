from uuid import uuid4
from secrets import token_urlsafe
from typing import List, Dict
import docker

test_run_id = uuid4()
postgres_container_name = f"p2f_postgres_{str(hex(test_run_id.fields[-1]))[2:]}"
p2f_container_name = f"p2f_api_{str(hex(test_run_id.fields[-1]))[2:]}"
network_name = f"p2f_network_test_{str(hex(test_run_id.fields[-1]))[2:]}"

client = docker.from_env()

# Setup network
test_network = client.networks.create(
    name=network_name,
    driver="bridge",
    enable_ipv6=False,
    attachable=True,
)

# Setup container
p2f_environments = {"POSTGRES_PASSWORD": "1234567890ABCDEF",
                    "POSTGRES_USER": "p2f_fastapi",
                    "POSTGRES_DB": "p2f",
                    "P2F_ADMIN_EMAIL_ADDRESS": "admin@example.com",
                    "P2F_EMAIL_ADDRESS": "p2f@example.com",
                    "P2F_EMAIL_CIDR": "",
                    "P2F_EMAIL_IP_ACTIVE": "False",
                    "P2F_EMAIL_SA_PASSWORD": "fedcba0987654321",
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

postgres_images = client.images.list("postgres:18-trix*")
postgres_image = postgres_images[0]

# TODO Remove ports and connect tests directly into docker network
p2f_postgres = client.containers.run(image=postgres_image, 
                                     name=postgres_container_name,
                                     ports={5432:5432},
                                     remove=True,
                                     detach=True,
                                     environment=p2f_environments,
                                     network=test_network)

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
                                network=test_network, 
                                ports={8082:8082},
                                # hostname="p2f-api", 
                                environment=p2f_environments)

