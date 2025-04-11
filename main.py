from src.driver import setup_driver
from src.analyzer import analyzer
from src.defines import FILE

def main():
    driver = setup_driver()
    analyzer(driver, FILE)

if __name__ == "__main__":
    main()