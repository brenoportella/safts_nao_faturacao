import os
import traceback
from datetime import datetime

import pandas as pd

from src.consults import *
from src.driver import driver_quit
from src.log_config import logger
from src.login import *
from src.save_excel import save_to_excel
from src.utils import *


def analyzer(driver, file_entry):
    logger.info("=== Analyzer iniciado ===")
    logger.info(f"Arquivo recebido: {file_entry}")
    logger.info(f"Driver inicial: {driver}")
    if not os.path.exists("results"):
        os.makedirs("results")

    try:
        df_principal = pd.read_excel(file_entry, dtype={"Login": str})
        df_principal.columns = df_principal.columns.str.strip()
        logger.info(f"Colunas do Excel: {df_principal.columns.tolist()}")
        logger.info(f"Primeiras linhas:\n{df_principal.head()}")
    except Exception as e:
        logger.error(f"ERRO: It could not read the xlsx file. Check structure.\n{e}")
        return

    columns_to_convert = ["Obs", "C. Previa", "Ficheiro S", "Com. N. Fat."]

    logger.info("Convertendo colunas object se necessário...")
    for column in columns_to_convert:
        logger.info(f"Coluna {column} -> tipo antes: {df_principal[column].dtype}")
        if df_principal[column].dtype != "object":
            df_principal[column] = df_principal[column].astype("object")
            logger.info(f"Coluna {column} convertida para object")

    counter = 0

    try:
        for index, row in df_principal.iterrows():
            time.sleep(1)
            logger.info("------------------------------------------------")
            logger.info(f"Processando linha {index}")
            print(row["Ano"], type(row["Ano"]))
            logger.info(
                f"Login: {row['Login']} | Senha: {row['Senha']} | Mes: {row['Mes']} | Ano: {row['Ano']}"
            )
            logger.info("Chamando login()...")

            login(driver, row["Login"], row["Senha"])

            logger.info("Login executado. Verificando comprimento da senha...")
            if len(str(row["Senha"])) < 8:
                logger.info("Senha curta detectada")
                counter += 1
                df_principal.at[index, "Obs"] = "Senha pequena invalida"
                save_to_excel(df_principal, counter, row["Mes"], row["Ano"])
                logger.info(f"Wrong password, too small: {row['Login']}")
                disconnect(driver)
                logger.info("Disconnect executado após senha curta")
                logger.info(f"Counter: {counter}")
                continue

            logger.info("Verificando wrong_password()...")
            if wrong_password(driver):
                logger.info("Senha incorreta detectada")
                counter += 1
                df_principal.at[index, "Obs"] = "Senha Incorreta"
                save_to_excel(df_principal, counter, row["Mes"], row["Ano"])
                logger.info(f"Wrong password: {row['Login']}")
                disconnect(driver)
                logger.info("Disconnect executado após senha incorreta")
                logger.info(f"Counter: {counter}")
                continue

            logger.info("Verificando expired_password()...")
            if expired_password(driver):
                logger.info("Senha expirada detectada")
                counter += 1
                df_principal.at[index, "Obs"] = "Senha Expirada"
                save_to_excel(df_principal, counter, row["Mes"], row["Ano"])
                logger.info(f"Expired password: {row['Login']}")
                disconnect(driver)
                logger.info("Disconnect executado após senha expirada")
                logger.info(f"Counter: {counter}")
                continue

            logger.info("Tirando screenshot após login.")
            driver.save_screenshot(f"screenshot_login_{row['Login']}.png")

            logger.info("Chamando consult_comunication() via loop_function...")
            ano = str(int(row["Ano"]))
            mes_number = convert_month(row["Mes"])
            loop_function(driver, lambda: consult_comunication(driver, ano, mes_number))

            logger.info("Verificando no_results_consult()...")
            if no_results_consult(driver):
                logger.info("Consult encontrou comunicação prévia")
                counter += 1
                df_principal.at[index, "C. Previa"] = "SIM"
                save_to_excel(df_principal, counter, row["Mes"], row["Ano"])
                logger.info(f"Have previous comunication: {row['Login']}")
                driver.save_screenshot(
                    f"results/screenshot_previous_comunication_{row['Login']}.png"
                )
                disconnect(driver)
                logger.info("Disconnect executado após comunicação prévia")
                logger.info(f"Counter: {counter}")
                continue

            logger.info("Voltando página após consult_comunication()")
            driver.back()

            logger.info("Chamando consult_files() via loop_function...")
            ano = str(int(row["Ano"]))
            mes = row["Mes"]
            loop_function(driver, lambda: consult_files(driver, ano, mes))

            logger.info("Verificando no_files_consult()...")
            if no_files_consult(driver):
                logger.info("Consult encontrou ficheiro SAFT")
                counter += 1
                df_principal.at[index, "Ficheiro S"] = "SIM"
                save_to_excel(df_principal, counter, row["Mes"], row["Ano"])
                logger.info(f"Have saft file: {row['Login']}")
                driver.save_screenshot(
                    f"results/screenshot_saft_file_{row['Login']}.png"
                )
                disconnect(driver)
                logger.info("Disconnect executado após ficheiro SAFT")
                logger.info(f"Counter: {counter}")
                continue

            logger.info("Voltando página após consult_files()")
            driver.back()

            logger.info("Chamando billing_abscence() via loop_function...")
            ano = str(int(row["Ano"]))
            mes = row["Mes"]
            loop_function(driver, lambda: billing_abscence(driver, ano, mes))

            logger.info(f"Saft n. billing comunicated {row['Login']}")
            driver.save_screenshot(
                f"results/screenshot_billing_abscence_comunication_{row['Login']}.png"
            )
            df_principal.at[index, "Com. N. Fat."] = "SIM"
            counter += 1
            save_to_excel(df_principal, counter, row["Mes"], row["Ano"])
            logger.info("billing_abscence() completo")
            logger.info(f"Counter: {counter}")

            disconnect(driver)
            logger.info("Disconnect executado ao final do ciclo do login atual")
            time.sleep(2)

    except Exception as e:
        logger.error("Unexpected error during execution:")
        logger.error(traceback.format_exc())
        backup_name = f"backup_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df_principal.to_excel(backup_name, index=False)
        logger.info(f"Backup automatic was save after the error: {backup_name}")

    finally:
        logger.info("Entrando no bloco finally...")
        if driver:
            logger.info("Executando driver_quit()...")
            driver_quit(driver)
            output_filename = f"output_{row['Mes']}_{row['Ano']}_final.xlsx"
            logger.info(f"Salvando Excel final: {output_filename}")
            df_principal.to_excel(output_filename, index=False)

    logger.info("Success\nSAFT non-billing submission process has finished.")
    logger.info("=== Analyzer finalizado ===")
