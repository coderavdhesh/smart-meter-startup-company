from http import HTTPStatus
from typing import List
from loguru import logger
import json
from fastapi import APIRouter, HTTPException, Path

from slowapi import Limiter
from slowapi.util import get_remote_address

from ..repository.electricity_reading_repository import ElectricityReadingRepository
from ..service.electricity_reading_service import ElectricityReadingService
from ..domain.models import OPENAPI_EXAMPLES, ElectricReading, Readings

repository = ElectricityReadingRepository()
service = ElectricityReadingService(repository)

router = APIRouter(prefix="/readings", tags=["Readings"])


@router.post(
    "/store",
    response_model=ElectricReading,
    description="Store Readings",
)
def store(data: ElectricReading):
    # handle the exception
    logger.info("Storing the reading {data} in the memory of the electricity_reading_repo", data = data)
    try:
        service.store_reading(data.model_dump(mode="json"))
        logger.success("The reading {} strored successfully", data)
        return data
    except Exception as e:
        # Handle general errors
        logger.error("Error storing reading: {error}", error=str(e))
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")
    


@router.get(
    "/read/{smart_meter_id}",
    response_model=List[Readings],
    description="Get Stored Readings",
)
def read(smart_meter_id: str = Path(openapi_examples=OPENAPI_EXAMPLES)):
    logger.info("Fetching readings for meter: {meter_id}", meter_id=smart_meter_id)
    try:
        if not smart_meter_id or smart_meter_id.strip() == "":
            logger.error("Smart meter ID is required but not provided")
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Smart meter ID is required")
        
        if smart_meter_id not in repository.get_all_smart_meter_ids():
            logger.error("Smart meter ID {meter_id} does not exist", meter_id=smart_meter_id)
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Smart meter ID does not exist")
        
        readings = service.retrieve_readings_for(smart_meter_id)
        if not readings:
            logger.warning("No readings found for meter: {meter_id}", meter_id=smart_meter_id)
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No readings found")
        else:
            all_readings = [r.to_json() for r in readings]
            logger.info("Fetched readings are : {all_readings}", all_readings=json.dumps(all_readings) )
            return all_readings
    except Exception as e:
        # logger.error(f"Error retrieving readings: {str(e)}")
        logger.error("Error retrieving readings for meter: {meter_id}, error: {error}", meter_id=smart_meter_id, error=str(e))
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")
