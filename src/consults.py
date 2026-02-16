import time

from pandas import options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from src.defines import *
from src.log_config import logger
from src.utils import *


def consult_comunication(driver, year, month):
    logger.debug(
        f"[consult_comunication] Início | year={year} ({type(year)}) | month={month}"
    )

    try:
        bt_consult = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div/div[4]/div[3]/div/fieldset/div/div/p[2]/a[2]",
                )
            )
        )
        logger.debug("[consult_comunication] Botão Consultar encontrado, clicando...")
        bt_consult.click()
    except TimeoutException:
        logger.error("[consult_comunication] Botão Consultar não encontrado.")
        return False

    try:
        ft_year = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.ID, "anoFilter"))
        )
        logger.debug("[consult_comunication] Dropdown anoFilter encontrado.")
    except TimeoutException:
        logger.error("[consult_comunication] anoFilter não encontrado!")
        return False

    # Log dos options do dropdown
    options = ft_year.find_elements(By.TAG_NAME, "option")
    values = [opt.get_attribute("value") for opt in options]
    texts = [opt.text for opt in options]

    logger.debug(f"[consult_comunication] Options values disponíveis: {values}")
    logger.debug(f"[consult_comunication] Options texts disponíveis: {texts}")

    # Verificar se o ano requisitado existe no dropdown
    if str(year) not in values:
        logger.error(
            f"[consult_comunication] Dropdown não contém o ano '{year}'. Nada será selecionado."
        )
        return False

    try:
        from selenium.webdriver.support.ui import Select

        select_year = Select(ft_year)
        select_year.select_by_value(str(year))
        logger.debug(f"[consult_comunication] Ano '{year}' selecionado com sucesso.")
    except Exception as e:
        logger.error(f"[consult_comunication] Falha ao selecionar o ano '{year}': {e}")
        return False

    # Seleção do mês
    try:
        ft_month = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.ID, "mesFilter"))
        )
        logger.debug("[consult_comunication] Dropdown mesFilter encontrado.")
    except TimeoutException:
        logger.error("[consult_comunication] mesFilter não encontrado!")
        return False

    # Meses também podem ser logados
    month_options = ft_month.find_elements(By.TAG_NAME, "option")
    month_values = [m.get_attribute("value") for m in month_options]
    logger.debug(f"[consult_comunication] Options mês disponíveis: {month_values}")

    if str(month) not in month_values:
        logger.error(
            f"[consult_comunication] Mês '{month}' não está disponível no dropdown!"
        )
        return False

    try:
        from selenium.webdriver.support.ui import Select

        select_month = Select(ft_month)
        select_month.select_by_value(str(month))
        logger.debug(f"[consult_comunication] Mês '{month}' selecionado com sucesso.")
    except Exception as e:
        logger.error(f"[consult_comunication] Falha ao selecionar o mês '{month}': {e}")
        return False

    # Botão pesquisar
    try:
        bt_search = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.ID, "pesquisar"))
        )
        logger.debug("[consult_comunication] Botão Pesquisar encontrado, clicando...")
        bt_search.click()
        time.sleep(TIME_SLEEP)
        logger.debug("[consult_comunication] Pesquisa concluída.")
        return True
    except TimeoutException:
        logger.error("[consult_comunication] Botão Pesquisar não encontrado!")
        return False


def no_results_consult(driver):
    try:
        no_results = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.ID, "searchResults"))
        )
        if no_results.get_attribute("class") == "container":
            return True
        else:
            return False

    except TimeoutException:
        pass


def consult_files(driver, year, month):
    bt_consultfl = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div/div[4]/section[2]/div/fieldset/p[2]/a[2]",
            )
        )
    )
    bt_consultfl.click()
    time.sleep(TIME_SLEEP)
    logger.info("Consultando ficheiros...")

    # Abrir calendário
    bt_calendar = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "icon-calendar"))
    )
    bt_calendar.click()
    logger.info("Abrindo calendário...")

    # Clicar no header para ir para vista de anos
    bt_header = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[2]/div[2]/table/thead/tr/th[2]")
        )
    )
    bt_header.click()

    # Selecionar ano
    bt_select_year = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//span[contains(@class,'year') and text()='{year}']")
        )
    )
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});", bt_select_year
    )
    bt_select_year.click()
    logger.info("Selecionando ano...")

    # Selecionar mês
    bt_select_month = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                f"//span[contains(@class,'month') and text()='{month}']",
            )
        )
    )
    bt_select_month.click()
    logger.info("Selecionando mês...")

    # Pesquisar
    bt_search = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.ID, "pesquisar"))
    )
    bt_search.click()
    logger.info("Pesquisando ficheiros...")

    time.sleep(TIME_SLEEP)


def no_files_consult(driver):
    try:
        no_files_results = WebDriverWait(driver, WAIT_NO_FILES).until(
            EC.presence_of_element_located((By.ID, "ficheiros_wrapper"))
        )

        return True
    except TimeoutException:
        return False


def billing_abscence(driver, year, month):
    bt_comunicate = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div/div[4]/div[3]/div/fieldset/div/div/p[2]/a[1]",
            )
        )
    )
    bt_comunicate.click()
    time.sleep(TIME_SLEEP)
    logger.info("Comunicando ausência de faturação...")
    # Abrir calendário
    bt_calendar = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "icon-calendar"))
    )
    bt_calendar.click()
    logger.info("Abrindo calendário...")

    # Clicar no header para ir para vista de anos
    bt_header = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[2]/div[2]/table/thead/tr/th[2]")
        )
    )
    bt_header.click()

    # Selecionar ano
    bt_select_year = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//span[contains(@class,'year') and text()='{year}']")
        )
    )
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});", bt_select_year
    )
    bt_select_year.click()

    # Selecionar mês
    bt_select_month = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                f"//span[contains(@class,'month') and text()='{month}']",
            )
        )
    )
    bt_select_month.click()

    # OK
    bt_ok = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.ID, "escolheMesAnoBtn"))
    )
    bt_ok.click()
    time.sleep(TIME_SLEEP)

    # Checkbox
    chkbox_accept = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.ID, "porDeclararCheckbox"))
    )
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});", chkbox_accept
    )
    chkbox_accept.click()

    # Confirmar
    bt_confirm = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.ID, "guardarBtn"))
    )
    bt_confirm.click()
