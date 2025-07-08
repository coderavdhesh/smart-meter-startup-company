from http import HTTPStatus
from typing import List

from fastapi import APIRouter, HTTPException, Path, logger

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
    try:
        service.store_reading(data.model_dump(mode="json"))
        return data
    except Exception as e:
        # Handle general errors
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")
    

@router.get(
    "/read/{smart_meter_id}",
    response_model=List[Readings],
    description="Get Stored Readings",
)
def read(smart_meter_id: str = Path(openapi_examples=OPENAPI_EXAMPLES)):

    try:
        if not smart_meter_id or smart_meter_id.strip() == "":
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Smart meter ID is required")
        
        readings = service.retrieve_readings_for(smart_meter_id)
        if not readings:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No readings found")
        else:
            return [r.to_json() for r in readings]
    except Exception as e:
        # logger.error(f"Error retrieving readings: {str(e)}")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")
