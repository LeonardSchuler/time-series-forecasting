from utils import datasets


def test_make_electricity_data_for_a_year_generates_a_year_worth_of_data():
    start_date = "2023-01-01"
    end_date = "2024-01-01"
    freq = "15min"
    seed = 42

    data = datasets.make_electricity_data(
        start_date=start_date, end_date=end_date, freq=freq, random_state=seed
    )
    assert (
        len(data) == 4 * 24 * 365
    ), f"There are 4 15-min intervals per hour, 24hours in a day, and 365 days in 2023: {35040} != {len(data)}"
