import utils


def test_transform_fifteen_mins_to_daily_generates_96_times_num_cols_new_values():
    start_date = "2021-01-01"
    end_date = "2022-01-01"
    freq = "15min"
    seed = 42

    data = utils.datasets.make_electricity_data(
        start_date=start_date, end_date=end_date, freq=freq, random_state=seed
    )
    daily = utils.transformations.minute_to_daily(data)
    assert len(daily) == 365
    assert daily.shape[1] == 96 * len(data.columns)


def test_transform_hourly_to_daily_generates_24_times_num_cols_new_values():
    start_date = "2021-01-01"
    end_date = "2022-01-01"
    freq = "1h"
    seed = 42

    data = utils.datasets.make_electricity_data(
        start_date=start_date, end_date=end_date, freq=freq, random_state=seed
    )
    daily = utils.transformations.minute_to_daily(data)
    assert len(daily) == 365
    assert daily.shape[1] == 24 * len(data.columns)


def test_transform_fifteen_mins_to_daily_and_back_is_idempotent():
    start_date = "2021-01-01"
    end_date = "2022-01-01"
    freq = "15min"
    seed = 42

    data = utils.datasets.make_electricity_data(
        start_date=start_date, end_date=end_date, freq=freq, random_state=seed
    )
    daily = utils.transformations.minute_to_daily(data)
    minutely = utils.transformations.daily_to_minute(daily)
    assert (data == minutely).all().all()
