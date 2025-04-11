from src.defines import *
from selenium.common.exceptions import WebDriverException

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
            print(f"Erro na tentativa {attempt + 1}: {str(e)}")
    else:
        print(f"Todas as tentativas falharam. Verifique o erro e tente novamente mais tarde.")