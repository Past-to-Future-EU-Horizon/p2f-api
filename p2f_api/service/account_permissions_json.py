# Third Party Imports
from pydantic import BaseModel

# class Aspect_Permissions(BaseModel):
#     # Setting all to False as deny by default principle
#     get: bool=False
#     post: bool=False
#     put: bool=False
#     delete: bool=False

class Account_Permissions(BaseModel):
    # web/age_model.py
    agemodel_list: bool = False
    agemodel_get: bool = False
    agemodel_create: bool = False
    agemodel_delete: bool = False
    agemodel_dataset_assign: bool = False
    agemodel_dataset_remove: bool = False
    agemodel_recordhash_assign: bool = False
    agemodel_recordhash_remove: bool = False
    # web/datasets.py
    dataset_list: bool = False
    dataset_get: bool = False
    dataset_create: bool = False
    dataset_update: bool = False
    dataset_delete: bool = False
    # web/dq_comment.py
    comment_list: bool = False
    comment_create: bool = False
    comment_update: bool = False
    comment_delete: bool = False
    # web/harm_age.py
    age_list: bool = False
    age_get: bool = False
    age_create: bool = False
    age_update: bool = False
    age_delete: bool = False
    # web/harm_data_record
    record_list: bool = False
    record_get: bool = False
    record_create: bool = False
    record_delete: bool = False
    # web/harm_data_type
    datatype_list: bool = False
    datatype_get: bool = False
    datatype_create: bool = False
    datatype_delete: bool = False
    datatype_assign: bool = False
    datatype_remove: bool = False
    # web/harm_ds_freq.py
    datafrequency_get: bool = False
    datafrequency_create: bool = False
    datafrequency_delete: bool = False
    # web/harm_ds_timecov.py
    timecoverage_get: bool = False
    timecoverage_create: bool = False
    timecoverage_delete: bool = False
    # web/harm_location.py
    location_list: bool = False
    location_get: bool = False
    location_create: bool = False
    location_update: bool = False
    location_delete: bool = False
    location_recordhash_assign: bool = False
    location_recordhash_remove: bool = False
    # web/harm_numerical
    numeric_list: bool = False
    numeric_get: bool = False
    numeric_create: bool = False
    numeric_update: bool = False
    numeric_delete: bool = False
    # web/harm_reference.py
    reference_list: bool = False
    reference_get: bool = False
    reference_create: bool = False
    reference_delete: bool = False
    reference_recordhash_assign: bool = False
    reference_recordhash_remove: bool = False
    reference_dataset_assign: bool = False
    reference_dataset_remove: bool = False
    # web/harm_species.py
    species_list: bool = False
    species_get: bool = False
    species_create: bool = False
    species_delete: bool = False
    species_recordhash_assign: bool = False
    species_recordhash_remove: bool = False
    # web/harm_timeslice.py
    timeslices_list: bool = False
    timeslice_get: bool = False
    timeslice_create: bool = False
    timeslice_update: bool = False
    timeslice_delete: bool = False
    timeslice_recordhash_assign: bool = False
    timeslice_recordhash_remove: bool = False
    timeslice_dataset_assign: bool = False
    timeslice_dataset_remove: bool = False
    # web/keywords.py
    keywords_list: bool = False
    dictionary_list: bool = False
    taxonomies_list: bool = False
    dictionary_get: bool = False
    dataset_keyword_create: bool = False
    dataset_keyword_delete: bool = False
    dictionary_dataset_assign: bool = False
    dictionary_dataset_remove: bool = False
    # web/link_git.py
    git_list: bool = False
    git_get: bool = False
    git_create: bool = False
    git_delete: bool = False
    git_dataset_assign: bool = False
    git_dataset_remove: bool = False
    # web/seasonality.py
    seasonality_get: bool = False
    season_get: bool = False
    seasonality_create: bool = False
    season_create: bool = False
    seasonality_delete: bool = False
    season_delete: bool = False
    # web/temp_accounts.py
    data_upload_check: bool = False

# List only permissions that need to be set to true
default_consortium_permissions = Account_Permissions(
    ## web/age_model.py
    agemodel_list=True,
    agemodel_get=True,
    agemodel_create=True,
    # agemodel_delete=True,
    agemodel_dataset_assign=True,
    agemodel_dataset_remove=True,
    agemodel_recordhash_assign=True,
    agemodel_recordhash_remove=True,
    ## web/datasets.py
    dataset_list=True,
    dataset_get=True,
    dataset_create=True,
    dataset_update=True,
    # dataset_delete=True,
    ## web/dq_comment.py
    comment_list=True,
    comment_create=True,
    comment_update=True,
    comment_delete=True,
    ## web/harm_age.py
    age_list=True,
    age_get=True,
    age_create=True,
    age_update=True,
    # age_delete=True,
    ## web/harm_data_record
    record_list=True,
    record_get=True,
    record_create=True,
    record_delete=True,
    ## web/harm_data_type
    datatype_list=True,
    datatype_get=True,
    datatype_create=True,
    # datatype_delete=True,
    datatype_assign=True,
    datatype_remove=True,
    ## web/harm_ds_freq.py
    datafrequency_get=True,
    datafrequency_create=True,
    # datafrequency_delete=True,
    ## web/harm_ds_timecov.py
    timecoverage_get=True,
    timecoverage_create=True,
    # timecoverage_delete=True,
    ## web/harm_location.py
    location_list=True,
    location_get=True,
    location_create=True,
    location_update=True,
    # location_delete=True,
    location_recordhash_assign=True,
    location_recordhash_remove=True,
    ## web/harm_numerical
    numeric_list=True,
    numeric_get=True,
    numeric_create=True,
    numeric_update=True,
    # numeric_delete=True,
    ## web/harm_reference.py
    reference_list=True,
    reference_get=True,
    reference_create=True,
    # reference_delete=True,
    reference_recordhash_assign=True,
    reference_recordhash_remove=True,
    reference_dataset_assign=True,
    reference_dataset_remove=True,
    ## web/harm_species.py
    species_list=True,
    species_get=True,
    species_create=True,
    # species_delete=True,
    species_recordhash_assign=True,
    species_recordhash_remove=True,
    ## web/harm_timeslice.py
    timeslices_list=True,
    timeslice_get=True,
    timeslice_create=True,
    timeslice_update=True,
    # timeslice_delete=True,
    timeslice_recordhash_assign=True,
    timeslice_recordhash_remove=True,
    timeslice_dataset_assign=True,
    timeslice_dataset_remove=True,
    ## web/keywords.py
    keywords_list=True,
    dictionary_list=True,
    taxonomies_list=True,
    dictionary_get=True,
    dataset_keyword_create=True,
    # dataset_keyword_delete=True,
    dictionary_dataset_assign=True,
    dictionary_dataset_remove=True,
    ## web/link_git.py
    git_list=True,
    git_get=True,
    git_create=True,
    # git_delete=True,
    git_dataset_assign=True,
    git_dataset_remove=True,
    ## web/seasonality.py
    seasonality_get=True,
    season_get=True,
    seasonality_create=True,
    season_create=True,
    seasonality_delete=True,
    season_delete=True,
    ## web/temp_accounts.py
    data_upload_check=True,
)

public_view = Account_Permissions(
# web/age_model.py
    agemodel_list=True,
    agemodel_get=True,
    # web/datasets.py
    dataset_list=True,
    dataset_get=True,
    # web/dq_comment.py
    # comment_list=True,
    # web/harm_age.py
    age_list=True,
    age_get=True,
    # web/harm_data_record
    record_list=True,
    record_get=True,
    # web/harm_data_type
    datatype_list=True,
    datatype_get=True,
    # web/harm_ds_freq.py
    datafrequency_get=True,
    # web/harm_ds_timecov.py
    timecoverage_get=True,
    # web/harm_location.py
    location_list=True,
    location_get=True,
    # web/harm_numerical
    numeric_list=True,
    numeric_get=True,
    # web/harm_reference.py
    reference_list=True,
    reference_get=True,
    # web/harm_species.py
    species_list=True,
    species_get=True,
    # web/harm_timeslice.py
    timeslices_list=True,
    timeslice_get=True,
    # web/keywords.py
    keywords_list=True,
    dictionary_list=True,
    taxonomies_list=True,
    dictionary_get=True,
    # web/link_git.py
    git_list=True,
    git_get=True,
    # web/seasonality.py
    seasonality_get=True,
    season_get=True,
)

super_user = Account_Permissions(
    # web/age_model.py
    agemodel_list=True,
    agemodel_get=True,
    agemodel_create=True,
    agemodel_delete=True,
    agemodel_dataset_assign=True,
    agemodel_dataset_remove=True,
    agemodel_recordhash_assign=True,
    agemodel_recordhash_remove=True,
    # web/datasets.py
    dataset_list=True,
    dataset_get=True,
    dataset_create=True,
    dataset_update=True,
    dataset_delete=True,
    # web/dq_comment.py
    comment_list=True,
    comment_create=True,
    comment_update=True,
    comment_delete=True,
    # web/harm_age.py
    age_list=True,
    age_get=True,
    age_create=True,
    age_update=True,
    age_delete=True,
    # web/harm_data_record
    record_list=True,
    record_get=True,
    record_create=True,
    record_delete=True,
    # web/harm_data_type
    datatype_list=True,
    datatype_get=True,
    datatype_create=True,
    datatype_delete=True,
    datatype_assign=True,
    datatype_remove=True,
    # web/harm_ds_freq.py
    datafrequency_get=True,
    datafrequency_create=True,
    datafrequency_delete=True,
    # web/harm_ds_timecov.py
    timecoverage_get=True,
    timecoverage_create=True,
    timecoverage_delete=True,
    # web/harm_location.py
    location_list=True,
    location_get=True,
    location_create=True,
    location_update=True,
    location_delete=True,
    location_recordhash_assign=True,
    location_recordhash_remove=True,
    # web/harm_numerical
    numeric_list=True,
    numeric_get=True,
    numeric_create=True,
    numeric_update=True,
    numeric_delete=True,
    # web/harm_reference.py
    reference_list=True,
    reference_get=True,
    reference_create=True,
    reference_delete=True,
    reference_recordhash_assign=True,
    reference_recordhash_remove=True,
    reference_dataset_assign=True,
    reference_dataset_remove=True,
    # web/harm_species.py
    species_list=True,
    species_get=True,
    species_create=True,
    species_delete=True,
    species_recordhash_assign=True,
    species_recordhash_remove=True,
    # web/harm_timeslice.py
    timeslices_list=True,
    timeslice_get=True,
    timeslice_create=True,
    timeslice_update=True,
    timeslice_delete=True,
    timeslice_recordhash_assign=True,
    timeslice_recordhash_remove=True,
    timeslice_dataset_assign=True,
    timeslice_dataset_remove=True,
    # web/keywords.py
    keywords_list=True,
    dictionary_list=True,
    taxonomies_list=True,
    dictionary_get=True,
    dataset_keyword_create=True,
    dataset_keyword_delete=True,
    dictionary_dataset_assign=True,
    dictionary_dataset_remove=True,
    # web/link_git.py
    git_list=True,
    git_get=True,
    git_create=True,
    git_delete=True,
    git_dataset_assign=True,
    git_dataset_remove=True,
    # web/seasonality.py
    seasonality_get=True,
    season_get=True,
    seasonality_create=True,
    season_create=True,
    seasonality_delete=True,
    season_delete=True,
    # web/temp_accounts.py
    data_upload_check=True,
)