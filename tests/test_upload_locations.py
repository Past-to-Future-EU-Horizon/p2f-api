import requests
from p2f_pydantic.harm_location import HARM_Location
from shared import base_headers
from shared import result_print
from shared import users_invalid, users_valid

def insert_location(email:str, token: str, location_object: HARM_Location, hostname: str, port: int):
    headers = base_headers
    headers["x-p2f-email"] = email
    headers["x-p2f-token"] = token
    r = requests.post(f"http://{hostname}:{port}/harm-data-locations/", 
                      data=location_object.model_dump_json(exclude_unset=True),
                      headers=headers)
    if r.ok and email in users_valid:
        result_print(email=email, test="Location Insert", success=True)
    elif r.ok == False and email in users_invalid:
        result_print(email=email, test="Location Insert", success=True)
    else:
        result_print(email=email, test="Location Insert", success=False)

def insert_locations(locations, email, token, hostname="127.0.0.1", port=8000):
    for ix, row in locations.iterrows():
        # print(row)
        # print(dir(row))
        # trow = row.T
        # print(trow)
        location_object = HARM_Location(location_name=row["Site Name"],
                                        location_code=row["Site Code"],
                                        latitude=row.Latitude,
                                        longitude=row.Longitude,
                                        elevation=row.Elevation,
                                        location_age=row["Location Age"])
        insert_location(email=email, token=token, location_object=location_object, hostname=hostname, port=port)

def get_all_inserted_locations(email, token, hostname="127.0.0.1", port=8000):
    headers = base_headers
    headers["x-p2f-email"] = email
    headers["x-p2f-token"] = token
    r = requests.get(f"http://{hostname}:{port}/harm-data-locations/",
                     headers=headers)
    if r.ok:
        result_print(email=email, test="Get All Locations", success=True)
        return [HARM_Location(**x).location_id for x in r.json()]
    else:
        result_print(email=email, test="Get All Locations", success=False)