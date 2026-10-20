from random import choice
from json import dumps
import requests
from p2f_pydantic.seasonality import Season
from shared import base_headers
from shared import result_print
from shared import users_invalid, users_valid

def assign_location_record(record_hash, location_id, email: str, token: str, hostname:str="127.0.0.1", port:int=8000):
    headers = base_headers
    headers["x-p2f-email"] = email
    headers["x-p2f-token"] = token
    r = requests.post(f"http://{hostname}:{port}/harm-data-locations/assign-record", 
                      headers=headers,
                      params={"location_id": location_id, "record_hash": record_hash})
    if r.ok: 
        return True
    else:
        return False

def assign_season_record(record_hash, season, email: str, token: str, hostname:str="127.0.0.1", port:int=8000):
    headers = base_headers
    headers["x-p2f-email"] = email
    headers["x-p2f-token"] = token
    r = requests.post(f"http://{hostname}:{port}/season/{record_hash}", 
                      headers=headers,
                      data=Season(record_hash=record_hash, season=season).model_dump_json(exclude_unset=True))
    if r.ok: 
        return True
    else:
        return False

def assign_location_record_bytable(dataset, email: str, token: str, hostname:str="127.0.0.1", port:int=8000):
    test_name = "ASSIGN LOCATION REC"
    successes = 0
    for ix, row in dataset.iterrows():
        if assign_location_record(record_hash=row["RecordHash"],
                               location_id=row["location_id"],
                               email=email, token=token, hostname=hostname, port=port):
            successes += 1
    if successes == len(dataset):
        result_print(email=email, test=test_name, success=True)
    else:
        result_print(email=email, test=test_name, success=False)

def assign_season_record_bytable(dataset, email: str, token: str, hostname:str="127.0.0.1", port:int=8000):
    test_name = "ASSIGN SEASON REC"
    successes = 0
    for ix, row in dataset.iterrows():
        if assign_season_record(record_hash=row["RecordHash"], 
                             season=row["season"],
                             email=email, token=token, hostname=hostname, port=port):
            successes += 1
    if successes == len(dataset):
        result_print(email=email, test=test_name, success=True)
    else:
        result_print(email=email, test=test_name, success=False)