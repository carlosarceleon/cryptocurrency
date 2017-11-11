def merge_dfs_on_column(dataframes, labels, col):
    from pandas import DataFrame
    '''Merge a single column of each dataframe into a new combined dataframe'''
    series_dict = {}
    for index in range(len(dataframes)):
        series_dict[labels[index]] = dataframes[index][col]

    return DataFrame(series_dict)

def clean_data( df ):
    from numpy import nan

    df = df.replace(0, nan)
    df = df.mean(axis=1)

    return df

def add_fiat_column( altcoin_data, btc_fiat_datasets, fiat = "EUR" ):
    for altcoin in altcoin_data.keys():
        altcoin_data[altcoin]['price_{}'.format(fiat)] = \
            altcoin_data[altcoin]['weightedAverage'] * \
            btc_fiat_datasets['avg_btc_price_{}'.format(fiat)]

