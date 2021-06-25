""" Stocks recovery functions """
import re
import pandas as pd
from decouple import config
from bs4 import BeautifulSoup

from app.main.config import cache, Config, logger
from app.main.model.scrapping import ChromeScrapper

from app.main.util.xpath import xpath_info
from app.main.util.data_manipulation import format_stock
from app.main.util.exceptions import InexistentRegionError


@cache.memoize(Config.CACHE_TIMEOUT)
def recover_region_stocks(region_name):
    """
    Scraps over Yahoo portal to find all stocks on informed region
    """
    logger.info("Starting region stocks obtention")

    logger.info("Generating scrapper")
    scrapper = ChromeScrapper(
        logger,
        driver_wait_time=config("SCRAPPER_WAIT_TIME", cast=int),
        headless=config("SCRAPPER_HEADLESS_NAVIGATION", cast=bool)
    )

    logger.info("Navigating to target stocks page")
    print(config("YAHOO_STOCKS_URL"))
    scrapper.navigate_to(config("YAHOO_STOCKS_URL"))

    logger.info("Removing original filtering buttons")
    remove_original_filtering_buttons(scrapper)

    logger.info("Opening region filter")
    open_region_filter(scrapper)

    logger.info("Selecting informed region (if existent)")
    select_informed_region(scrapper, region_name)

    logger.info("Expanding results table (if necessary)")
    expand_stocks_table(scrapper)

    logger.info("Recovering stocks information")
    stock_information = recover_stocks(scrapper)

    logger.info("Parsing information to final format")
    stock_information = {
        stock['symbol']: format_stock(stock)
        for stock in stock_information
    }

    logger.info("Region stocks successfully obtained!")
    return stock_information


def remove_original_filtering_buttons(scrapper):
    """
    Removes original filtering info, for execution protection
    """
    removal_buttons = scrapper.find_elements(xpath_info['removal_buttons'])
    while len(removal_buttons) > 0:
        removal_buttons[0].click()
        removal_buttons = scrapper.find_elements(xpath_info['removal_buttons'])


def open_region_filter(scrapper):
    """
    Opens filters menu and selects the 'Region' filter
    """
    scrapper.press_clickable(xpath_info['add_filter_button'])

    scrapper.press_clickable(xpath_info['region_checkbox'])

    scrapper.press_clickable(xpath_info['close_menu_button'])

    scrapper.press_clickable(xpath_info['add_region_checkbox'])


def select_informed_region(scrapper, region_name):
    """
    Searches for informed region selector and, if found,
    clicks on search button
    """
    try:
        region_check_xpath = xpath_info['choose_region_checkbox'].format(
            region_name.title())
        scrapper.press_clickable(region_check_xpath)
    except Exception:
        raise InexistentRegionError(
            f"Inexistent region informed: {region_name}")

    scrapper.press_clickable(xpath_info['find_stocks_button'])

    scrapper.wait_element(xpath_info['matching_stocks_evidence'])


def expand_stocks_table(scrapper):
    """
    If the results are greater than 25 records, choose the 100 rows option
    for better performance
    """
    before_first, before_last, before_total = recover_result_metrics(scrapper)

    if before_total > 25:
        scrapper.press_clickable(xpath_info['show_25_rows_link'])

        scrapper.press_clickable(xpath_info['show_100_rows_link'])

        transformation_wait_count = 0
        while True:
            after_first, after_last, after_total = recover_result_metrics(
                scrapper)

            if after_last != before_last:
                break
            elif transformation_wait_count > 1000:
                raise Exception("Results table expansion failed")
            else:
                print("Waiting table transformation to occur")
                transformation_wait_count += 1


def recover_stocks(scrapper):
    """
    Recovers all stocks informed, concerning all possible paginations
    """
    last_first = 0
    retry_count = 0
    reload_count = 0
    stock_information = list()

    while True:
        try:
            first, last, total = recover_result_metrics(scrapper)
        except Exception as ex:
            if reload_count == 0:
                raise ex

        if first == last_first:
            logger.debug("skipping repeated")

            retry_count += 1
            if retry_count > config("SCRAPPER_RETRY_COUNT", cast=int):
                logger.info("Reloading the page")
                scrapper.reload_current_page()
                reload_count += 1

            if reload_count > config("SCRAPPER_RELOAD_COUNT", cast=int):
                logger.error("Failed to obtain all records")
                logger.error("Returning partial results")
                break

            continue

        else:
            retry_count = 0
            reload_count = 0

        logger.info(f"Recovering from {first} to {last} of {total}")

        # Page information recovery
        stock_information += recover_tabular_information(
            scrapper.read_page_source())

        # Jumping to next page
        if last < total:
            execute_next_page_jump(scrapper)
            last_first = first

        # Last page evidence: breaking
        else:
            break

    return stock_information


def recover_tabular_information(page_source):
    data_table = BeautifulSoup(page_source, "html.parser").select_one("table")
    stocks_page = pd.read_html(str(data_table))[-1]

    tabular_information = stocks_page[["Name", "Symbol", "Price (Intraday)"]].rename(columns={
        "Name": "name",
        "Symbol": "symbol",
        "Price (Intraday)": "price"
    }).fillna("").to_dict("records")

    return tabular_information


def recover_result_metrics(scrapper):
    """
    Finds results information and parses in workable variables
    """
    result_metrics = scrapper.read_element_text(
        xpath_info['result_metrics_span'])
    first, last, total = map(
        int,
        re.search(r"^([0-9]+)\-([0-9]+)\sof\s([0-9]+)\sresults$",
                  result_metrics).groups()
    )

    return first, last, total


def execute_next_page_jump(scrapper):
    """
    Clicks on 'Next Page' link
    """
    scrapper.press_clickable(xpath_info['next_page_link'])

    scrapper.wait_element(xpath_info['matching_stocks_evidence'])
