from enum import Enum


class Aggregator(Enum):
    DAY = 'date'
    HOUR = 'hour'
    MONTH = 'month'