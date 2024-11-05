# src/__init__.py
from .data_quality_checker import DataQualityChecker
from .utils.validators import check_nulls, check_duplicates, check_ranges

__version__ = '0.1.0'

__all__ = [
    'DataQualityChecker',
    'check_nulls',
    'check_duplicates',
    'check_ranges'
]
