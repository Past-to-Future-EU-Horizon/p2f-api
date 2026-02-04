# Third Party Imports
from pydantic import BaseModel

class Aspect_Permissions(BaseModel):
    # Setting all to False as deny by default principle
    get: bool=False
    insert: bool=False
    update: bool=False
    delete: bool=False

class Account_Permissions(BaseModel):
    dataset: Aspect_Permissions
    harm_age: Aspect_Permissions
    harm_location: Aspect_Permissions
    harm_data_records: Aspect_Permissions
    harm_data_type: Aspect_Permissions
    harm_species: Aspect_Permissions
    harm_numerical: Aspect_Permissions
    harm_reference: Aspect_Permissions
    harm_timeslice: Aspect_Permissions
    link_git: Aspect_Permissions