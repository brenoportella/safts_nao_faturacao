from src.defines import *
from selenium.common.exceptions import WebDriverException
from src.log_config import logger

def convert_month(month):
     months = {
        'jan': '01',
        'fev': '02',
        'mar': '03',
        'abr': '04',
        'mai': '05',
        'jun': '06',
        'jul': '07',
        'ago': '08',
        'set': '09',
        'out': '10',
        'nov': '11',
        'dez': '12'
     }
     return months.get(month.lower())

def loop_function(function):
    for attempt in range(NUMBER_ATTEMPT):
        try:
            function()
            break
        except WebDriverException as e:
            logger.error(f"Error on {attempt + 1} try: {str(e)}")
    else:
        logger.info(f"All the tries failled. Check the error and try again.")