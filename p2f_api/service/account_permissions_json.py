# Third Party Imports
from pydantic import BaseModel

class Aspect_Permissions(BaseModel):
    # Setting all to False as deny by default principle
    get: bool=False
    post: bool=False
    put: bool=False
    delete: bool=False

class Account_Permissions(BaseModel):
    datasets: Aspect_Permissions
    harm_data_age: Aspect_Permissions
    harm_data_locations: Aspect_Permissions
    harm_data_records: Aspect_Permissions
    harm_data_types: Aspect_Permissions
    harm_data_species: Aspect_Permissions
    harm_numerical: Aspect_Permissions
    harm_reference: Aspect_Permissions
    harm_timeslice: Aspect_Permissions
    link_git: Aspect_Permissions
    age_models: Aspect_Permissions
    data_frequency: Aspect_Permissions
    seasonality: Aspect_Permissions
    season: Aspect_Permissions
    time_coverage: Aspect_Permissions

TFFF = Aspect_Permissions(get=True, post=False, put=False, delete=False)
TTFF = Aspect_Permissions(get=True, post=True, put=False, delete=False)
TTTT = Aspect_Permissions(get=True, post=True, put=True, delete=True)

default_consortium_permissions = Account_Permissions(
    datasets=Aspect_Permissions(get=True, post=True, put=False, delete=False), 
    harm_data_age=Aspect_Permissions(get=True, post=True, put=False, delete=False), 
    harm_data_locations=Aspect_Permissions(get=True, post=True, put=False, delete=False), 
    harm_data_records=Aspect_Permissions(get=True, post=True, put=False, delete=False), 
    harm_data_types=Aspect_Permissions(get=True, post=True, put=False, delete=False), 
    harm_data_species=Aspect_Permissions(get=True, post=True, put=False, delete=False), 
    harm_numerical=Aspect_Permissions(get=True, post=True, put=False, delete=False), 
    harm_reference=Aspect_Permissions(get=True, post=True, put=False, delete=False), 
    harm_timeslice=Aspect_Permissions(get=True, post=True, put=False, delete=False), 
    link_git=Aspect_Permissions(get=True, post=True, put=False, delete=False), 
    age_models=TTFF,
    data_frequency=TTFF,
    seasonality=TTFF, 
    season=TTFF,
    time_coverage=TTFF
)

public_view = Account_Permissions(
    datasets=Aspect_Permissions(get=True, post=False, put=False, delete=False), 
    harm_data_age=Aspect_Permissions(get=True, post=False, put=False, delete=False), 
    harm_data_locations=Aspect_Permissions(get=True, post=False, put=False, delete=False), 
    harm_data_records=Aspect_Permissions(get=True, post=False, put=False, delete=False), 
    harm_data_types=Aspect_Permissions(get=True, post=False, put=False, delete=False), 
    harm_data_species=Aspect_Permissions(get=True, post=False, put=False, delete=False), 
    harm_numerical=Aspect_Permissions(get=True, post=False, put=False, delete=False), 
    harm_reference=Aspect_Permissions(get=True, post=False, put=False, delete=False), 
    harm_timeslice=Aspect_Permissions(get=True, post=False, put=False, delete=False), 
    link_git=Aspect_Permissions(get=True, post=False, put=False, delete=False),
    age_models=TFFF,
    data_frequency=TFFF,
    seasonality=TFFF, 
    season=TFFF,
    time_coverage=TFFF 
)

super_user = Account_Permissions(
    datasets=Aspect_Permissions(get=True, post=True, put=True, delete=True), 
    harm_data_age=Aspect_Permissions(get=True, post=True, put=True, delete=True), 
    harm_data_locations=Aspect_Permissions(get=True, post=True, put=True, delete=True), 
    harm_data_records=Aspect_Permissions(get=True, post=True, put=True, delete=True), 
    harm_data_types=Aspect_Permissions(get=True, post=True, put=True, delete=True), 
    harm_data_species=Aspect_Permissions(get=True, post=True, put=True, delete=True), 
    harm_numerical=Aspect_Permissions(get=True, post=True, put=True, delete=True), 
    harm_reference=Aspect_Permissions(get=True, post=True, put=True, delete=True), 
    harm_timeslice=Aspect_Permissions(get=True, post=True, put=True, delete=True), 
    link_git=Aspect_Permissions(get=True, post=True, put=True, delete=True), 
    age_models=TTTT,
    data_frequency=TTTT,
    seasonality=TTTT, 
    season=TTTT,
    time_coverage=TTTT
)