# Third Party Imports
from pydantic import BaseModel

class Aspect_Permissions(BaseModel):
    # Setting all to False as deny by default principle
    get: bool=False
    insert: bool=False
    update: bool=False
    delete: bool=False

class Account_Permissions(BaseModel):
    datasets: Aspect_Permissions
    harm_age: Aspect_Permissions
    harm_location: Aspect_Permissions
    harm_data_records: Aspect_Permissions
    harm_data_type: Aspect_Permissions
    harm_species: Aspect_Permissions
    harm_numerical: Aspect_Permissions
    harm_reference: Aspect_Permissions
    harm_timeslice: Aspect_Permissions
    link_git: Aspect_Permissions

default_consortium_permissions = Account_Permissions(
    datasets=Aspect_Permissions(get=True, insert=True, update=False, delete=False), 
    harm_age=Aspect_Permissions(get=True, insert=True, update=False, delete=False), 
    harm_location=Aspect_Permissions(get=True, insert=True, update=False, delete=False), 
    harm_data_records=Aspect_Permissions(get=True, insert=True, update=False, delete=False), 
    harm_data_type=Aspect_Permissions(get=True, insert=True, update=False, delete=False), 
    harm_species=Aspect_Permissions(get=True, insert=True, update=False, delete=False), 
    harm_numerical=Aspect_Permissions(get=True, insert=True, update=False, delete=False), 
    harm_reference=Aspect_Permissions(get=True, insert=True, update=False, delete=False), 
    harm_timeslice=Aspect_Permissions(get=True, insert=True, update=False, delete=False), 
    link_git=Aspect_Permissions(get=True, insert=True, update=False, delete=False), 
)

public_view = Account_Permissions(
    datasets=Aspect_Permissions(get=True, insert=False, update=False, delete=False), 
    harm_age=Aspect_Permissions(get=True, insert=False, update=False, delete=False), 
    harm_location=Aspect_Permissions(get=True, insert=False, update=False, delete=False), 
    harm_data_records=Aspect_Permissions(get=True, insert=False, update=False, delete=False), 
    harm_data_type=Aspect_Permissions(get=True, insert=False, update=False, delete=False), 
    harm_species=Aspect_Permissions(get=True, insert=False, update=False, delete=False), 
    harm_numerical=Aspect_Permissions(get=True, insert=False, update=False, delete=False), 
    harm_reference=Aspect_Permissions(get=True, insert=False, update=False, delete=False), 
    harm_timeslice=Aspect_Permissions(get=True, insert=False, update=False, delete=False), 
    link_git=Aspect_Permissions(get=True, insert=False, update=False, delete=False), 
)

super_user = Account_Permissions(
    datasets=Aspect_Permissions(get=True, insert=True, update=True, delete=True), 
    harm_age=Aspect_Permissions(get=True, insert=True, update=True, delete=True), 
    harm_location=Aspect_Permissions(get=True, insert=True, update=True, delete=True), 
    harm_data_records=Aspect_Permissions(get=True, insert=True, update=True, delete=True), 
    harm_data_type=Aspect_Permissions(get=True, insert=True, update=True, delete=True), 
    harm_species=Aspect_Permissions(get=True, insert=True, update=True, delete=True), 
    harm_numerical=Aspect_Permissions(get=True, insert=True, update=True, delete=True), 
    harm_reference=Aspect_Permissions(get=True, insert=True, update=True, delete=True), 
    harm_timeslice=Aspect_Permissions(get=True, insert=True, update=True, delete=True), 
    link_git=Aspect_Permissions(get=True, insert=True, update=True, delete=True), 
)