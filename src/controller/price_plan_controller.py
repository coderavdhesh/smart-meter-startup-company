from http import HTTPStatus
from typing import Dict, List

from fastapi import APIRouter, HTTPException, Path, Query
from loguru import logger

from ..service.account_service import AccountService
from ..service.price_plan_service import PricePlanService
from .electricity_reading_controller import repository as readings_repository
from ..domain.models import OPENAPI_EXAMPLES, PricePlanComparisons

router = APIRouter(
    prefix="/price-plans",
    tags=["Price Plan Comparator Controller"],
)


@router.get(
    "/compare-all/{smart_meter_id}",
    response_model=PricePlanComparisons,
    description="Compare prices for all plans for a given meter",
)
def compare(smart_meter_id: str = Path(openapi_examples=OPENAPI_EXAMPLES)):

    """This controller is comparing the price plans for a given smart meter ID."""

    logger.info("Comapre the price plan for the meter ID: {smart_meter_id}", smart_meter_id=smart_meter_id)


    logger.info("Fetching price plan comparisons for meter: {smart_meter_id}", smart_meter_id=smart_meter_id)
    price_plan_service = PricePlanService(readings_repository)

    logger.info("Creating account service instance")
    account_service = AccountService()

    logger.info("Fetching list of spend against each price plan for meter: {smart_meter_id}", smart_meter_id=smart_meter_id)
    list_of_spend_against_price_plans = price_plan_service.get_list_of_spend_against_each_price_plan_for(smart_meter_id)

    if not account_service.has_meter(smart_meter_id):
        logger.warning("The smart meter {smart_meter_id} does not exist", smart_meter_id=smart_meter_id)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Smart meter {smart_meter_id} not found")
    
    if len(list_of_spend_against_price_plans) < 1:
        logger.warning("No price plans found for smart meter {smart_meter_id}", smart_meter_id=smart_meter_id)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"No price plans found for smart meter {smart_meter_id}")
    else:
        logger.success("Sucessfully, Price Plan comparisons for meter {smart_meter_id} are: {comparisons}")
        return {
            "pricePlanId": account_service.get_price_plan(smart_meter_id),
            "pricePlanComparisons": list_of_spend_against_price_plans,
        }


@router.get(
    "/recommend/{smart_meter_id}",
    response_model=List[Dict],
    description="View recommended price plans for usage",
)
def recommend(
    smart_meter_id: str = Path(openapi_examples=OPENAPI_EXAMPLES),
    limit: int = Query(description="Number of items to return", default=None),
):
    logger.info("Fetching the recomended price plans for the meter: {smart_meter_id}", smart_meter_id = smart_meter_id)

    price_plan_service = PricePlanService(readings_repository)
    list_of_spend_against_price_plans = price_plan_service.get_list_of_spend_against_each_price_plan_for(
        smart_meter_id, limit=limit
    )

    logger.success("Fetched the recommended price plans for meter {smart_meter_id} are: {plans}",
                   smart_meter_id=smart_meter_id,
                   plans=list_of_spend_against_price_plans)
    return list_of_spend_against_price_plans
