import pandas as pd
from datetime import date


def strings_to_datetime(df):
    df['hora inici'] = (pd.to_datetime(df['dia'] + ' ' + df['hora inici']))
    df['hora final'] = (pd.to_datetime(df['dia'] + ' ' + df['hora final']))
    df['dia'] = (pd.to_datetime(df['dia'])).dt.date

    return df

Intervals1 = pd.read_excel(
    'intervals_collections/intervals_anna/intervals-0.99.xlsx', index_col=0)
Intervals2 = pd.read_csv(
    'intervals_collections/intervals_alba/alba-0.7.csv', index_col=None, delimiter=';')

strings_to_datetime(Intervals1)
strings_to_datetime(Intervals2)

merged = pd.merge_ordered(Intervals1, Intervals2,
              on=['dia', 'hora inici', 'hora final', 'resultat'])
def join_times(x):
    startdf = pd.DataFrame({'time':x['hora inici'], 'what':1})
    enddf = pd.DataFrame({'time':x['hora final'], 'what':-1})
    mergdf = pd.concat([startdf, enddf]).sort_values('time')
    mergdf['running'] = mergdf['what'].cumsum()
    mergdf['newwin'] = mergdf['running'].eq(1) & mergdf['what'].eq(1)
    mergdf['group'] = mergdf['newwin'].cumsum()
    x['group'] = mergdf['group'].loc[mergdf['what'].eq(1)]
    return mergdf

def rejoin_times(x):
    startdf = pd.DataFrame({'time':x['hora inici'], 'what':1})
    enddf = pd.DataFrame({'time':x['hora final'], 'what':-1})
    mergdf = pd.concat([startdf, enddf]).sort_values('time')
    mergdf.loc[(
        mergdf.time.shift() <
        mergdf.time - 3), 'group'] = 1
    mergdf['running'] = mergdf['what'].cumsum()
    mergdf['newwin'] = mergdf['running'].eq(1) & mergdf['what'].eq(1)
    mergdf['group'] = mergdf['newwin'].cumsum()
    x['group'] = mergdf['group'].loc[mergdf['what'].eq(1)]
    return mergdf

mergdf = join_times(merged)
grouped_df = merged.groupby('group')
combined = pd.DataFrame()
combined = grouped_df.max()
combined['hora inici'] = grouped_df['hora inici'].min()
print(len(combined[combined['resultat'] == 'VERDADERO']))
print(len(combined[combined['resultat'] == 'FALSO']))
print(len(Intervals1[Intervals1['resultat'] == 'VERDADERO']))
print(len(Intervals1[Intervals1['resultat'] == 'FALSO']))
print(len(Intervals2[Intervals2['resultat'] == 'VERDADERO']))
print(len(Intervals2[Intervals2['resultat'] == 'FALSO']))
