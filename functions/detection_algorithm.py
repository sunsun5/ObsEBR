def detection(filtered_intervals, length):
    """
    Given a dataframe containing the time intervals, previously
    filtered according to the correlation between geomagnetic
    variations and the models, this functions groups intervals
    based on their starting times. If a group has a minimum
    length, it will be considered a SFE alert.

        INPUTS: dataframe with intervals' starting time,
                minimum group length
        OUTPUT: list of groups that meet length condition
    """

    filtered_intervals = filtered_intervals.sort_values('start_index')
    filtered_intervals.loc[(
        filtered_intervals.start_index.shift() <
        filtered_intervals.start_index - 3), 'group'] = 1

    filtered_intervals['group'] = (
        filtered_intervals['group'].cumsum().ffill().fillna(0))

    alerts_list = [df_g for name_g, df_g in filtered_intervals.groupby(
        'group').filter(lambda x: len(x) > length).groupby('group')]

    return alerts_list
