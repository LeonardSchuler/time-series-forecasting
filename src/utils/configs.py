# src/utils/config.py

import logging


def setup_logging(level=logging.INFO):
    """Set up logging for the utils package."""
    # Get the top-level package name from the module's __name__
    package_name = __name__.split(".")[
        0
    ]  # Gets the top-level package name (e.g., 'utils')

    # Get the logger for the top-level package
    logger = logging.getLogger(package_name)

    # Set the logging level for the logger
    logger.setLevel(level)

    # Remove existing handlers to prevent duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Set the format for the console handler
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

    # Prevent propagation to the root logger
    logger.propagate = False
