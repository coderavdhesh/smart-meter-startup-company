from functools import reduce

from ..repository.price_plan_repository import price_plan_repository
from .electricity_reading_service import ElectricityReadingService
from ..utils.time_converter import time_elapsed_in_hours


def calculate_time_elapsed(readings):
    min_time = min(map(lambda r: r.time, readings))
    max_time = max(map(lambda r: r.time, readings))
    elapsed = time_elapsed_in_hours(min_time, max_time)

    return elapsed if elapsed>0 else 1

class PricePlanService:
    def __init__(self, reading_repository):
        self.electricity_reading_service = ElectricityReadingService(reading_repository)

    def get_list_of_spend_against_each_price_plan_for(self, smart_meter_id, limit=None) -> list:

        """This fucntion is getting the price plans for a given smart meter ID."""

        readings = self.electricity_reading_service.retrieve_readings_for(smart_meter_id)
        if len(readings) < 1:
            return []
        
        average = self.calculate_average_reading(readings)
        time_elapsed = calculate_time_elapsed(readings)
        consumed_energy = average / time_elapsed

        price_plans = price_plan_repository.get()

        def _cost_from_plan(price_plan):
            cost = {}
            cost[price_plan.name] = consumed_energy * price_plan.unit_rate
            return cost

        list_of_spend = list(map(_cost_from_plan, self.cheapest_plans_first(price_plans)))

        return list_of_spend[:limit]

    def cheapest_plans_first(self, price_plans):
        return list(sorted(price_plans, key=lambda plan: plan.unit_rate))

    def calculate_average_reading(self, readings):
        sum = reduce((lambda p, c: p + c), map(lambda r: r.reading, readings), 0)
        return sum / len(readings)
