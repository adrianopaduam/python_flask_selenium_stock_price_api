""" Selenium custom scrapping class """
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

from app.main.util.exceptions import DriverGenerationError, ElementNotFoundError


class ChromeScrapper:
    """
    Google Chrome scrapper class

    Attributes:
        logger (stocks_api.log.ApiLogger): The application logger

        driver (selenium.webdriver.Chrome): Selenium scrapping driver

        wait (selenium.webdriver.Chrome): Selenium scrapping wait
    """

    def __init__(self, logger, driver_wait_time=30, headless=False):
        """
        Google Chrome scrapper class constructor

        Arguments:
            logger (stocks_api.log.ApiLogger): The application logger

            deriver_wait_time (int):  Optional feature to tweak waiting time

            headless (bool): Optional flag to run driver on headless mode
        """
        # Logger attribute generation
        self.logger = logger

        # Driver and Wait objects generation
        self.driver, self.wait = self.__generate_driver(
            driver_wait_time, headless
        )

    def __del__(self):
        """
        Google Chrome scrapper class destructor
        """
        # Guaranteeing driver navigation closure
        self.exit_navigation()

    def __generate_driver(self, driver_wait_time, headless):
        """
        Generates google chrome driver and wait with specified options

        Arguments:
            deriver_wait_time (int):  Optional feature to tweak waiting time

            headless (bool): Optional flag to run driver on headless mode
        """
        try:
            # Driver options definition
            self.logger.info("Selenium driver options definition")
            options = webdriver.ChromeOptions()
            if headless:
                options.headless = True
                options.add_argument('window-size=2000x1500')
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")

            # Selenium driver instantiation
            self.logger.info("Selenium driver instantiation")
            driver = webdriver.Chrome(
                ChromeDriverManager(log_level=0).install(),
                options=options
            )

            # Selenium wait instantiation
            self.logger.info("Selenium wait instantiation")
            wait = WebDriverWait(driver, driver_wait_time)

            # Returning created objects
            return driver, wait

        except Exception as driver_gen_exc:
            # Exception detailing
            exc_detail = f"{type(driver_gen_exc).__name__} => {driver_gen_exc}"
            self.logger.error(f"Error in driver generation: {exc_detail}")

            # Known exception raising
            raise DriverGenerationError(exc_detail)

    def navigate_to(self, page_url):
        """
        Navigates to informed page
        """
        self.logger.info(f"Navigating to {page_url}")
        self.driver.get(page_url)

    def reload_current_page(self):
        """
        Reloads current page
        """
        self.logger.info(f"Reloading {self.driver.current_url}")
        self.driver.get(self.driver.current_url)

    def wait_element(self, element_xpath):
        """
        Wait until element is present on page
        """
        try:
            self.logger.info(f"Waiting element: {element_xpath}")

            # Searching element
            element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, element_xpath))
            )

            # Returning element
            return element

        except Exception:  # pragma: no cover
            self.logger.info("Failed to find element")
            raise ElementNotFoundError(f"Element not found: {element_xpath}")

    def find_elements(self, elements_xpath):
        """
        Find all elements with informed xpath
        """
        try:
            self.logger.info(f"Finding elements: {elements_xpath}")

            # Searching elements
            elements = self.driver.find_elements_by_xpath(elements_xpath)

            # Returning elements list
            return elements

        except Exception as ex:  # pragma: no cover
            self.logger.info("Failed to find elements")

            error_msg = f"{type(ex).__name__} => {ex}"
            raise Exception(f"Unknown error to find elements: {error_msg}")

    def press_clickable(self, clickable_xpath):
        """
        Execute click action on clickable elements
        """
        try:
            # Searching clickable
            clickable_element = self.wait_element(clickable_xpath)

            # Pressing clickable
            self.logger.info(f"Pressing clickable: {clickable_xpath}")
            clickable_element.click()

        except Exception:  # pragma: no cover
            self.logger.info("Failed to press clickable")
            raise ElementNotFoundError(f"Clickable not found: {clickable_xpath}")

    def read_element_text(self, element_xpath):
        """
        Find element on page and return the .text component
        """
        # Searching element
        element = self.wait_element(element_xpath)

        # Returning element text
        return element.text

    def read_page_source(self):
        """
        Returns current page source
        """
        return self.driver.page_source

    def exit_navigation(self):
        """
        Securely finalizes driver navigation
        """
        try:
            self.driver.quit()
            self.logger.info("Driver successfully finalized")
        except Exception:
            self.logger.info("Driver already finalized. Skipping action")
