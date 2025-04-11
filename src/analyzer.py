# BASIC THE BRAIN OF THE PROGRAM

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
            logger.error(f"ERRO: Não foi possível ler o arquivo excel. Verifique se o nome da folha foi escrito corretamente. Se a sua estrutura está correta. Consulte o Guia para mais informações.\n{e}")
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
                    logger.info(f"Senha Errada: {row['Login']}")
                    disconnect(driver)
                    logger.info(counter)
                    continue
                if expired_password(driver):
                    counter += 1
                    df_principal.at[index, 'Obs'] = "Senha Expirada"
                    save_to_excel(df_principal, counter, row['Mes'], row['Ano'])
                    logger.info(f"Senha Expirada: {row['Login']}")
                    disconnect(driver)
                    logger.info(counter)
                    continue
                
                loop_function(lambda: consult_comunication(driver, row['Ano'], convert_month(row['Mes'])))
                if no_results_consult(driver):
                    counter += 1
                    df_principal.at[index, 'C. Previa'] = "SIM"
                    save_to_excel(df_principal, counter, row['Mes'], row['Ano'])
                    logger.info(f"Comunicação Prévia: {row['Login']}")
                    disconnect(driver)
                    logger.info(counter)
                    continue
                driver.back()

                loop_function(lambda: consult_files(driver, row['Ano'], row['Mes']))
                if no_files_consult(driver):
                    counter += 1
                    df_principal.at[index, 'Ficheiro S'] = "SIM"
                    save_to_excel(df_principal, counter, row['Mes'], row['Ano'])
                    logger.info(f"Possui ficheiro S.: {row['Login']}")
                    disconnect(driver)
                    logger.info(counter)
                    continue
                driver.back()

                loop_function(lambda: billing_abscence(driver, row['Ano'], row['Mes']))
                logger.info(f"Saft n. faturacao comunicado {row['Login']}")
                df_principal.at[index, 'Com. N. Fat.'] = "SIM"
                counter += 1
                save_to_excel(df_principal, counter, row['Mes'], row['Ano'])
                logger.info(counter)
                disconnect(driver)
            
        except Exception as e:
            logger.error(f"Erro inesperado durante a execução: {e}")
            df_principal.to_excel(f"backup_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx", index=False)
            logger.info("Backup automático salvo após erro.")
        finally:
            month = year = "final"
            if(driver):
                driver_quit(driver)
                save_to_excel(df_principal, counter, month, year)
        logger.info("Sucesso\nProcesso de submissão de SAFTs de não faturação concluído!")