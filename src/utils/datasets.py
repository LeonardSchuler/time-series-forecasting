import numpy as np
import pandas as pd


def make_electricity_data(
    start_date, end_date, freq="15min", inclusive="left", random_state=None
):
    """
    Generate time series data for wind speed and electricity generation with dependency on wind speed.

    Parameters:
    - start_date (str): Start date of the time series (e.g., '2024-01-01').
    - end_date (str): End date of the time series (e.g., '2024-02-01').
    - freq (str): Frequency of the time series (default: '15min' for 15-minute intervals).
    - inclusive (str): Whether to set each bound as closed or open. (default: 'left' for [start,end)).
    - seed (int): Random seed for reproducibility (default: None).

    Returns:
    - pd.DataFrame: A DataFrame containing wind speed and electricity generation time series.
    """
    # Set seed for reproducibility
    if random_state is not None:
        np.random.seed(random_state)

    # Generate time index
    time_index = pd.date_range(
        start=start_date, end=end_date, freq=freq, inclusive=inclusive
    )

    # Generate wind speed data (in m/s) with some variability
    avg_wind_speed = 8  # Average wind speed in m/s
    std_wind_speed = 2  # Standard deviation
    wind_speed_no_seasonilty = np.random.normal(
        loc=avg_wind_speed, scale=std_wind_speed, size=len(time_index)
    )

    # Add daily, weekly, and yearly seasonality to wind speed
    daily_seasonality = np.sin(2 * np.pi * time_index.hour / 24)
    weekly_seasonality = np.sin(2 * np.pi * time_index.dayofweek / 7)

    # Yearly seasonality: assume wind speeds are higher in the middle of the year (summer)
    yearly_seasonality = np.sin(2 * np.pi * time_index.dayofyear / 365)

    # Combine seasonality components and add to wind speed
    wind_speed = (
        wind_speed_no_seasonilty
        + 3 * daily_seasonality
        + 2 * weekly_seasonality
        + 4 * yearly_seasonality
    )

    # Add some random noise and ensure wind speed stays positive
    wind_speed = np.clip(
        wind_speed + np.random.normal(0, 0.5, size=len(wind_speed)), 0, None
    )

    # Generate electricity output (in MW) with quadratic dependency on wind speed
    electricity = 0.1 * wind_speed**2 + np.random.normal(
        0, 1, size=len(time_index)
    )  # Add noise
    electricity = np.abs(electricity)

    # Create DataFrame for wind speed and electricity
    data = pd.DataFrame(
        {
            "time": time_index,
            "electricity": electricity,
            "wind_speed": wind_speed,
            "wind_speed_no_seasonality": wind_speed_no_seasonilty,
            "daily_seasonality": daily_seasonality,
            "weekly_seasonality": weekly_seasonality,
            "yearly_seasonality": yearly_seasonality,
        }
    )

    # Set timestamp as index
    data.set_index("time", inplace=True)

    return data
