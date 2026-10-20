from random import choice
import requests
from p2f_pydantic.harm_data_numerical import Insert_HARM_Numerical
from shared import base_headers
from shared import result_print
from shared import users_invalid, users_valid

def insert_numerical(email: str, token: str, numerical_insert: Insert_HARM_Numerical, hostname: str="127.0.0.1", port: int=8000):
    headers = base_headers
    headers["x-p2f-email"] = email
    headers["x-p2f-token"] = token
    r = requests.post(f"http://{hostname}:{port}/harm-numerical/",
                      headers=headers,
                      data=numerical_insert.model_dump_json(exclude_unset=True))
    if r.ok:
        return True
    else:
        return False

def insert_numericals_from_datasets(dataset, datatypes_list: list, email: str, token: str, hostname: str="127.0.0.1", port: int=8000):
    test_name = "NUMERIC_INSERT"
    datatype_float = choice(datatypes_list)
    datatype_float_conf = choice([x for x in datatypes_list if x not in [datatype_float]])
    datatype_int = choice([x for x in datatypes_list if x not in [datatype_float, datatype_float_conf]])
    datatype_int_conf = choice([x for x in datatypes_list if x not in [datatype_float, datatype_float_conf, datatype_int]])
    insert_results = {}
    for insert_type in ["float", "float_conf", "int", "int_conf"]:
        insert_results[insert_type] = 0
    for ix, row in dataset.iterrows():
        insert_float = Insert_HARM_Numerical(
            numerical_type="FLOAT",
            value=row["test_float"],
            fk_data_record=row["RecordHash"],
            fk_data_type=datatype_float
        )
        insert_float_conf = Insert_HARM_Numerical(
                    numerical_type="FLOAT",
                    value=row["test_float_v"],
                    lower_conf_interval=row["test_float_lc"],
                    lower_conf_value=row["test_float_l"], 
                    upper_conf_interval=row["test_float_uc"],
                    upper_conf_value=row["test_float_u"],
                    fk_data_record=row["RecordHash"],
                    fk_data_type=datatype_float_conf)
        insert_int = Insert_HARM_Numerical(
            numerical_type="INT",
            value=row["test_int"],
            fk_data_record=row["RecordHash"],
            fk_data_type=datatype_int
        )
        insert_int_conf = Insert_HARM_Numerical(
            numerical_type="INT",
            value=row["test_int_v"],
            lower_conf_interval=row["test_int_lc"],
            lower_conf_value=row["test_int_l"], 
            upper_conf_interval=row["test_int_uc"],
            upper_conf_value=row["test_int_u"],
            fk_data_record=row["RecordHash"],
            fk_data_type=datatype_int_conf
        )
        f = insert_numerical(email=email, token=token, numerical_insert=insert_float, port=port)
        fc = insert_numerical(email=email, token=token, numerical_insert=insert_float_conf, port=port)
        i = insert_numerical(email=email, token=token, numerical_insert=insert_int, port=port)
        ic = insert_numerical(email=email, token=token, numerical_insert=insert_int_conf, port=port)
        if f:
            insert_results["float"] += 1
        if fc:
            insert_results["float_conf"] += 1
        if i:
            insert_results["int"] += 1
        if ic:
            insert_results["int_conf"] += 1
    # print(insert_results)
    if insert_results["float"] >= (len(dataset) * 0.9):
        result_print(email=email, test=test_name, success=True)
    else:
        result_print(email=email, test=test_name, success=False)
    if insert_results["float_conf"] >= (len(dataset) * 0.9):
        result_print(email=email, test=test_name, success=True)
    else:
        result_print(email=email, test=test_name, success=False)
    if insert_results["int"] >= (len(dataset) * 0.9):
        result_print(email=email, test=test_name, success=True)
    else:
        result_print(email=email, test=test_name, success=False)
    if insert_results["int_conf"] >= (len(dataset) * 0.9):
        result_print(email=email, test=test_name, success=True)
    else:
        result_print(email=email, test=test_name, success=False)