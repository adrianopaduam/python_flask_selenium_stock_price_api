""" Data validation routines """
import re
from urllib.parse import unquote_plus

from app.main.config import cache, Config, logger


@cache.memoize(Config.CACHE_TIMEOUT)
def validate_region_name(region_name):
    """
    Validates if region name is valid.
    Must be a non empty string
    """
    logger.info("Starting region parameter validation")
    is_valid_region = False
    error_message = None

    # Checking inexistent region
    if region_name is None:
        error_message = "'region' parameter must be informed"
        return is_valid_region, region_name, error_message

    # Checking region conformity
    region_name = unquote_plus(region_name).strip().replace('\"', '')
    if (
        not isinstance(region_name, str) or
        len(region_name) == 0 or
        not re.search(r"^[a-zA-Z\s\-]+$", region_name)
    ):
        error_message = " ".join([
            "'region' must be a non-empty string",
            "containing a valid country name",
            "(letters, whitespaces and hiphen only)"
        ])
    else:
        is_valid_region = True

    logger.info(f"Region informed: {region_name}")
    logger.info(f"Passed validation: {is_valid_region}")
    logger.info(f"Error message: {error_message}")

    return is_valid_region, region_name, error_message
