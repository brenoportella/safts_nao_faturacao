from src.analyzer import analyzer
from src.defines import FILE
from src.driver import setup_driver


def main():
    driver = setup_driver()
    analyzer(driver, FILE)


if __name__ == "__main__":
    main()
