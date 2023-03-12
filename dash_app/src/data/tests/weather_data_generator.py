import random
from faker import Faker
from random import randint
from datetime import date, timedelta
from .. import fields

class FakeWeatherDataGenerator:

    def __init__(
                  self,
                  location_no=5,
                  timepoint_no=10,
                  cloudcover_range=(fields.Cloudcover.LOW_BOUND, fields.Cloudcover.HIGH_BOUND),
                  seeing_range=(fields.Seeing.LOW_BOUND, fields.Seeing.HIGH_BOUND),
                  transparency_range=(fields.Transparency.LOW_BOUND, fields.Transparency.HIGH_BOUND),
                  lifted_index_range=(fields.LiftedIndex.VALUES.value),
                  rh2m_range=(fields.Rh2m.LOW_BOUND, fields.Rh2m.HIGH_BOUND),
                  temp2m_range=(fields.Temp2m.LOW_BOUND, fields.Temp2m.HIGH_BOUND),
                  prec_types=list(fields.Prec),
                  wind10m_directions=list(fields.WindDirection),
                  wind10m_speed_range=(fields.WindSpeed.LOW_BOUND, fields.WindSpeed.HIGH_BOUND)
                  ):
        self.fake = Faker('en_US')
        self.location_no = location_no
        self.timepoint_no = timepoint_no
        self.tomorrow = date.today() + timedelta(days=1)
        self.three_days_from_now = date.today() + timedelta(days=3)
        self.locations = [self.fake.unique.city() for _ in range(self.location_no)]
        self.timepoints = sorted([self.fake.unique.date_time_between(start_date=self.tomorrow,
                                                               end_date=self.three_days_from_now) 
                           for _ in range(self.timepoint_no)])
        self.cloudcover_range = cloudcover_range
        self.seeing_range = seeing_range
        self.transparency_range = transparency_range
        self.lifted_index_range = lifted_index_range
        self.rh2m_range = rh2m_range
        self.temp2m_range = temp2m_range
        self.prec_types = prec_types
        self.wind10m_directions = wind10m_directions
        self.wind10m_speed_range = wind10m_speed_range


    def produce_data(self):

        def _produce_random_measures(location, timepoint):
            cloudcover = randint(*self.cloudcover_range)
            seeing = randint(*self.seeing_range)
            transparency = randint(*self.transparency_range)
            lifted_index = random.choice(self.lifted_index_range)
            rh2m = randint(*self.rh2m_range)
            temp2m = randint(*self.temp2m_range)
            prec_type = random.choice(self.prec_types).value
            wind10m_direction = random.choice(self.wind10m_directions).value
            wind10m_speed = randint(*self.wind10m_speed_range)

            return [location, timepoint, cloudcover, seeing, transparency, lifted_index, rh2m,
                     temp2m, prec_type, wind10m_direction, wind10m_speed]

        return [_produce_random_measures(location=location, timepoint=timepoint)
                  for location in self.locations
                  for timepoint in self.timepoints]
    