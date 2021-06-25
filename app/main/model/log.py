"""Custom logging module"""
import os
import logging
from pathlib import Path

from app.main.util.exceptions import LogFileCreationError


class ApiLogger:
    """
    Customized Logger class
    """

    def __init__(
        self, logger_name, logger_level=logging.INFO,
        record_log=True, log_file_path=None
    ):
        """
        Customized Logger class constructor

        Parameters:
            logger_name (str): The logger name

            logger_level (int): Optional logger level definition.
                follows python's logging module classification.
                Default: logging.INFO

            record_log (bool): Optional boolean flag
                for file logging necessity (default True)

            log_file_path (str): File path to store created logs.
                If not informed and record_log is True,
                then the log will be created at current user folder
    """
        # Logger creation (or recovery if already existent)
        self.__logger = logging.getLogger(logger_name)
        self.__logger.setLevel(logger_level)

        # Default logger format definition
        default_log_format = '%(asctime)s | %(levelname)s :: %(message)s'

        # Creating stream handler (if necessary)
        if self.__logger.hasHandlers():
            self.__logger.debug("Stream Handler Already Existent. Not created")
        else:
            # Stream handler creation
            ch = logging.StreamHandler()
            ch.setLevel(logger_level)

            # Log formatting default implementation
            ch.setFormatter(logging.Formatter(
                default_log_format,
                datefmt='%d/%b/%Y %H:%M:%S'
            ))

            # Handler insertion on logger
            self.__logger.addHandler(ch)

            self.__logger.debug("Stream Handler Successfully Created")

        # Creating file handler (if necessary)
        if record_log:
            self.__logger.debug("Creating File Handler")

            # File path manipulation (empty file protection)
            log_file_path = self.__parse_file_path(log_file_path)

            # Defining log file creation necessity
            create_file_handler = self.__define_handler_creation_necessity(
                log_file_path)

            # Checking file handler pre-existence
            file_handler_already_exists = any([
                isinstance(handler, logging.FileHandler)
                for handler in self.__logger.handlers
            ])

            # Actual file handler creation
            if create_file_handler and not file_handler_already_exists:
                ch = logging.FileHandler(log_file_path)
                ch.setLevel(logger_level)

                # File log formatting definition
                ch.setFormatter(logging.Formatter(
                    default_log_format,
                    datefmt='%d/%b/%Y %H:%M:%S'
                ))

                # File handler insertion on logger
                self.__logger.addHandler(ch)
                self.__logger.debug("FileHandler successfully created")

            elif create_file_handler and file_handler_already_exists:
                self.__logger.debug(
                    "FileHandler already existent. Not created")

    def debug(self, message):
        """
        Log message on debug mode

        Parameters:
            message: (str)
                Message to be logged
        """
        self.__logger.debug(message)

    def info(self, message):
        """
        Log message on info mode

        Parameters:
            message: (str)
                Message to be logged
        """
        self.__logger.info(message)

    def warn(self, message):
        """
        Log message on warning mode

        Parameters:
            message: (str)
                Message to be logged
        """
        self.__logger.warning(message)

    def error(self, message):
        """
        Log message on error mode

        Parameters:
            message: (str)
                Message to be logged
        """
        self.__logger.error(message)

    def __parse_file_path(self, log_file_path):
        """
        Checks file path existence, and parse it to pathlib.Path object

        Parameters:
            log_file_path (str): The path of the file to record logs
        """
        # Informed path condition
        if log_file_path:
            log_file_path = Path(log_file_path)

        # Inexistent path condition
        else:
            self.__logger.debug(" ".join([
                "File path not informed.",
                "log file on home folder will be created"
            ]))
            log_file_path = Path.home() / "stocks_api.log"

        # Returning pathlib.Path object
        return log_file_path

    def __define_handler_creation_necessity(self, log_file_path):
        """
        Checks if the informed file path is valid, and writable
        """
        # Existent and writable file condition
        if (
            log_file_path.is_file() and
            os.access(log_file_path, os.W_OK)
        ):
            create_file_handler = True
            self.__logger.debug("File already existent and it is writable")

        # Inexistent but creatable file condition (new file creation)
        elif (
            log_file_path.parent.is_dir() and
            not log_file_path.is_dir() and
            os.access(log_file_path.parent, os.W_OK)
        ):
            log_file_path.touch()
            if not log_file_path.is_file():
                raise LogFileCreationError(
                    f"Unable to create/write on informed path: {log_file_path}"
                )

            create_file_handler = True
            self.__logger.debug("File created and it is writable")

        # Not writable/Not creatable file condition
        else:
            create_file_handler = False
            self.__logger.error("File or file folder is not writable")
            raise LogFileCreationError(
                f"Unable to create/write on informed path: {log_file_path}")

        # Return file handler creation necessity flag
        return create_file_handler
