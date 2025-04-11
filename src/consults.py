from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

from src.defines import *

def consult_comunication(driver, year, month):
    bt_consult = WebDriverWait(driver, WAIT_TIME).until(
                      EC.presence_of_element_located((By.XPATH,"/html/body/div/div[4]/div[3]/div/fieldset/div/div/p[2]/a[2]")))
    bt_consult.click()

    ft_year = WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((By.ID,"anoFilter")))
    ft_select_year = ft_year.find_element(By.CSS_SELECTOR, f"option[value='{year}']")
    ft_select_year.click()

    ft_month = WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((By.ID,"mesFilter")))
    ft_select_month = ft_month.find_element(By.CSS_SELECTOR, f"option[value='{month}']")
    ft_select_month.click()

    bt_search = WebDriverWait(driver, WAIT_TIME).until(
                      EC.presence_of_element_located((By.ID,"pesquisar")))
    bt_search.click()
    time.sleep(TIME_SLEEP)

def no_results_consult(driver):
    try:
        no_results = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.ID, 'searchResults')))
        if no_results.get_attribute("class") == "container":
          return True
        else:
          return False
          
    except TimeoutException:
        pass

def consult_files(driver, year, month):
    bt_consultfl = WebDriverWait(driver, WAIT_TIME).until(
                      EC.presence_of_element_located((By.XPATH,"/html/body/div/div[4]/section[2]/div/fieldset/p[2]/a[2]")))
    bt_consultfl.click()
    
    bt_calendar = WebDriverWait(driver, WAIT_TIME).until(
                      EC.presence_of_element_located((By.CLASS_NAME,"icon-calendar")))
    bt_calendar.click()
    bt_year = WebDriverWait(driver, WAIT_TIME).until(
                      EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div[2]/table/thead/tr/th[2]")))
    bt_year.click()

    bt_select_year = WebDriverWait(driver, WAIT_TIME).until(
                      EC.presence_of_element_located((By.XPATH,f"//span[contains(@class, 'year') and text()='{year}']")))
    bt_select_year.click()

    bt_select_month = WebDriverWait(driver, WAIT_TIME).until(
                      EC.presence_of_element_located((By.XPATH,f"//span[contains(@class,'month') and text()='{month}']")))
    bt_select_month.click()
    
    bt_search = WebDriverWait(driver, WAIT_TIME).until(
                      EC.presence_of_element_located((By.ID,"pesquisar")))
    bt_search.click()
    time.sleep(TIME_SLEEP)
    
def no_files_consult(driver):
    try:
      no_files_results = WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.ID, "ficheiros_wrapper")))

      return True
    except TimeoutException:
      return False
    
def billing_abscence(driver, year, month):
    bt_comunicate = WebDriverWait(driver, WAIT_TIME).until(
                      EC.presence_of_element_located((By.XPATH,"/html/body/div/div[4]/div[3]/div/fieldset/div/div/p[2]/a[1]")))
    bt_comunicate.click()
    time.sleep(TIME_SLEEP)
    bt_calendar = WebDriverWait(driver, WAIT_TIME).until(
                      EC.presence_of_element_located((By.CLASS_NAME,"icon-calendar")))
    bt_calendar.click()

    bt_year = WebDriverWait(driver, WAIT_TIME).until(
                      EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div[2]/table/thead/tr/th[2]")))
    bt_year.click()

    bt_select_year = WebDriverWait(driver, WAIT_TIME).until(
                      EC.presence_of_element_located((By.XPATH,f"//span[contains(@class,'year') and text()='{year}']")))
    bt_select_year.click()

    bt_select_month = WebDriverWait(driver, WAIT_TIME).until(
                      EC.presence_of_element_located((By.XPATH,f"//span[@class='month' and text()='{month}']")))
    bt_select_month.click()

    bt_ok = WebDriverWait(driver, WAIT_TIME).until(
                      EC.presence_of_element_located((By.ID,"escolheMesAnoBtn")))
    bt_ok.click()
    time.sleep(TIME_SLEEP)
    chkbox_accept = WebDriverWait(driver, WAIT_TIME).until(
                      EC.presence_of_element_located((By.ID,"porDeclararCheckbox")))
    chkbox_accept.click()
    
    bt_confirm = WebDriverWait(driver, WAIT_TIME).until(
                      EC.presence_of_element_located((By.ID,"guardarBtn")))
    bt_confirm.click()