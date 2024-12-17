import logging

import pandas as pd

logger = logging.getLogger(__name__)


def minute_to_daily(df: pd.DataFrame) -> pd.DataFrame:
    """Stacks observations of time points in a day as columns,
    such that every observation/row represents a day.
    If a column 'electricity' is available and observations follow a 15min interval,
    create new columns 'electricity_00_00', 'electricity_00_15', 'electricity_00_30'
    The widening is repeated with any additional columns as well.
    Inverse to daily_to_minute.

    Args:
        df (pd.DataFrame): Long dataframe where multiple observations make up an entire day.

    Returns:
        pd.DataFrame: Wide dataframe where every observation is a day.
    """
    df = df.copy()
    original_shape = df.shape
    original_frequency = int((df.index[1] - df.index[0]).seconds / 60)

    if isinstance(df, pd.Series):
        df = df.to_frame()

    columns = df.columns
    df.index = pd.to_datetime(df.index)

    # Extract the date and formatted time
    df["date"] = df.index.date
    df["time"] = df.index.strftime("%H_%M")

    # Perform the pivot (reshape)
    reshaped_df = df.pivot(index="date", columns="time", values=columns)

    # Flatten multi-level columns if necessary
    reshaped_df.columns = [f"{col[0]}_{col[1]}" for col in reshaped_df.columns]
    if reshaped_df.index.dtype == "object":
        reshaped_df.index = pd.to_datetime(reshaped_df.index)

    reshaped_df.index.freq = "D"

    logger.info(f"Frequency change: {original_frequency}min -> 1d")
    logger.info(f"Shape change: {original_shape} -> {reshaped_df.shape}")

    return reshaped_df


def daily_to_minute(df: pd.DataFrame) -> pd.DataFrame:
    """Goes from wide format where the columns of the dataframe df are all x-min intervals of a day to long format where every row is a x-min interval.
    Assumes that the columns are of the form electricity_00_00, electricity_00_15, electricity_00_30
    If multiple column prefixes are available, e.g. additionally: wind_00_00, wind_00_15,
    create two columns in return frame, 'electricity', 'wind'.
    Inverse to minute_to_daily.


    Args:
        df (pd.DataFrame): Wide dataframe where all columns represent an entire day.

    Returns:
        pd.DataFrame: Long dataframe where two observations differ by the original column frequency difference.
    """
    df = df.copy()
    if isinstance(df, pd.Series):
        df = df.to_frame()
    df.index = pd.to_datetime(df.index)
    original_frequency = int((df.index[1] - df.index[0]).total_seconds() / 60 / 60 / 24)
    original_shape = df.shape
    df.index.name = "date"
    df.columns = df.columns.str.rsplit("_", n=2, expand=True)
    df.columns.names = [None, "hour", "minute"] + [None] * (len(df.columns.names) - 3)
    df = df.stack(["hour", "minute"], future_stack=True)
    df = df.reset_index()
    index = pd.to_datetime(df.date.astype(str) + " " + df.hour + ":" + df.minute)
    df = df.set_index(index)
    df = df.drop(columns=["date", "hour", "minute"])
    new_frequency = int((df.index[1] - df.index[0]).total_seconds() / 60)
    new_shape = df.shape
    logger.info(f"Frequency change: {original_frequency}d -> {new_frequency}min")
    logger.info(f"Shape change: {original_shape} -> {new_shape}")
    return df
