from random import randint, choice
from string import ascii_letters, digits
from datetime import datetime, date
import requests
from p2f_pydantic.datasets import Datasets
from shared import random_doi, base_headers
from shared import users_valid, users_invalid
from shared import result_print



def build_valid_user_datasets(email):
    dataset_01 = Datasets(title=f"Dataset 01 by {email}",
                          doi=random_doi(),
                          publication_date=date(year=randint(1900, 2026), 
                                                month=randint(1, 12), 
                                                day=randint(1, 28)),
                          is_sub_dataset=False, 
                          is_new_p2f=False)
    dataset_01a = Datasets(title=dataset_01.title, 
                           doi=dataset_01.doi,
                           publication_date=dataset_01.publication_date,
                           sub_dataset_name=f"First subdataset A by {email}",
                           is_sub_dataset=True, 
                           is_new_p2f=dataset_01.is_new_p2f)
    dataset_01b = Datasets(title=dataset_01.title, 
                           doi=dataset_01.doi,
                           publication_date=dataset_01.publication_date,
                           sub_dataset_name=f"First subdataset B by {email}",
                           is_sub_dataset=True, 
                           is_new_p2f=dataset_01.is_new_p2f)
    dataset_02 = Datasets(title=f"Dataset 02 by {email}",
                          doi=random_doi(),
                          publication_date=date(year=randint(1900, 2026), 
                                                month=randint(1, 12), 
                                                day=randint(1, 28)),
                          is_sub_dataset=False, 
                          is_new_p2f=True)
    dataset_02a = Datasets(title=dataset_02.title, 
                           doi=dataset_02.doi,
                           publication_date=dataset_02.publication_date,
                           sub_dataset_name=f"Second subdataset A by {email}",
                           is_sub_dataset=True, 
                           is_new_p2f=dataset_02.is_new_p2f)
    dataset_02b = Datasets(title=dataset_02.title, 
                           doi=dataset_02.doi,
                           publication_date=dataset_02.publication_date,
                           sub_dataset_name=f"Second subdataset B by {email}",
                           is_sub_dataset=True, 
                           is_new_p2f=dataset_02.is_new_p2f)
    return (dataset_01, dataset_01a, dataset_01b, dataset_02, dataset_02a, dataset_02b)

def insert_test_user_test_eval(email, status=None, unexpected_exception=False):
    if unexpected_exception:
        success = False
    else:
        success = None
        if email in users_valid:
            if status == 200: 
                success = True
        elif email in users_invalid:
            if status in [401, 402, 403]:
                success = True
            elif status in [200, 201]:
                success = False
        # finally
        if success == None:
            success = False
    result_print(email=email, test="DATASETS UPLOAD", success=success)

def insert_dataset_user(email, token, port, hostname="127.0.0.1"):
    headers = base_headers
    headers["x-p2f-email"] = email
    headers["x-p2f-token"] = token
    valid_datasets = build_valid_user_datasets(email)
    for vd in valid_datasets:
        try:
            r = requests.post(f"http://{hostname}:{port}/datasets/",
                              data=vd.model_dump_json(exclude_unset=True),
                              headers=headers)
            insert_test_user_test_eval(email=email, status=r.status_code)
        except Exception: 
            insert_test_user_test_eval(email=email, unexpected_exception=True)

def list_datasets_utility(email: str | None = None, 
                          token: str | None = None,
                          port=8000, 
                          hostname="127.0.0.1"):
    headers = base_headers
    if email:
        headers["x-p2f-email"] = email
    if token:
        headers["x-p2f-token"] = token
    r = requests.get(f"http://{hostname}:{port}/datasets/",
                     params={"is_sub_dataset": True},
                     headers=headers)
    if r.ok:
        return [Datasets(**x) for x in r.json()]