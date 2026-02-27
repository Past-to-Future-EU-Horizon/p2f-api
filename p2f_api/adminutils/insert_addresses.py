from ..service.temp_accounts  import insert_permitted_address
from ..service.account_permissions_json import Account_Permissions
from ..service.account_permissions_json import default_consortium_permissions, super_user, public_view
import pandas as pd
from email_validator import validate_email
from furl import furl
from argparse import ArgumentParser
import pathlib

TLD_TIMEZONE_MAP = {
    ".nl": "Europe/Amsterdam",
    ".de": "Europe/Berlin",
    ".uk": "Europe/London", 
    ".at": "Europe/Vienna",
    ".ch": "Europe/Zurich", 
    ".ee": "Europe/Tallinn", 
    ".dk": "Europe/Copenhagen",
    ".edu": "America/New_York",
    ".cz": "Europe/Prague",
    ".be": "Europe/Brussels",
    ".lv": "Europe/Riga", 
    ".es": "Europe/Madrid", 
    ".au": "Australia/Canberra", 
    ".fi": "Europe/Helsinki", 
    ".org": "Europe/Brussels"
    }

PERMISSIONS_MAP = {"default_consortium_permissions": default_consortium_permissions,
                   "super_user": super_user,
                   "public_view": public_view}

def args_collect():
    parser = ArgumentParser()
    parser.add_argument("-f", "--address-file", help="The file with the valid email addresses.")
    parser.add_argument("-i", "--individual-email", help="Individual email address")
    parser.add_argument("-p", "--permissions", default="default_consortium_permissions")
    return parser.parse_args()

def read_address_file(filename: str):
    fpath = pathlib.Path(filename)
    match fpath.suffix:
        case "csv":
            df = pd.read_csv(filename, header=None)
        case "xlsx":
            df = pd.read_excel(filename, header=None)
    all_emails = []
    for ix, row in df.iterrows():
        raw_email = row[0]
        all_emails.append(clean_address(raw_email))
    return all_emails

def clean_address(address: str):
    while address[-1] in [" "]:
        address = address[:-1]
    while address[0] in [" "]:
        address = address[1:]
    return address

def handle_email_address_file(addresses: list):
    for address in addresses:
        validemail = validate_email(address)
        tld = validemail.domain.split(".")[-1]
        if f".{tld}" in TLD_TIMEZONE_MAP.keys():
            tz = TLD_TIMEZONE_MAP[f".{tld}"]
        else:
            tz = "UTC"
        insert_permitted_address(email=address, 
                                 permissions=default_consortium_permissions, 
                                 timezone=tz)
    

if __name__ == "__main__":
    args = args_collect()
    if args.i is not None:
        address = clean_address(args.i)
    if args.f is not None:
        addrs = read_address_file(args.f)
        handle_email_address_file(addresses=addrs)