from src.driver import setup_driver
from src.login import login
import time
def main ():
    driver = setup_driver()
    
    if login(driver, '513029818', 'CTKCICXYFZAT19'):
        print("Login successful")
        time.sleep(5)
        driver.save_screenshot("screenshot_login.png")

    time.sleep(10)
    driver.quit()

if __name__ == "__main__":
    main()