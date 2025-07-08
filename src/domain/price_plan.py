class PricePlan:
    def __init__(self, name, supplier, unit_rate, peak_time_multipliers=[]):
        self.name = name
        self.supplier = supplier
        self.unit_rate = unit_rate
        self.peak_time_multipliers = peak_time_multipliers

    # def get_price(self, date_time):
    #     matching_multipliers = [m for m in self.peak_time_multipliers if m.day_of_week == date_time.isoweekday()]
    #     return self.unit_rate * matching_multipliers[0].multiplier if len(matching_multipliers) else self.unit_rate
    
    def calculate_the_price_for_datetime(self, date_time):

        if not date_time:
            raise ValueError("date_time must be provided")
        
        target_day = date_time.isoweekday()
        price_multiplier_at_the_peak_time= self._get_price_multiplier_of_the_peak_time_for_the_date(target_day)

        return self.unit_rate * price_multiplier_at_the_peak_time
    
    def _get_price_multiplier_of_the_peak_time_for_the_day(self, target_day):
        price_multiplier = 1.0

        for peak_time_multiplier in self.peak_time_multipliers:
            if peak_time_multiplier.day_of_week == target_day:
                price_multiplier = peak_time_multiplier.multiplier
                break
        
        return price_multiplier

    class DayOfWeek:
        SUNDAY = 0
        MONDAY = 1
        TUESDAY = 2
        WEDNESDAY = 3
        THURSDAY = 4
        FRIDAY = 5
        SATURDAY = 6

    class PeakTimeMultiplier:
        def __init__(self, day_of_week, price_multiplier):
            self.day_of_week = day_of_week
            self.price_multiplier = price_multiplier
