# src/utils/config.py

import logging

import pandas as pd


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


def setup_pandas():
    """
    Configures sensible defaults for viewing pandas DataFrames in Jupyter notebooks.
    """
    # Set maximum rows and columns to display
    pd.set_option("display.max_rows", 100)  # Show up to 100 rows
    pd.set_option("display.max_columns", 20)  # Show up to 20 columns

    # Set column width and precision
    pd.set_option("display.max_colwidth", 100)  # Column width to display
    pd.set_option("display.precision", 2)  # Decimal precision for floats
    pd.set_option("display.float_format", "{:.2f}".format)


def setup_plots():
    """
    Configures sensible defaults for plotting in Jupyter notebooks.
    """
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Set figure size and resolution
    plt.rcParams["figure.figsize"] = [12, 6]  # Set default figure size (width, height)
    plt.rcParams["figure.dpi"] = 100  # Set default dots per inch (DPI)

    # Set plot style
    sns.set_style("darkgrid")


def setup():
    setup_logging()
    setup_pandas()
    setup_plots()
