import logging

import pandas as pd

logger = logging.getLogger(__name__)


def minute_to_daily(df):
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

    logger.info(f"Frequency change: {original_frequency}min ->  1d")
    logger.info(f"Shape change: {original_shape} -> {reshaped_df.shape}")

    return reshaped_df


def daily_to_minute(df):
    df = df.copy()
    if isinstance(df, pd.Series):
        df = df.to_frame()
    df.index = pd.to_datetime(df.index)
    original_frequency = int((df.index[1] - df.index[0]).seconds / 60)
    original_shape = df.shape
    df.index.name = "date"
    df.columns = df.columns.str.rsplit("_", n=2, expand=True)
    df.columns.names = [None, "hour", "minute"] + [None] * (len(df.columns.names) - 3)
    df = df.stack(["hour", "minute"], future_stack=True)
    df = df.reset_index()
    index = pd.to_datetime(df.date.astype(str) + " " + df.hour + ":" + df.minute)
    df = df.set_index(index)
    df = df.drop(columns=["date", "hour", "minute"])
    new_frequency = int((df.index[1] - df.index[0]).seconds / 60 / 60 / 24)
    new_shape = df.shape
    logger.info(f"Frequency change: {original_frequency}min ->  {new_frequency}d")
    logger.info(f"Shape change: {original_shape} -> {new_shape}")
    return df
