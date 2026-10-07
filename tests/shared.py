from random import randint, choice
from string import ascii_letters, digits

base_headers = {"Accept": "application/json", "Content-Type": "application/json"}

p2f_admin_email = "admin@example.com"
consortium_user_email = "user@example.com"
unauthorized_user_email = "unauthorized@example.com"
users_valid = [p2f_admin_email, consortium_user_email]
users_invalid = [unauthorized_user_email]

def random_doi():
    doi = "10."
    for i in range(randint(5, 8)):
        doi += choice(list(ascii_letters + digits))
    doi += "/"
    for i in range(randint(6, 12)):
        doi += choice(list(ascii_letters + digits))
    return doi

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def result_print(email: str, test: str, success: bool):
    if success:        
        success_text = f"{bcolors.OKGREEN}SUCCESS{bcolors.ENDC}"
    else:
        success_text = f"{bcolors.FAIL}FAILURE{bcolors.ENDC}"
    print(f"RESULT: {test:^30}{email:^30}-{success_text:>15}")

def is_token_valid(token: str | None, email: str):
    success = False
    if email in users_valid:
        if len(token) == len([x for x in token if x in list(ascii_letters + digits + "_-")]):
            success = True
    elif email in users_invalid:
        if token is None:
            success = True
    return success