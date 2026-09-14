from uuid import uuid4
import docker

test_run_id = uuid4()

client = docker.from_env()

p2f_environments = {"POSTGRES_PASSWORD": "1234567890ABCDEF",
                    "POSTGRES_USER": "p2f_fastapi",
                    "POSTGRES_DB": "p2f",}

images = client.images.list("postgres:18-trix*")
postgres = images[0]

p2f_postgres = client.containers.run(image=postgres, 
                                     name=f"p2f_postgres_{str(hex(test_run_id.fields[-1]))[2:]}",
                                     ports={5432:5432}, 
                                     remove=True,
                                     detach=True,
                                     environment=p2f_environments)