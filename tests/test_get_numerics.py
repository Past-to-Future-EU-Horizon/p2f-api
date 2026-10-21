from random import choice
from time import sleep
import requests
from p2f_pydantic.harm_data_numerical import Numerical_Table_Statistics
from p2f_pydantic.harm_data_types import HARM_Data_Type
from shared import result_print
from shared import base_headers
from shared import mimes

def get_datatype_by_dataset_id(dataset_id, email: str, token: str, hostname: str="127.0.0.1", port:int=8000,):
    headers = base_headers
    headers["x-p2f-email"] = email
    headers["x-p2f-token"] = token
    params = {"dataset_id": dataset_id}
    r = requests.get(f"http://{hostname}:{port}/harm-data-types/",
                     headers=headers,
                     params=params)
    if r.ok:
        datatypes = [str(HARM_Data_Type(**x).datatype_id) for x in r.json()]
        return choice(datatypes)

def read_numeric_stats(datatypes: list, datasets: list, hostname: str = "127.0.0.1", port: int = 8000):
    test_datatype_name = "NUMERIC STATS DATATYPE"
    test_dataset_name = "NUMERIC STATS DATASET"
    success_datatype = 0
    datatypes_collections = {}
    success_dataset = 0
    datasets_collections = {}
    for datatype in datatypes:
        r = requests.get(f"http://{hostname}:{port}/harm-numerical/statistics",
                         headers=base_headers,
                         params={"datatype_id": datatype})
        if r.ok:
            success_datatype += 1
            datatypes_collections[datatype] = Numerical_Table_Statistics(**r.json())
        sleep(5)
    if success_datatype == len(datatypes):
        result_print(email="Not needed", test=test_datatype_name, success=True)
    else: 
        result_print(email="Not needed", test=test_datatype_name, success=False)
    for dataset in datasets:
        r = requests.get(f"http://{hostname}:{port}/harm-numerical/statistics",
                         headers=base_headers,
                         params={"dataset_id": dataset})
        if r.ok:
            success_dataset += 1
            datasets_collections[dataset] = Numerical_Table_Statistics(**r.json())
        sleep(5)    
    if success_dataset == len(datasets):
        result_print(email="Not needed", test=test_dataset_name, success=True)
    else: 
        result_print(email="Not needed", test=test_dataset_name, success=False)
    return datatypes_collections, datasets_collections

def list_numerics_iterated(email: str, token: str, hostname: str="127.0.0.1", port:int=8000,
                           record_hashes:list=None, datasets: list=None, datatypes: list=None):
    headers = base_headers
    headers["x-p2f-email"] = email
    headers["x-p2f-token"] = token
    ###### BY RECORD HASH
    record_success = 0
    for record_hash in record_hashes:
        r = requests.get(f"http://{hostname}:{port}/harm-numerical/",
                         headers=headers,
                         params={"record_hash": record_hash})
        if r.ok:
            record_success += 1
    if len(record_hashes) == record_success:
        result_print(email=email, test="LIST NUMERIC BY RECORD", success=True)
    else:
        result_print(email=email, test="LIST NUMERIC BY RECORD", success=False)
    ####### BY DATASET ID
    dataset_success = 0
    for dataset in datasets:
        r = requests.get(f"http://{hostname}:{port}/harm-numerical/",
                         headers=headers,
                         params={"dataset_id": dataset})
        if r.ok:
            dataset_success += 1
    if len(datasets) == dataset_success:
        result_print(email=email, test="LIST NUMERIC BY DATASET", success=True)
    else:
        result_print(email=email, test="LIST NUMERIC BY DATASET", success=False)
    ######## BY DATATYPE
    datatype_success = 0
    for datatype in datatypes:
        r = requests.get(f"http://{hostname}:{port}/harm-numerical/",
                         headers=headers,
                         params={"datatype_id": datatype})
        if r.ok:
            datatype_success += 1
    if len(datasets) == dataset_success:
        result_print(email=email, test="LIST NUMERIC BY DATATYPE", success=True)
    else:
        result_print(email=email, test="LIST NUMERIC BY DATATYPE", success=False)

def list_numerics_specific(email: str, token: str, numeric_type: str, hostname: str="127.0.0.1", port:int=8000,
                           record_hash:str=None, dataset: str=None, datatype: str=None,):
    headers = base_headers
    headers["x-p2f-email"] = email
    headers["x-p2f-token"] = token
    params = {
        "numeric_type": numeric_type,
        "record_hash": record_hash,
        "dataset_id": dataset,
        "datatype_id": datatype
    }
    params = {x: y for x, y in params.items() if y is not None}
    for test_name, mime_type in mimes.items():
        headers["Accept"] = mime_type
        r = requests.get(f"http://{hostname}:{port}/harm-numerical/",
                        headers=headers,
                        params=params)
        if r.ok:
            result_print(email=email, test=f"LIST NUMERIC SPECIFIC {test_name}", success=True)
        else:
            result_print(email=email, test=f"LIST NUMERIC SPECIFIC {test_name}", success=False)

