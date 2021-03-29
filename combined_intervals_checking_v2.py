import pandas as pd
from datetime import date


def strings_to_datetime(df):
    df['hora inici'] = (pd.to_datetime(df['dia'] + ' ' + df['hora inici']))
    df['hora final'] = (pd.to_datetime(df['dia'] + ' ' + df['hora final']))
    df['dia'] = (pd.to_datetime(df['dia'])).dt.date

    return df

Intervals1 = pd.read_excel(
    'intervals_an/intervals-0.985.xlsx', index_col=0)
Intervals2 = pd.read_excel(
    'intervals_an/intervals-0.993.xlsx', index_col=0)

strings_to_datetime(Intervals1)
strings_to_datetime(Intervals2)

merged = pd.merge_ordered(Intervals1, Intervals2,
              on=['dia', 'hora inici', 'hora final'])