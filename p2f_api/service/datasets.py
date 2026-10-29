# Batteries included libraries
from typing import List, Optional
from inspect import stack
from io import BytesIO
import uuid

# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
from sqlalchemy import union
from fastapi.responses import Response

# Local libraries
from p2f_api.apilogs import logger, fa
from ..data.db_connection import engine
from ..data.datasets import datasets
from ..data.harm_data_record import harm_data_record
from ..data.harm_locations import harm_locations, harm_location_to_rec
from ..data.harm_core import coreSegment, coreSegment_to_record
from ..data.harm_data_types import harm_data_type
from ..data.harm_data_numerical import harmonized_int, harmonized_int_confidence
from ..data.harm_data_numerical import harmonized_float, harmonized_float_confidence
from service import shared_execution
from p2f_pydantic.datasets import Datasets

def list_datasets(
    is_new_p2f: Optional[bool] = None,
    is_sub_dataset: Optional[bool] = None,
    doi: Optional[str] = None,
    location_id: Optional[uuid] = None,
    datatype_id: Optional[uuid] = None,
    core_id: Optional[uuid] = None,
    core_segment_id: Optional[uuid] = None,
    output_format: shared_execution.mimes = "application/json",
    ) -> List[Datasets] | Response:
    logger.debug(f"{fa.service}{fa.list} {stack()[0][3]}()")
    with Session(engine) as session:
        logger.debug("•  Created session")
        # logger.debug(f"Parameters: {is_new_p2f}, {is_sub_dataset}, {doi}")
        stmt = select(datasets)
        if is_new_p2f is not None:
            stmt = stmt.where(datasets.is_new_p2f == is_new_p2f)
        if is_sub_dataset is not None:
            stmt = stmt.where(datasets.is_sub_dataset == is_sub_dataset)
        if doi is not None:
            stmt = stmt.where(datasets.doi == doi)
        if location_id is not None:
            loc_to_rechash_subqry = select(harm_location_to_rec.fk_data_record).distinct()
            loc_to_rechash_subqry = loc_to_rechash_subqry.where(harm_location_to_rec.fk_harm_location == location_id)
            rechash_to_dataset_subqry = select(harm_data_record.fk_dataset).distinct()
            rechash_to_dataset_subqry = rechash_to_dataset_subqry.where(harm_data_record.record_hash.in_(loc_to_rechash_subqry))
            stmt = stmt.where(datasets.dataset_id.in_(rechash_to_dataset_subqry))
        if datatype_id is not None:
            subqry_i_rec = select(harmonized_int.fk_data_record).distinct().where(harmonized_int.fk_data_type == datatype_id)
            subqry_ic_rec = select(harmonized_int_confidence.fk_data_record).distinct().where(harmonized_int_confidence.fk_data_type == datatype_id)
            subqry_f_rec = select(harmonized_float.fk_data_record).distinct().where(harmonized_float.fk_data_type == datatype_id)
            subqry_fc_rec = select(harmonized_float_confidence.fk_data_record).distinct().where(harmonized_float_confidence.fk_data_type == datatype_id)
            # group them up
            subqry_union_rec = union(subqry_i_rec, subqry_ic_rec, subqry_f_rec, subqry_fc_rec)
            # grab the datasets
            rechash_to_dataset_subqry_dt = select(harm_data_record.fk_dataset).distinct()
            rechash_to_dataset_subqry_dt = rechash_to_dataset_subqry_dt.where(harm_data_record.record_hash.in_(subqry_union_rec))
            stmt = stmt.where(datasets.dataset_id.in_(rechash_to_dataset_subqry_dt))
        if core_id is not None:
            # Select core segments with the core_id
            core_to_coreseg_subqry = select(coreSegment.core_segment_id).distinct()
            core_to_coreseg_subqry = core_to_coreseg_subqry.where(coreSegment.fk_core_id == core_id)
            # Select from the rec_hash with the coreseg_ids
            coreseg_to_rechash_subqury = select(coreSegment_to_record.fk_record_hash).distinct()
            coreseg_to_rechash_subqury = coreseg_to_rechash_subqury.where(coreSegment_to_record.fk_core_segment_id.in_(core_to_coreseg_subqry))
            # Select the dataset_ids using the rec_hashes
            rechash_to_dataset_subqry_core = select(harm_data_record.fk_dataset).distinct()
            rechash_to_dataset_subqry_core = rechash_to_dataset_subqry_core.where(harm_data_record.record_hash.in_(coreseg_to_rechash_subqury))
            stmt = stmt.where(datasets.dataset_id.in_(rechash_to_dataset_subqry_core))
        if core_segment_id is not None:
            coreseg_to_rechash_subqury_coreseg = select(coreSegment_to_record.fk_record_hash).distinct()
            coreseg_to_rechash_subqury_coreseg = coreseg_to_rechash_subqury_coreseg.where(coreSegment_to_record.fk_core_segment_id == core_segment_id)
            rechash_to_dataset_subqry_coreseg = select(harm_data_record.fk_dataset).distinct()
            rechash_to_dataset_subqry_coreseg = rechash_to_dataset_subqry_coreseg.where(harm_data_record.record_hash.in_(coreseg_to_rechash_subqury_coreseg))
            stmt = stmt.where(datasets.dataset_id.in_(rechash_to_dataset_subqry_coreseg))
        results = shared_execution.list(stmt=stmt,
                                        pydantic_object=Datasets,
                                        session_object=session,
                                        output_format=output_format)
        logger.debug(f"•  Found {len(results)} results")
    return results


def get_dataset(dataset_id: Optional[uuid.UUID]=None,
                output_format: shared_execution.mimes = "application/json", 
                pk_datasets=None) -> Datasets | Response:
    logger.debug(f"{fa.service}{fa.get} {stack()[0][3]}()")
    with Session(engine) as session:
        logger.debug("•  Created session")
        stmt = select(datasets)
        if dataset_id is not None:
            stmt = stmt.where(datasets.dataset_id == dataset_id)
        if pk_datasets is not None:
            stmt = stmt.where(datasets.pk_datasets == pk_datasets)
        result = shared_execution.get(stmt=stmt,
                                      pydantic_object=Datasets,
                                      session_object=session,
                                      output_format=output_format)
    return result


def create_dataset(new_dataset: Datasets,
                   output_format: shared_execution.mimes = "application/json",) -> Datasets:
    logger.debug(f"{fa.service}{fa.create} {stack()[0][3]}()")
    # logger.debug(f"•  received: {new_dataset}")
    if new_dataset.dataset_id is None:
        new_dataset.dataset_id = uuid.uuid4()
    else:
        if get_dataset(dataset_id=new_dataset.dataset_id) is not None:
            new_dataset.dataset_id = uuid.uuid4()
    with Session(engine) as session:
        logger.debug("•  Created session")
        stmt = insert(datasets)
        stmt = stmt.values(**new_dataset.model_dump(exclude_unset=True))
        logger.debug(f"•  statement: {stmt}")
        inserted_pk = shared_execution.create(stmt=stmt,
                                              session_object=session)
        logger.debug("•  Executed and Commited")
    return get_dataset(pk_datasets=inserted_pk, 
                       output_format=output_format)


def update_dataset(dataset_update: Datasets,
                   output_format: shared_execution.mimes = "application/json",) -> Datasets:
    logger.debug(f"{fa.service}{fa.update} {stack()[0][3]}()")
    with Session(engine) as session:
        logger.debug("•  Created session")
        stmt = update(datasets)
        stmt = stmt.where(
            datasets.dataset_id == dataset_update.dataset_id
        )
        stmt = stmt.values(**dataset_update.model_dump(exclude_unset=True))
        execute = session.execute(stmt)
        commit = session.commit()
    return get_dataset(dataset_id=dataset_update.dataset_id,
                       output_format=output_format)


def delete_dataset(dataset_id,
                   output_format: shared_execution.mimes = "application/json",) -> None:
    logger.debug(f"{fa.service}{fa.delete} {stack()[0][3]}()")
    with Session(engine) as session:
        logger.debug("•  Created session")
        stmt = delete(datasets).where(datasets.dataset_id == dataset_id)
        return shared_execution.delete(stmt=stmt,
                                       session_object=session)
