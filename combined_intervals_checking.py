import pandas as pd
from datetime import date
from itertools import product
from functions import overlap


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

print(Intervals1[Intervals1['dia'] == date(2001, 4, 15)])
for (i1,int1),(i2,int2) in product(
        enumerate(Intervals1),enumerate(Intervals2)):
    if overlap(int1,int2):
        print(i1,i2)