import requests

def test_token_requesttoken(hostname="127.0.0.1", port=8000, email="admin@example.com"):
    r = requests.post(f"http://{hostname}:{port}/token/request", 
                      json={"email": email})

def extract_token(logs, email):
    next_line_password = False
    current_email = "" 
    password = None
    for line in logs.split("\n"):
        if next_line_password:
            password = line
            next_line_password = False
        if "Your token for the P2F Portal is below" in line and current_email == email:
            next_line_password = True
        if "To: " in line:
            current_email = line[4:]
            # print(current_email == email)
    return password