from random import choice
import requests
from p2f_pydantic.harm_data_record import HARM_Data_Record
from shared import base_headers
from shared import result_print
from shared import users_invalid, users_valid

def insert_record(email: str, token: str, record_hash: HARM_Data_Record, hostname: str="127.0.0.1", port: int=8000):
    headers = base_headers
    headers["x-p2f-email"] = email
    headers["x-p2f-token"] = token
    r = requests.post(f"http://{hostname}:{port}/harm-data-records/",
                      headers=headers,
                      data=record_hash.model_dump_json(exclude_unset=True))
    if r.ok:
        return True
    else:
        return False

def insert_records(dataset, email: str, token: str, hostname: str="127.0.0.1", port: int=8000):
    test_name = "RECORD INSERT"
    success_counter = 0
    for ix, row in dataset.iterrows():
        data_record = HARM_Data_Record(fk_dataset=row["dataset_id"],
                                       record_hash=row["RecordHash"])
        if insert_record(email=email, token=token, record_hash=data_record, hostname=hostname, port=port):
            success_counter += 1
    if success_counter >= (len(dataset) * 0.9):
        result_print(email=email, test=test_name, success=True)
    else:
        result_print(email=email, test=test_name, success=False)