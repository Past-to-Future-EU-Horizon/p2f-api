from random import randint, choice, random
from uuid import UUID, uuid4
from hashlib import md5
import pandas as pd

def record_hash(dataset_id: UUID, row: int):
    h = md5()
    h.update(str(dataset_id).encode("utf8"))
    h.update(str(row).encode("utf8"))
    return h.hexdigest()

def generate_dataset(dataset_id: UUID, 
                     n: int=100):
    df = pd.DataFrame(columns=["dataset_id", "Record ID", "RecordHash", 
                               "test_int", 
                               "test_int_v", "test_int_l", "test_int_u", "test_int_lc", "test_int_uc",
                               "test_float",
                               "test_float_v", "test_float_l", "test_float_u", "test_float_lc", "test_float_uc",
                               "season", "age", "length_along_core",])
    seasonality_dict = {"hot/cold": ["Hot", "Cold"],
                        "summer/winter": ["Summer", "Winter"],
                        "spring/summer/fall/winter": ["Spring", "Summer", "Fall", "Winter"]}
    seasonality = choice(list(seasonality_dict.keys()))
    for i in range(n):
        test_int_v = randint(-2000, 2000)
        test_int_l = randint(int(test_int_v - abs(test_int_v*0.5)), test_int_v)
        test_int_u = randint(test_int_v, int(test_int_v + abs(test_int_v*0.5)))
        test_int_lc = choice([5, 2.5])
        test_int_uc = 95
        if test_int_lc == 2.5:
            test_int_uc = 97.5
        test_float_v = randint(-2000, 2000) + random()
        test_float_l = randint(int(test_float_v - abs(test_float_v*0.5)), int(test_float_v)) - random()
        test_float_u = randint(int(test_float_v), int(test_float_v + abs(test_float_v*0.5))) + random()
        test_float_lc = choice([5, 2.5])
        test_float_uc = 95
        if test_float_lc == 2.5:
            test_float_uc = 97.5
        season = choice(seasonality_dict[seasonality])
        age = randint(0, 5_000_000)
        length_along_core = randint(0, 20) + random()
        df.loc[i] = (dataset_id, i, record_hash(dataset_id, i),
                     randint(-2000, 2000),
                     test_int_v, test_int_l, test_int_u, test_int_lc, test_int_uc,
                     randint(-2000, 2000) + random(), 
                     test_float_v, test_float_l, test_float_u, test_float_lc, test_float_uc,
                     season, age, length_along_core)
    return df

def generate_location():
    location_code = str(hex(uuid4().fields[1]))[2:]
    site_name = f"Random Location {location_code}"
    site_code = f"RL_{location_code.upper()}"
    latitude = round((randint(-89, 89) + random()), 5)
    longitude = round((randint(-179, 179) + random()), 5)
    elevation = round((randint(-1000, 5000) + random()), 5)
    location_age = 0
    if choice([True, False, False, False, False, False]):
        location_age = randint(200, 5_000_000)
    return (site_name, site_code, latitude, longitude, elevation, location_age)
    
def generate_locations(n: int = 10):
    df = pd.DataFrame(columns=["Site Name", "Site Code", "Latitude", "Longitude", "Elevation", "Location Age"])
    for i in range(n):
        df.loc[i] = generate_location()
    return df

def generate_data_types(n: int = 10):
    df = pd.DataFrame(columns=["Measure", "Units", "Method", "Calibration", "is_proxy"])
    for i in range(n+20):
        measure = choice(["Sea Surface Temperatures (SST)", "Moes Hardness Scale", "Bottle Water Temperature (BWT)", "Mg/Ca", "dO12", "UK37"])
        units = choice(["Celcius", "mmol/L", "Meters", "%", "log"])
        calibration = choice(["BAYMAG", "None", "Against Reference", "Pu132 Explosive Space Modulator", "Best Guess", "None"])
        method = choice(["Direct measurement", "Mg/Ca", "UK37", "Tile Scratch", "Spectrometry", "Crystallography", "Diffraction", "Sublimation"])
        is_proxy = choice([True, False])
        df.loc[i] = (measure, units, method, calibration, is_proxy)
    df.drop_duplicates()
    return df[:n]