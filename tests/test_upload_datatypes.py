import requests
from p2f_pydantic.harm_data_types import HARM_Data_Type
from shared import base_headers
from shared import result_print
from shared import users_invalid, users_valid

def insert_datatype(email: str, token: str, datatype_object: HARM_Data_Type, hostname: str="127.0.0.1", port: int=8000):
    test_name = "INSERT DATATYPE"
    headers = base_headers
    headers["x-p2f-email"] = email
    headers["x-p2f-token"] = token
    r = requests.post(f"http://{hostname}:{port}/harm-data-types/",
                      headers=headers,
                      data=datatype_object.model_dump_json(exclude_unset=True))
    if r.ok and email in users_valid:
        result_print(email=email, test=test_name, success=True)
    elif r.ok==False and email in users_invalid:
        result_print(email=email, test=test_name, success=True)
    else:
        result_print(email=email, test=test_name, success=False)

def insert_datatypes(email: str, token: str, datatypes, hostname: str="127.0.0.1", port: int=8000):
    for ix, row in datatypes.iterrows():
        datatype_object = HARM_Data_Type(
            measure=row["Measure"],
            unit_of_measurement=row["Units"],
            method=row["Method"],
            calibration=row["Calibration"],
            is_proxy=row["is_proxy"]
        )
        insert_datatype(email=email, token=token, datatype_object=datatype_object, hostname=hostname, port=port)

def get_all_inserted_datatypes(email: str, token: str, hostname: str="127.0.0.1", port: int=8000):
    test_name = "GET DATATYPES"
    headers = base_headers
    headers["x-p2f-email"] = email
    headers["x-p2f-token"] = token
    r = requests.get(f"http://{hostname}:{port}/harm-data-types/", 
                     headers=headers)
    if r.ok:
        result_print(email=email, test=test_name, success=True)
        return [HARM_Data_Type(**x).datatype_id for x in r.json()]
    else:
        result_print(email=email, test=test_name, success=False)