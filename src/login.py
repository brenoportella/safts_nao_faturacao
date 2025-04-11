from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.defines import WAIT_TIME


def login(driver, nif, password):
    driver.get(
        'https://faturas.portaldasfinancas.gov.pt/painelEmitente.action'
    )
    aut_nif = WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[1]/section/div[1]/div/div/label[2]'))
    )
    aut_nif[0].click()

    field_nif = WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_all_elements_located((By.ID, 'username'))
    )
    field_nif[0].send_keys(nif)

    field_password = WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_all_elements_located((By.NAME, 'password'))
    )
    field_password[0].send_keys(password)
    
    bt_login = WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_all_elements_located((By.ID, 'sbmtLogin'))
    )
    bt_login[0].click()

wrong_expired_time = 2
def wrong_password(driver):
    try:
        error_message = WebDriverWait(driver, wrong_expired_time).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'error-message'))
        )
        return True
    except TimeoutException:
        return False


def expired_password(driver):
    try:
        renew_password = WebDriverWait(driver, wrong_expired_time).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '/html/body/div/main/div/div/div/section/div/form/div[1]',
                )
            )
        )

        return True
    except TimeoutException:
        return False


def disconnect(driver):
    driver.get(
        'https://www.acesso.gov.pt//jsp/logout.jsp?partID=PFAP&path=/geral/atauth/logout'
    )
