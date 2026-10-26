import requests
from p2f_pydantic.harm_location import HARM_Location

from shared import result_print
from shared import base_headers
from shared import mimes

def get_locations_by_dataset_id(dataset_ids, email: str, token: str, hostname: str="127.0.0.1", port:int=8000,):
    test_name = "GET LOCATIONS BY DATASET"
    dataset_successes = 0
    for dataset_id in dataset_ids:
        headers = base_headers
        headers["x-p2f-email"] = email
        headers["x-p2f-token"] = token
        params = {"dataset_id": dataset_id}
        r = requests.get(f"http://{hostname}:{port}/harm-data-locations/",
                        headers=headers,
                        params=params)
        if r.ok:
            try: 
                results = [HARM_Location(**x) for x in r.json()]
                # print(results)
                dataset_successes += 1
            except Exception as e:
                print(e)
    if len(dataset_ids) == dataset_successes:
        result_print(email=email, test=test_name, success=True)
    else:
        result_print(email=email, test=test_name, success=False)