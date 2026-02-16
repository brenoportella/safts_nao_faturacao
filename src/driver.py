import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

download_dir = os.path.dirname(os.path.abspath(__file__))


def setup_driver():
    """
    Configura e retorna uma instância headless do Chromium WebDriver.

    Requer que os pacotes `chromium` e `chromium-driver` estejam instalados
    no Debian. O driver e o navegador já ficam em versões compatíveis.
    """

    chrome_prefs = {
        "download.default_directory": str(download_dir),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # modo headless moderno
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.binary_location = "/usr/bin/chromium"
    options.add_experimental_option("prefs", chrome_prefs)

    service = ChromeService(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def driver_quit(driver):
    """
    Encerra corretamente a instância do WebDriver.
    """
    driver.quit()


# from selenium import webdriver

# def setup_driver():
#     """
#     Sets up and returns a configured Edge WebDriver instance.

#     This function configures the Edge WebDriver with specific preferences and options,
#     such as the default download directory and disabling popup blocking and safe browsing
#     features. It also runs the browser in headless mode.

#     Returns:
#         webdriver.Edge: A configured Edge WebDriver instance.
#     """
#     edge_prefs = {
#         'disable-popup-blocking': True,
#         'safebrowsing.enabled': False,
#     }

#     options = webdriver.EdgeOptions()
#     options.add_argument('--safebrowsing-disable-download-protection')
#     options.add_argument('--headless')
#     options.add_argument('--disable-cache')
#     options.add_argument('--disable-application-cache')
#     options.add_argument('--disable-offline-load-stale-cache')
#     options.add_experimental_option('prefs', edge_prefs)

#     driver = webdriver.Edge(options=options)
#     return driver

# def driver_quit(driver):
#     """
#     Quits the Edge WebDriver instance.

#     Args:
#         driver (webdriver.Edge): The Edge WebDriver instance to quit.
#     """
#     driver.quit()
