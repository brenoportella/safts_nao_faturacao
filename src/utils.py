from src.defines import *
from selenium.common.exceptions import WebDriverException
from src.log_config import logger
import datetime
import os
import time

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

def get_month_abbr(month_input):
    """
    Converte qualquer variação de mês para a abreviação do Portal das Finanças.
    Ex: 'Janeiro' ou 'jan' -> 'Jan'
    """
    m = str(month_input).lower().strip()
    months_map = {
        'jan': 'Jan', 'fev': 'Fev', 'mar': 'Mar', 'abr': 'Abr',
        'mai': 'Mai', 'jun': 'Jun', 'jul': 'Jul', 'ago': 'Ago',
        'set': 'Set', 'out': 'Out', 'nov': 'Nov', 'dez': 'Dez'
    }
    # Pega os 3 primeiros caracteres (jan, fev...) e busca no mapa
    return months_map.get(m[:3], m.capitalize())

# def loop_function(function, check_success=None):
#     for attempt in range(NUMBER_ATTEMPT):
#         try:
#             function()
#             if not check_success or check_success():
#                 break
#         except WebDriverException as e:
#             logger.error(f"Error on {attempt + 1} try: {str(e)}")
#     else:
#         logger.info(f"All the tries failled. Check the error and try again.")

def loop_function(driver, function, check_success=None): # Adicionei o driver aqui
    for attempt in range(NUMBER_ATTEMPT):
        try:
            function()
            if not check_success or check_success():
                break
        except Exception as e:
            # Cria uma pasta para os erros se não existir
            if not os.path.exists("error_screenshots"):
                os.makedirs("error_screenshots")
            
            # Tira print com timestamp e erro
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"error_screenshots/error_attempt_{attempt + 1}_{timestamp}.png"
            driver.save_screenshot(filename)
            
            logger.error(f"Error on {attempt + 1} try: {str(e)}. Screenshot saved to {filename}")
            
            # Se falhar a tentativa, às vezes é bom dar um Refresh ou Back para resetar o estado
            # driver.refresh() 
            time.sleep(2)
    else:
        logger.info(f"All the tries failed. Check the screenshots and try again.")