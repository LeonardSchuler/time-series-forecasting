import utils


def test_split_three_years_electricity_data_evenly():
    start_date = "2021-01-01"
    end_date = "2024-01-01"
    freq = "15min"
    seed = 42

    data = utils.datasets.make_electricity_data(
        start_date=start_date, end_date=end_date, freq=freq, random_state=seed
    )
    data = utils.transformations.minute_to_daily(data)
    train, val, test = utils.splits.to_train_validation_test_data(
        data, "2022-01-01", "2023-01-01"
    )
    assert len(train) == 365
    assert len(val) == 365
    assert len(test) == 365
