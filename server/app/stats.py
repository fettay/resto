import pandas as pd


def compute_evolution(data_dict, aggregate_days, date_key, aggregate_function):
    df = pd.DataFrame(data_dict)
    df[date_key] = pd.to_datetime(df[date_key])
    take_last = (df.shape[0] // aggregate_days) * aggregate_days + 1
    min_date = pd.Timestamp.today() - pd.Timedelta(days=take_last)
    max_date = pd.Timestamp.today() - pd.Timedelta(days=1)
    df = df[(min_date < df[date_key]) & (df[date_key] < max_date)]
    values = df.groupby(pd.Grouper(key=date_key, freq="%dd" % aggregate_days, label='right')).agg(aggregate_function)
    mean_passed = (values.iloc[:-1]).mean().values[0]
    val = values.iloc[-1].values[0]
    return (val, ((val - mean_passed) / mean_passed) * 100)