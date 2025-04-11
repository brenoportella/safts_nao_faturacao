from selenium import webdriver

def setup_driver():
    """
    Sets up and returns a configured Edge WebDriver instance.

    This function configures the Edge WebDriver with specific preferences and options,
    such as the default download directory and disabling popup blocking and safe browsing
    features. It also runs the browser in headless mode.

    Returns:
        webdriver.Edge: A configured Edge WebDriver instance.
    """
    edge_prefs = {
        'disable-popup-blocking': True,
        'safebrowsing.enabled': False,
    }

    options = webdriver.EdgeOptions()
    options.add_argument('--safebrowsing-disable-download-protection')
    # options.add_argument('--headless')
    options.add_argument('--disable-cache')
    options.add_argument('--disable-application-cache')
    options.add_argument('--disable-offline-load-stale-cache')
    options.add_experimental_option('prefs', edge_prefs)

    driver = webdriver.Edge(options=options)
    return driver

def driver_quit(driver):
    """
    Quits the Edge WebDriver instance.

    Args:
        driver (webdriver.Edge): The Edge WebDriver instance to quit.
    """
    driver.quit()