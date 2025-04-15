from src.login import *
from src.consults import *
from src.utils import *
from src.driver import driver_quit
from src.save_excel import save_to_excel
from src.log_config import logger

import datetime

import pandas as pd

def analyzer(driver, file_entry):
        try:
            df_principal = pd.read_excel(file_entry)
        except Exception as e:
            logger.error(f"ERRO: It could not read the xlsx file. Check if the structure are corret, see in readme.md.\n{e}")
            return

        columns_to_convert = ['Obs', 'C. Previa', 'Ficheiro S', 'Com. N. Fat.']

        for column in columns_to_convert:
            if df_principal[column].dtype != 'object':
                df_principal[column] = df_principal[column].astype('object')
        
        counter = 0
        try:
            for index, row in df_principal.iterrows():
                
                login(driver, row['Login'], row['Senha'])

                if wrong_password(driver):
                    counter += 1
                    df_principal.at[index, 'Obs'] = "Senha Incorreta"
                    save_to_excel(df_principal, counter, row['Mes'], row['Ano'])
                    logger.info(f"Wrong password: {row['Login']}")
                    disconnect(driver)
                    logger.info(counter)
                    continue
                if expired_password(driver):
                    counter += 1
                    df_principal.at[index, 'Obs'] = "Senha Expirada"
                    save_to_excel(df_principal, counter, row['Mes'], row['Ano'])
                    logger.info(f"Expired password: {row['Login']}")
                    disconnect(driver)
                    logger.info(counter)
                    continue
                
                loop_function(lambda: consult_comunication(driver, row['Ano'], convert_month(row['Mes'])))
                if no_results_consult(driver):
                    counter += 1
                    df_principal.at[index, 'C. Previa'] = "SIM"
                    save_to_excel(df_principal, counter, row['Mes'], row['Ano'])
                    logger.info(f"Have previous comunication: {row['Login']}")
                    disconnect(driver)
                    logger.info(counter)
                    continue
                driver.back()

                loop_function(lambda: consult_files(driver, row['Ano'], row['Mes']))
                if no_files_consult(driver):
                    counter += 1
                    df_principal.at[index, 'Ficheiro S'] = "SIM"
                    save_to_excel(df_principal, counter, row['Mes'], row['Ano'])
                    logger.info(f"Have saft file: {row['Login']}")
                    disconnect(driver)
                    logger.info(counter)
                    continue
                driver.back()

                loop_function(lambda: billing_abscence(driver, row['Ano'], row['Mes']))
                logger.info(f"Saft n. billing comunicated {row['Login']}")
                df_principal.at[index, 'Com. N. Fat.'] = "SIM"
                counter += 1
                save_to_excel(df_principal, counter, row['Mes'], row['Ano'])
                logger.info(counter)
                disconnect(driver)
            
        except Exception as e:
            logger.error(f"Unexpected error during execution: {e}")
            df_principal.to_excel(f"backup_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx", index=False)
            logger.info("Backup automatic was save after the error.")
        finally:
            month = year = "final"
            if(driver):
                driver_quit(driver)
                save_to_excel(df_principal, counter, month, year)
        logger.info("Success\nSAFT non-billing submission process has finished.")